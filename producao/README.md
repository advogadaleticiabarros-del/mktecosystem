# Produção de conteúdo (fora do app)

Ferramentas de produção feitas à mão com o Claude, que não rodam dentro do Orbit mas alimentam o Editorial dele.
Só texto e código ficam aqui; vídeos, áudios, fotos e renders ficam em `C:\tmp\videos-reels\` (fora do git).

- `reels/motor/`: motor motion v2 dos Reels da Letícia (padrão oficial) + `narrar.py` (voz clonada no ElevenLabs).
  Uso: skill `leticia-reels-motion` (`.claude/skills/`). Testes: `cd producao/reels/motor && py -m pytest`.
- `reels/motor-v1/`: versão anterior, congelada para consulta.
- `reels/series/NN-nome/`: roteiro, `serie.py`, transcrição, legendas e scripts de subida de cada série já publicada.
- `reels/HISTORICO.md`: histórico dos pipelines de Reels (01 a 13).

Chaves nunca entram aqui: ElevenLabs em `C:\Users\prosy\.elevenlabs-leticia.json`, Pexels via `PEXELS_API_KEY`
ou pelo painel de chaves do Orbit.
