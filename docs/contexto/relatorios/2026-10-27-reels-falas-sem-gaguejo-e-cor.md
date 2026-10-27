# 27/10/2026 · Reels: todos os vídeos de 26/10 prontos, fala sem gaguejo e cor corrigida

## Pedido
"Faça os demais vídeos agora, me entregue todos prontos, tente errar menos nas falas, os erros e gagueiras ainda estão
aparecendo." Estilo escolhido: tela dividida. Durante a sessão: "cuidado com as cores", analisar o Reel de referência
(regra para viralizar) e preparar o tema do dia: assédio eleitoral, demissão por voto.

## Feito
- `producao/reels/motor/fala.py`: passada literal (`LITERAL`) e `gaguejos()` na montagem; `transferencia()` corrigida
  (a conversão HDR nunca rodava por causa de uma vírgula na saída do ffprobe). Testes em `test_fala.py` (28 passam).
- `producao/reels/motor-dividida/diagramas.py`: peças novas (linha do tempo, escudo, etapas, ficha com carimbo,
  vai e volta, sem salário, descanso), só na paleta café e dourado.
- Série 19: cortes revistos em `falas.py`, R1 v3 nos dois estilos, R2 na tela dividida, legenda do R2.
- Série 20 (VIDEO 2): `falas.py`, `serie_dividida.py`, `legendas.py`; 3 Reels.
- Série 21: `roteiro-gravacao.md` (assédio eleitoral) para a Dra. gravar.
- Contexto em `docs/CONTEXTO_PROJETO.md` (Série 19, item de 27/10, e Série 20); regra nova na skill `leticia-reels-premium`.

Entregues em `Desktop\NOVOS REELS`:
- VIDEO 1\PRONTOS: `contrato-intermitente-inteiro-v3-1.mp4`, `contrato-intermitente-dividida-v3-1.mp4`,
  `contrato-intermitente-dividida-2.mp4`.
- VIDEO 2\PRONTOS: `gestante-experiencia-dividida-1.mp4`, `limbo-previdenciario-dividida-2.mp4`,
  `intervalo-11-horas-dividida-3.mp4`.

## Verificado
- Transcrição literal de cada fala montada lida por inteiro; os avisos que sobraram são erro de escuta do Whisper
  (conferidos por energia e por emenda ouvida isolada), corrigidos só na legenda (`CORRIGE`).
- `conferir.py` sem avisos nos 6 arquivos (1080×1920, 30 fps, 11 Mbps, -19,7 a -19,9 LUFS, pico ≤ -1,2 dBTP).
- Fala montada em `bt709`; folhas de quadros revisadas (pele no tom real).
- Não verificado: ninguém assistiu com som; nada foi ao Orbit.

## Decisões e porquês
- Saiu do R2 o trecho "a maioria das empresas, grandes empresas, né": dito 15 a 25 dB abaixo da voz, sem corte limpo.
- Gestante: "Imagina você entrar no, pra trabalhar" virou "Imagina você trabalhar numa empresa" (emenda testada).
- Volume: os 4 Reels novos saíram entre -20,4 e -21,5 LUFS; ganho só no áudio, limitador ≤ 0,5 dB (regra: até 2 dB).
- Interjornada: uma pausa de 0,30 s ficou (limite 0,25) entre "descanso" e "então"; não refeito por prazo.
- Assédio eleitoral: tom neutro, sem partido nem candidato (OAB), apesar do pedido citar um lado.

## Pendente
- Jessica: assistir os 6 com som; decidir se sobem ao Orbit (R1 v3 nos dois estilos como Trial Reels).
- Dra.: gravar o roteiro da série 21; depois perguntar o estilo da edição.

## Próxima sessão
Se aprovados: passo 7 da skill `leticia-reels-premium` (backup, mídia, rascunhos com legenda de `legendas.py`).
Para a série 21: ler `producao/reels/series/21-assedio-eleitoral/roteiro-gravacao.md`.
