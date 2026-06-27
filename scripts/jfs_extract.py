#!/usr/bin/env python3
"""
Extrator de arquivos .jfs (Warhammer 40K: Kill Team / engine Juice/JFS v1)

Uso:
    python3 jfs_extract.py <arquivo.jfs> <arquivo.txt-da-lista> <pasta_saida>

O .txt-da-lista é opcional, mas recomendado: contém linhas no formato
    NomeDoArquivo.ext<TAB>hash<TAB>tamanho<TAB>data
e é usado para renomear as entradas extraídas com os nomes originais
(em vez de "__unknown_<hash>.bin").
"""
import struct
import zlib
import sys
import os


def get_hash(s: str) -> int:
    """Reimplementação validada do JfsHash.iGetHash (string.ToUpper() antes de hashear)."""
    s = s.upper()
    length = len(s)
    if length == 0:
        return 0
    h = 0
    if length != 1:
        for i in range(length - 1):
            for j in range(i, length):
                ci = ord(s[i]) & 0xFF
                cj = ord(s[j]) & 0xFF
                h += (ci + i) * (ci + 7) * (cj + 19) * (cj + j)
        h &= 0xFFFFFFFF
    return h % 4000000000


def load_name_map(txt_path):
    """Lê o .txt sidecar (nome\thash\ttamanho\tdata) e devolve dict hash->nome."""
    mapping = {}
    if not txt_path or not os.path.isfile(txt_path):
        return mapping
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            name = parts[0]
            try:
                h = int(parts[1])
            except ValueError:
                continue
            mapping[h] = name
    return mapping


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


def extract_all(jfs_path, txt_path, out_dir):
    data, entries, info = parse_jfs(jfs_path)
    name_map = load_name_map(txt_path)

    os.makedirs(out_dir, exist_ok=True)

    ok, fail, unknown = 0, 0, 0
    log_lines = []

    for e in entries:
        h = e['hash']
        off, csize, dsize, cflag = e['offset'], e['csize'], e['dsize'], e['compressed']
        chunk = data[off:off + csize]

        try:
            payload = zlib.decompress(chunk) if cflag == 1 else chunk
        except Exception as ex:
            fail += 1
            log_lines.append(f"ERRO hash={h} offset={off}: {ex}")
            continue

        if len(payload) != dsize:
            log_lines.append(f"AVISO hash={h}: tamanho descomprimido {len(payload)} != esperado {dsize}")

        name = name_map.get(h)
        if name is None:
            unknown += 1
            rel_name = f"__unknown_{h}.bin"
        else:
            rel_name = name.replace('\\', os.sep).replace('/', os.sep)

        out_path = os.path.join(out_dir, rel_name)
        os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)

        # Evita colisão silenciosa se dois nomes iguais aparecerem (não deveria acontecer)
        if os.path.exists(out_path):
            base, ext = os.path.splitext(out_path)
            out_path = f"{base}__hash{h}{ext}"

        with open(out_path, 'wb') as f:
            f.write(payload)

        ok += 1

    summary = (f"{os.path.basename(jfs_path)}: {info['numfiles']} entradas | "
               f"extraidas={ok} falhas={fail} sem_nome_no_txt={unknown}")
    log_lines.insert(0, summary)
    print(summary)
    if unknown:
        print(f"  -> {unknown} arquivo(s) sem correspondencia no .txt (salvos como __unknown_<hash>.bin)")
    if fail:
        print(f"  -> {fail} falha(s) de descompressao, ver log")

    with open(os.path.join(out_dir, '_extract_log.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))

    return ok, fail, unknown


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    jfs_path = sys.argv[1]
    txt_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else None
    out_dir = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(jfs_path)[0] + '_extraido'
    extract_all(jfs_path, txt_path, out_dir)
