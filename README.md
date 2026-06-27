# Warhammer 40,000: Kill Team — Tradução PT-BR

> Tradução não-oficial completa do jogo para o Português do Brasil.

---

## 📋 Sobre o projeto

Este projeto, assim como sua documentação, foi feito inteiramente com o uso da plataforma CLAUDE — incluindo toda a engenharia reversa do formato de arquivos do jogo, sem uso de nenhuma ferramenta de terceiros.

Este projeto traduz **844 termos** do jogo Warhammer 40,000: Kill Team (2011/port PC 2014) para o Português do Brasil, cobrindo **100% dos textos visíveis do jogo**:

- Briefings e objetivos de todas as 5 missões da campanha
- Interface completa (menus, HUD, opções, telas de seleção)
- Codex/Lexicon (lore de todas as unidades: Space Marines, Orks, Tyranids)
- Armas, classes, perks e power-ups
- Killstreaks e estatísticas
- Conquistas (Steam/Xbox/PSN)
- Textos legais e diálogos de sistema (save/erro)

**Versão do jogo testada:** Steam (port PC, build D3T 2014)
**Plataforma:** PC (Steam)

---

## ✅ O que foi traduzido

| Categoria | Termos (aprox.) | Descrição |
|---|---|---|
| UI (menus, HUD, opções) | ~390 | Interface completa do jogo |
| Codex/Lexicon | 50 | Lore de todas as unidades |
| Diálogos de sistema (save/erro) | ~150 | Mensagens de save, erro, perfil |
| Missões (briefings + objetivos in-game) | 118 | Texto de todas as 5 missões |
| Killstreaks / Estatísticas | 60 | Nomes de sequência de abates e telas de stats |
| Armas / Classes / Perks / Pickups | ~80 | Nomes de armas, perks, itens coletáveis |
| Leaderboards (nomes gerados) | 35 | Nomes das classificações online |
| Conquistas (Steam/Xbox/PSN) | 24 | Nome e descrição de cada conquista |
| Capítulos (nomes, descrições, motes) | 18 | Telas de seleção de Capítulo |
| Textos legais | 10 | Copyright, licenças de terceiros |
| **Total** | **844** | **100% do texto extraível do jogo** |

### Termos mantidos em inglês/latim/dialeto Ork (intencionalmente)

Termos canônicos do universo Warhammer 40K, nomes de Capítulo, e o dialeto Ork (a forma como os próprios Orks "escrevem errado" no universo) foram preservados no idioma original:

`Imperium`, `Adeptus Astartes`, `Codex Astartes`, `Exterminatus`, `Warp`, `Bolter`, `Aquila` — termos latinos/lore.
`Blood Ravens`, `Ultramarines`, `White Scars`, `Imperial Fists`, `Blood Angels`, `Salamanders` — nomes de Capítulo.
`Kroozer`, `Warboss`, `Boyz`, `Nobz`, `Choppa`, `Shoota`, `Stikk Bomma`, `Tankbusta`, `Burna Boy`, `Stormboy`, `Weirdboy`, `Teleporta`, `Orkdom`, `Orkiness` — dialeto/jargão Ork.
`Genestealer`, `Carnifex`, `Hive Tyrant`, `Hormagaunt`, `Termagant`, `Ripper Swarm`, `Hive Fleet` — termos Tyranid.

---

## Como foi traduzido?

Para detalhes técnicos completos, leia [`COMO_FUNCIONA.md`](COMO_FUNCIONA.md).

Resumo: o Kill Team usa um formato de arquivo proprietário chamado **JFS** (herdado da engine interna "JET", usada também em *Juiced 2: Hot Import Nights*). Não existia nenhuma ferramenta pública capaz de ler esse formato no port de PC — toda a engenharia reversa (algoritmo de hash dos nomes de arquivo, estrutura do contêiner `.jfs`, e o formato binário multi-idioma `strings.bin`) foi feita do zero com auxílio da CLAUDE, desmontando o executável e validando byte a byte contra os arquivos reais do jogo.

A tradução em si foi feita pela própria CLAUDE, lote por lote, com atenção a manter consistência terminológica do universo Warhammer 40K e preservar todos os placeholders de variável (`%d`, `%s`, `{v:Nome}`) intactos.

---

## 🛠️ Como instalar

### Pré-requisitos

- Jogo instalado via Steam

Diferente de outras traduções de jogos Unity, **não é necessário nenhuma ferramenta externa** — o arquivo já vem pronto para substituir diretamente.

### Passo a passo

**1. Faça backup do arquivo original**

```
Copie o arquivo:
...\SteamLibrary\steamapps\common\W40K Kill Team\gui.jfs

Para uma pasta segura antes de continuar.
```

**2. Baixe o arquivo de tradução**

Baixe o arquivo `gui_US.jfs` da seção [Releases](../../releases) deste repositório.

**3. Substitua o arquivo**

- Renomeie `gui_US.jfs` para `gui.jfs`
- Coloque na pasta:
```
...\SteamLibrary\steamapps\common\W40K Kill Team\
```
- Confirme a substituição

**4. Jogue!**

- Abra o jogo normalmente pelo Steam
- Os textos aparecerão automaticamente em **Português do Brasil**, pois o jogo geralmente cai no idioma padrão (inglês/US) quando o Windows está em PT-BR — slot que sobrescrevemos.
- Se o seu jogo carregar em outro idioma (francês, italiano, alemão, espanhol) em vez de inglês, vá em **Help & Options → PC Options → Language** dentro do próprio jogo e selecione **English**.

### Alternativa: versão Espanhol

Caso o seu jogo, por alguma configuração, sempre force outro idioma e o inglês não funcione, há uma segunda versão (`gui_ES.jfs`) que sobrescreve o slot de **Espanhol** em vez do de Inglês. Nesse caso, depois de trocar o arquivo, selecione **Spanish** no menu de opções do jogo.

---

## 🔄 Como desinstalar / restaurar

Para voltar ao inglês original, basta restaurar o backup:

1. Feche o jogo
2. Copie o `gui.jfs` original de volta para a pasta do jogo
3. Confirme a substituição

---

## ⚠️ Avisos

- Esta é uma tradução **não-oficial** — não tem relação com a d3t, Nomad Games, Relic Entertainment, SEGA ou Games Workshop
- Testada na versão atual disponível na Steam
- Esta tradução sobrescreve o slot de idioma Inglês (US) ou Espanhol (ES) do jogo — os demais idiomas (Francês, Italiano, Alemão, e o outro slot não usado) permanecem 100% intactos e no original
- Se o jogo atualizar e a tradução parar de funcionar, restaure o backup e aguarde uma atualização deste projeto

---

## 🐛 Reportar erros

Encontrou um erro de tradução, texto cortado ou algo que não faz sentido em PT-BR? Abra uma [Issue](../../issues) com:

- Print da tela com o erro
- Contexto (qual missão, menu, tela)
- Sugestão de tradução correta (opcional)

---

## 🔧 Para desenvolvedores

Quer contribuir com melhorias ou criar uma tradução para outro idioma? Veja o arquivo [COMO_FUNCIONA.md](COMO_FUNCIONA.md) para entender a estrutura técnica completa do projeto, incluindo o algoritmo de hash, o formato do contêiner `.jfs` e o formato do `strings.bin`.

---

## 📜 Licença

Este projeto está licenciado sob a MIT License.

Você pode usar, modificar, distribuir e até utilizar comercialmente este projeto livremente.

Warhammer 40,000: Kill Team © d3t Limited / Nomad Games Limited / Relic Entertainment / SEGA. Warhammer 40,000 © Games Workshop.
Este projeto é uma tradução não-oficial e não possui vínculo com os detentores da propriedade intelectual.
