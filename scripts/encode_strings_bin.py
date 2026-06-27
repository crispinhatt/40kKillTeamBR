#!/usr/bin/env python3
"""
Encoder do strings.bin do Warhammer 40K: Kill Team.

Toma o JSON com TODOS os idiomas originais (strings_parsed.json) + nosso
JSON de traducao PT-BR (traducao_pt_br.json) e gera um novo strings.bin
binario, sobrescrevendo o texto de UM idioma (ex: "US" ou "ES") com a
traducao em portugues, para cada chave presente no arquivo de traducao.

As chaves do strings.bin original que NAO tem traducao em nosso arquivo
ficam intactas (todos os idiomas originais preservados).

Uso:
    python3 encode_strings_bin.py <strings_parsed.json> <traducao_pt_br.json> <idioma_alvo> <saida.bin>

    idioma_alvo: "US" ou "ES" (ou qualquer um dos 5 codigos originais)
"""
import struct
import sys
import json


def pad4(n):
    r = n % 4
    return 0 if r == 0 else 4 - r


def encode_string_field(s: str) -> bytes:
    """Codifica uma string (key ou langcode) com seu length-prefix e padding de espacos."""
    raw = s.encode('ascii')
    out = struct.pack('<i', len(raw)) + raw
    out += b' ' * pad4(len(raw))
    return out


def encode_text_field(s: str) -> bytes:
    """Codifica o campo de texto: int32 com numero de CARACTERES + UTF-32LE bytes."""
    raw = s.encode('utf-32-le')
    n_chars = len(raw) // 4
    return struct.pack('<i', n_chars) + raw


def build_strings_bin(original_entries, traducoes, idioma_alvo):
    traducoes_validas = {k: v for k, v in traducoes.items() if not k.startswith('_')}

    chaves_nao_encontradas = [k for k in traducoes_validas if k not in
                               {e['key'] for e in original_entries}]
    if chaves_nao_encontradas:
        print(f"AVISO: {len(chaves_nao_encontradas)} chaves de traducao nao "
              f"existem no strings.bin original: {chaves_nao_encontradas[:5]}...")

    out = struct.pack('<i', len(original_entries))
    aplicadas = 0

    for entry in original_entries:
        key = entry['key']
        langs = dict(entry['langs'])  # copia para nao mutar o original

        if key in traducoes_validas:
            langs[idioma_alvo] = traducoes_validas[key]
            aplicadas += 1

        out += encode_string_field(key)
        out += struct.pack('<i', len(langs))
        for lang_code, texto in langs.items():
            out += encode_string_field(lang_code)
            out += encode_text_field(texto)

    print(f"Traducoes aplicadas no idioma '{idioma_alvo}': {aplicadas} de {len(traducoes_validas)}")
    return out


if __name__ == '__main__':
    parsed_path, trad_path, idioma_alvo, saida_path = sys.argv[1:5]

    with open(parsed_path, encoding='utf-8') as f:
        original_entries = json.load(f)
    with open(trad_path, encoding='utf-8') as f:
        traducoes = json.load(f)

    novo_bin = build_strings_bin(original_entries, traducoes, idioma_alvo)

    with open(saida_path, 'wb') as f:
        f.write(novo_bin)

    print(f"strings.bin gerado: {saida_path} ({len(novo_bin)} bytes)")
