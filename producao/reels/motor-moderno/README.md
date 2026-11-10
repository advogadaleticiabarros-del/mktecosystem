# Motor moderno (10/11/2026) — Reels com a Dra. gravando, estilo inteiro

Cópia do `../motor/` (que fica intacto), feita a pedido da Jessica: "os Reels em que a Dra. grava estão feios e mal
editados... mais moderno, com motions mais legais, transição de cenas de ângulos diferentes, mesclagem de imagens sobre o
assunto com a imagem da Dra.". Piloto: Limbo previdenciário 1/2 (`C:	mpideos-reels8-limbo-previdenciario\moderno\`).

O que muda em relação ao motor premium:
- **Ângulos de câmera** (`motor.angulos`): cada emenda no rosto troca o ângulo (close, lateral esquerda, médio, lateral
  direita), com assentamento de 0,3 s. `bg["ang"]` fixa um ângulo na cena ("lado"/"ladoD" abrem espaço para uma janela).
- **Janela 3D** (`motor.janela`): vídeo num cartão com borda de ouro metálico e reflexo, entrando com giro 3D e flutuando.
  Serve para a Dra. sobre o vídeo do assunto (`rosto=True`, `desde`=início da cena para a boca bater com a voz, `zoom`
  ~1,75 no rosto) e para o assunto ao lado dela.
- **Títulos palavra por palavra** (`anim="palavras"`).
- **Legenda curta e maior** (`CFG["leg_max"]` = 16 caracteres, 58 px), só a palavra falada num selo dourado.
- **Transições** `zoomblur` e `giro` (3D), com efeito sonoro.
- Rosto da Dra. continua sem filtro nem grão, inclusive dentro da janela.

Recorte da Dra. (tirar o fundo): testado com rembg (u2net, u2net_human_seg, isnet) e reprovado: o cabelo sai junto com a
estante ou é cortado. Por isso a mistura é feita com janelas, sem recorte.

---

# Padrão oficial de Reels — motion v2 procedural (10/10/2026)

Base da série "13º sem susto" (pasta 13). Para cada vídeo novo, copiar esta pasta para `NN-nome/work/` e seguir a skill
`leticia-reels-motion` (`~/.claude/skills/leticia-reels-motion/SKILL.md`).

- `motor.py`: motor genérico (áudio, energia da voz, legenda, blocos, pó de ouro, verificador, render, codificação). Não muda por série.
- `serie.py`: roteiro da série (CFG, trechos, cenas). É o único arquivo que muda.
- `engine.html` + `fx.js`: visual e camada procedural (pó de ouro, explosões, soco, tinta, luz, verificador da área limpa).
- `transcrever.py`: Whisper com marcação de palavras (para áudio enviado).
- `narrar.py`: roteiro → voz clonada da Letícia no ElevenLabs + transcricao.json exata (padrão desde 14/10/2026). Testes: `py -m pytest test_narrar.py`.

Padrão premium (21/10/2026, skill `leticia-reels-premium`): sem trilha nem ambiência (virou chiado), uma entrega por vídeo, voz original (só ganho), -14 LUFS (menos se os picos exigirem corte > 2 dB) / -1 dBTP,
H.264 a 11 Mbps, efeitos com 3 a 4 variações sorteadas com semente fixa (`REELS[n]["semente"]`, padrão 20+n)
e punch-in alternado nas emendas do rosto (cenas com `"rosto": True` no bg).
- `fala.py`: `py fala.py transcrever <bruto>` e `py fala.py montar <falas.py> [n]` (pausas reais, fusão de 20 ms,
  retranscrição de cada trecho; grava fala-rN.mp4/.wav/.emendas.json/.transcricao.json). Rodar até "fala ok".
- `conferir.py`: `py conferir.py <mp4> [cfg_rN.json]` (congelamento, volume, formato, cenas longas, folha de 10 quadros).
- Testes: `py -m pytest` (test_fala, test_conferir, test_motor, test_narrar).

Comandos: `py serie.py --checar` → `py serie.py 1 --amostras` → `py serie.py 1 2 3`.
A versão anterior (v1, série "Direitos da gestante") está congelada em `../_padrao-motion-v1/`.
