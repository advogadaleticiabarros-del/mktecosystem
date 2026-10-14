# Padrão oficial de Reels — motion v2 procedural (10/10/2026)

Base da série "13º sem susto" (pasta 13). Para cada vídeo novo, copiar esta pasta para `NN-nome/work/` e seguir a skill
`leticia-reels-motion` (`~/.claude/skills/leticia-reels-motion/SKILL.md`).

- `motor.py`: motor genérico (áudio, energia da voz, legenda, blocos, pó de ouro, verificador, render, codificação). Não muda por série.
- `serie.py`: roteiro da série (CFG, trechos, cenas). É o único arquivo que muda.
- `engine.html` + `fx.js`: visual e camada procedural (pó de ouro, explosões, soco, tinta, luz, verificador da área limpa).
- `transcrever.py`: Whisper com marcação de palavras (para áudio enviado).
- `narrar.py`: roteiro → voz clonada da Letícia no ElevenLabs + transcricao.json exata (padrão desde 14/10/2026). Testes: `py -m pytest test_narrar.py`.

Comandos: `py serie.py --checar` → `py serie.py 1 --amostras` → `py serie.py 1 2 3`.
A versão anterior (v1, série "Direitos da gestante") está congelada em `../_padrao-motion-v1/`.
