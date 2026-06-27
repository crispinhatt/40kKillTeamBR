#!/usr/bin/env python3
"""
Repacker do formato .jfs (Warhammer 40K: Kill Team).

Recebe um .jfs original + um dicionario {hash_do_arquivo: novos_bytes}
e produz um novo .jfs com esses arquivos substituidos, recalculando
offsets, tamanhos comprimidos/descomprimidos e o cabecalho. Todos os
demais arquivos do pacote sao copiados byte-a-byte sem reprocessar
(zero risco de corromper o que nao foi tocado).

Uso:
    python3 repack_jfs.py <original.jfs> <saida.jfs> hash1=arquivo1.bin [hash2=arquivo2.bin ...]
"""
import struct
import zlib
import sys


def parse_jfs(path):
    with open(path, 'rb') as f:
        data = f.read()

    magic = data[0:4]
    if magic[1:4] != b'SFJ':
        raise ValueError(f"Magic inesperado em {path}: {magic!r}")

    u1, u2, numfiles = struct.unpack_from('<III', data, 4)
    entries = []
    pos = 16
    for _ in range(numfiles):
        h, off, csize, dsize, clevel, cflag = struct.unpack_from('<IIIIII', data, pos)
        entries.append({
            'hash': h, 'offset': off, 'csize': csize,
            'dsize': dsize, 'clevel': clevel, 'compressed': cflag,
        })
        pos += 24

    return data, entries, {'u1': u1, 'u2': u2, 'numfiles': numfiles, 'header_end': pos}


def repack(original_path, output_path, substituicoes):
    """substituicoes: dict {hash:int -> novos_bytes_descomprimidos:bytes}"""
    data, entries, info = parse_jfs(original_path)

    novos_chunks = []   # bytes ja comprimidos (ou crus) de cada entrada, na ordem original
    novas_entries = []

    for e in entries:
        h = e['hash']
        if h in substituicoes:
            payload = substituicoes[h]
            chunk = zlib.compress(payload, 6)
            csize = len(chunk)
            dsize = len(payload)
            clevel = e['clevel']  # mantem cosmetico igual ao original
            compressed = 1
        else:
            # copia o chunk original sem tocar (bytes comprimidos identicos ao original)
            chunk = data[e['offset']: e['offset'] + e['csize']]
            csize = e['csize']
            dsize = e['dsize']
            clevel = e['clevel']
            compressed = e['compressed']

        novos_chunks.append(chunk)
        novas_entries.append({
            'hash': h, 'csize': csize, 'dsize': dsize,
            'clevel': clevel, 'compressed': compressed,
        })

    header_end = 16 + len(novas_entries) * 24
    offset_atual = header_end
    for ne, chunk in zip(novas_entries, novos_chunks):
        ne['offset'] = offset_atual
        offset_atual += len(chunk)

    out = struct.pack('<4sIII', b'\x01SFJ', info['u1'], info['u2'], len(novas_entries))
    for ne in novas_entries:
        out += struct.pack('<IIIIII', ne['hash'], ne['offset'], ne['csize'],
                            ne['dsize'], ne['clevel'], ne['compressed'])
    for chunk in novos_chunks:
        out += chunk

    with open(output_path, 'wb') as f:
        f.write(out)

    print(f"Repack concluido: {output_path}")
    print(f"  Entradas: {len(novas_entries)} | Substituidas: {len(substituicoes)}")
    print(f"  Tamanho original: {len(data)} bytes | Tamanho novo: {len(out)} bytes")

    return out


if __name__ == '__main__':
    original_path, output_path = sys.argv[1], sys.argv[2]
    substituicoes = {}
    for arg in sys.argv[3:]:
        hash_str, arq = arg.split('=', 1)
        with open(arq, 'rb') as f:
            substituicoes[int(hash_str)] = f.read()
    repack(original_path, output_path, substituicoes)
