# Como funciona — Documentação Técnica

Guia detalhado da engenharia reversa e da estrutura da tradução, para quem deseja contribuir, revisar termos ou adaptar para outro idioma.

---

## 🧱 Estrutura do jogo

O *Warhammer 40,000: Kill Team* (port PC, 2014, por d3t Limited) usa uma engine interna proprietária chamada **JET**, herdada dos jogos de corrida *Juiced* / *Juiced 2: Hot Import Nights* (também desenvolvidos pela mesma equipe, então conhecida como Juice Games, depois THQ Digital Studios Warrington).

Os assets do jogo são empacotados em arquivos `.jfs` (**J**et **F**ile **S**ystem), um formato binário proprietário sem nenhuma ferramenta pública de extração compatível com esta versão do formato (existe uma ferramenta para o *Juiced 2*, mas usa uma estrutura de cabeçalho externa diferente — o Kill Team embute o cabeçalho dentro do próprio `.jfs`).

Todo o texto do jogo está concentrado em **um único arquivo dentro do `gui.jfs`**: o `strings.bin`, uma tabela mestre multi-idioma.

---

## 🔑 Algoritmo de hash dos nomes de arquivo

Dentro de um `.jfs`, cada arquivo é identificado por um **hash de 32 bits** do seu nome (não pelo nome em si). O algoritmo foi extraído via desmontagem do `.NET IL` de uma ferramenta de extração do Juiced 2 (que usa o mesmo algoritmo de hash da engine JET) e validado byte a byte contra os arquivos reais do Kill Team:

```python
def get_hash(s: str) -> int:
    s = s.upper()  # IMPORTANTE: hash é calculado sobre a string em CAIXA ALTA
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
```

Exemplo validado: `get_hash("strings.bin")` = `3190977537`.

---

## 📦 Estrutura do contêiner `.jfs`

**Cabeçalho do arquivo (16 bytes, little-endian):**

| Offset | Tamanho | Campo |
|---|---|---|
| 0 | 4 bytes | Magic `\x01SFJ` (JFS versão 1) |
| 4 | 4 bytes | Inteiro auxiliar (uso não totalmente mapeado) |
| 8 | 4 bytes | Inteiro auxiliar (uso não totalmente mapeado) |
| 12 | 4 bytes | Número total de arquivos no pacote |

**Por arquivo, um registro de 24 bytes** (repetido N vezes, logo após o cabeçalho):

| Campo | Tipo | Descrição |
|---|---|---|
| `hash` | uint32 | Hash do nome do arquivo (algoritmo acima) |
| `offset` | uint32 | Posição absoluta dos dados no `.jfs` |
| `compressedSize` | uint32 | Tamanho comprimido |
| `decompressedSize` | uint32 | Tamanho real do arquivo |
| `compressionLevel` | uint32 | Nível de compressão usado (cosmético) |
| `compressed` | uint32 | `1` = dados em zlib, `0` = dados crus |

A partir do `offset` indicado, os dados são **zlib puro** (assinatura `78 9c`), sem nenhum truque adicional — `zlib.decompress()` padrão funciona diretamente.

O arquivo `.jfslist` que acompanha cada `.jfs` é um objeto serializado via **.NET BinaryFormatter** contendo apenas nome do arquivo + data de modificação (metadado de build, não usado em tempo de execução pelo jogo — pode ser ignorado para extração/reempacotamento).

---

## 🗣️ Estrutura do `strings.bin`

O `strings.bin` (dentro de `gui.jfs`, hash `3190977537`) é uma tabela de localização multi-idioma. Formato (little-endian):

```
int32 totalCount
repete totalCount vezes:
    int32 keyLen
    bytes key[keyLen]              # ASCII, padding de espaços até múltiplo de 4
    int32 numLanguages
    repete numLanguages vezes:
        int32 langCodeLen
        bytes langCode[langCodeLen]  # ASCII ("US","FR","IT","DE","ES"), padding de espaços até múltiplo de 4
        int32 textLen                 # número de CARACTERES, não de bytes
        bytes text[textLen * 4]       # UTF-32 LE, um codepoint por 4 bytes
```

O jogo vem com 5 idiomas nativos: **US** (inglês), **FR**, **IT**, **DE**, **ES**. Não existe slot nativo para português — a tradução funciona **sobrescrevendo o conteúdo de um slot existente** (US ou ES, dependendo da versão baixada).

Total de entradas no arquivo original: **846** (844 com texto real, 2 são marcadores internos vazios sem conteúdo traduzível).

---

## 🌍 Sistema de seleção de idioma do jogo

O executável (`killteam.exe`) reconhece apenas 5 strings literais para idioma: `english`, `french`, `italian`, `german`, `spanish`, armazenadas/lidas via registro do Windows em `HKCU\Software\Sega\KillTeam`. Não há suporte nativo a um 6º idioma — por isso a estratégia de sobrescrever um slot existente em vez de tentar adicionar um novo.

O jogo detecta o idioma do sistema (`GetUserDefaultLCID`/`GetUserDefaultLangID`) e cai no padrão (inglês) quando o locale do Windows não corresponde a nenhum dos 5 suportados — o que faz a versão **US** funcionar automaticamente na maioria dos PCs configurados em Português do Brasil, sem precisar trocar nada no jogo.

---

## ⚙️ Placeholders preservados

Elementos dinâmicos do jogo que devem ser mantidos intactos em qualquer tradução:

- `%d`, `%s` — valores dinâmicos (inteiros e strings) inseridos em tempo de execução
- `{v:NomeDaVariavel}` — variáveis nomeadas (ex: `{v:PlayerName}`)
- `\n` — quebra de linha

**Atenção:** alterar ou remover esses elementos quebra a exibição do texto no jogo. Todas as 844 traduções foram validadas automaticamente para garantir que os placeholders do texto em português batem exatamente com os do texto original em cada chave.

---

## 🛠️ Ferramentas e scripts utilizados

- **monodis / mono-complete** — desmontagem do executável e de uma ferramenta .NET de extração do Juiced 2, para extrair o algoritmo de hash
- **Python 3** — todos os scripts de extração, parsing e reempacotamento
- **zlib** (biblioteca padrão Python) — (des)compressão dos dados internos do `.jfs`
- **Claude (Anthropic)** — engenharia reversa completa do formato + tradução de todos os 844 termos

Nenhuma ferramenta de terceiros (UABEA, AssetStudio, etc.) foi necessária — o formato do jogo não é baseado em Unity, então essas ferramentas não se aplicam aqui. Todo o pipeline de extração/reempacotamento foi escrito do zero.

---

## 📜 Scripts do projeto

- **`jfs_extract.py`** — extrai todos os arquivos de dentro de um `.jfs`, resolvendo nomes via hash
- **`parse_strings_bin.py`** — decodifica o `strings.bin` para JSON legível (todas as 846 entradas × 5 idiomas)
- **`encode_strings_bin.py`** — recodifica o JSON de tradução de volta para o formato binário, sobrescrevendo o idioma escolhido
- **`repack_jfs.py`** — substitui um arquivo dentro do `.jfs` original e recalcula cabeçalho/offsets de todo o pacote, preservando os demais 581 arquivos byte a byte intactos

---

## 🤝 Como contribuir

1. Faça fork do repositório
2. Edite o arquivo `killteam_ptbr.json` (formato `"CHAVE": "texto traduzido"`)
3. Rode `encode_strings_bin.py` + `repack_jfs.py` para gerar um novo `gui.jfs`
4. Teste no jogo
5. Abra um Pull Request

---

## 🌍 Criar tradução para outro idioma

O processo é o mesmo: escolha qual dos 5 slots (US/FR/IT/DE/ES) sobrescrever, gere o `killteam_<idioma>.json` com as traduções, e rode os mesmos dois scripts (`encode_strings_bin.py` + `repack_jfs.py`) apontando para o idioma escolhido.

---

## 📌 Histórico de versões

- **1.0.0** — Primeira versão pública. 844 termos traduzidos (100% do texto extraível do jogo).
