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
