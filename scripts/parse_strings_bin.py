#!/usr/bin/env python3
"""
Parser do strings.bin do Warhammer 40K: Kill Team
(tabela mestre de localizacao, dentro de gui.jfs)

Formato (little-endian):
  int32 totalCount
  repete totalCount vezes:
    int32 keyLen
    bytes key[keyLen]            (ASCII, com padding de espacos at\u00e9 multiplo de 4)
    int32 numLanguages
    repete numLanguages vezes:
      int32 langCodeLen
      bytes langCode[langCodeLen]  (ASCII, padding de espacos at\u00e9 multiplo de 4)
      int32 textLen                (numero de CARACTERES, nao bytes)
      bytes text[textLen * 4]      (UTF-32 LE, um codepoint por 4 bytes)
"""
import struct
import sys
import json


def pad4(n):
    r = n % 4
    return 0 if r == 0 else 4 - r


def parse_strings_bin(path):
    with open(path, 'rb') as f:
        data = f.read()

    pos = 0
    (total_count,) = struct.unpack_from('<i', data, pos)
    pos += 4

    entries = []
    for entry_idx in range(total_count):
        (key_len,) = struct.unpack_from('<i', data, pos)
        pos += 4
        key = data[pos:pos + key_len].decode('ascii', errors='replace')
        pos += key_len + pad4(key_len)

        (num_langs,) = struct.unpack_from('<i', data, pos)
        pos += 4

        langs = {}
        for _ in range(num_langs):
            (lang_len,) = struct.unpack_from('<i', data, pos)
            pos += 4
            lang_code = data[pos:pos + lang_len].decode('ascii', errors='replace')
            pos += lang_len + pad4(lang_len)

            (text_len,) = struct.unpack_from('<i', data, pos)
            pos += 4
            raw = data[pos:pos + text_len * 4]
            pos += text_len * 4
            text = raw.decode('utf-32-le', errors='replace')
            langs[lang_code] = text

        entries.append({'key': key, 'langs': langs})

    leftover = len(data) - pos
    return entries, leftover, total_count


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None

    entries, leftover, total_count = parse_strings_bin(in_path)
    print(f"Total de entradas declaradas no header: {total_count}")
    print(f"Entradas lidas: {len(entries)}")
    print(f"Bytes restantes nao consumidos: {leftover} (deveria ser 0 se o parser estiver perfeito)")

    all_langs = set()
    for e in entries:
        all_langs.update(e['langs'].keys())
    print(f"Idiomas encontrados: {sorted(all_langs)}")

    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"JSON salvo em {out_path}")
