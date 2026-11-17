# Série 23 · Dois Reels da Dra. sobre contrato intermitente (16-17/11/2026)

## Pedido
Jessica, com os vídeos `Desktop\NOVOS REELS\3\IMG_2092.MOV` e `IMG_2093.MOV`: "faça esses dois Reels da Dra. Letícia, cada
um é um tema, não mexa no som nem na qualidade da imagem, faça todas as animações e deixe o vídeo dinâmico, com cenas,
gancho inicial com efeito (mesmo que a cena se repita), efeito sonoro; pesquise como viralizar no nicho". Depois: "me dê
uma página da web para enviar para a Dra. Letícia aprovar". Estilo escolhido por ela: inteiro com banco.

## Feito
- R1 "Intermitente: o 13º já vem na diária" (63,6 s) e R2 "Intermitente de fachada" (91,5 s), em
  `C:\tmp\videos-reels\23-reels-3\intermitente-13-na-diaria-1.mp4` e `intermitente-de-fachada-2.mp4` (fora do git).
- Roteiros em `producao/reels/series/23-novos-reels-3/`: `falas.py` (cortes e base legal no docstring), `falas_r2.py`,
  `serie.py` (cenas), `legendas.py` (legenda, primeiro comentário, data), `pagina.py` (página de conferência),
  `creditos-pexels.txt`.
- `producao/reels/motor3d/clip3d.py`: novos clipes `livro` e `cofre9`.
- Página para a Dra.: https://claude.ai/artifact/BjkSFXaZPJKA9GahNRJbXp (vídeos em prévia de 720p, legenda, comentário,
  cortes). É privada: a Jessica precisa compartilhar pelo menu Share.
- Espaço em disco: com autorização da Jessica, apaguei os intermediários (quadros, áudio, seq, mídia, vídeos de trabalho)
  das pastas `C:\tmp\videos-reels\13, 17, 18, 19, 20`; MP4 finais e roteiros ficaram. O C: tinha 0,5 GB livres.
- Registro em `docs/CONTEXTO_PROJETO.md` (seção Série 23).

## Verificado
- `fala.py montar` sem emenda com problema (o que sobrou no relatório são trocas do Whisper, corrigidas na legenda).
- Cor BT.709 nas falas montadas; `serie.py --checar`: área limpa ok nos dois.
- `conferir.py`: sem avisos nos dois (1080x1920, 30 fps, 11 Mbps, -17,2/-17,3 LUFS, pico -1,9/-1,7 dBTP).
- Folhas de 10 quadros revisadas uma vez.
- Não verificado: escuta humana com som (a Jessica e a Dra. precisam assistir).

## Decisões e porquês
- Fala jurídica corrigida por corte, sem regravar: saíram "FGTS na diária" (é depositado, art. 452-A §8º), "não tem
  direito a férias" (§9º) e "nada mais vai receber". A tela mostra o FGTS depositado à parte.
- Gancho = frase forte da própria Dra. que volta depois na fala (pedido dela), com zoom, título e carimbo.
- Rosto baixo e perto nesta gravação: vídeo sobe 220/110 px e textos de rosto ficam numa linha em y=985.
- Banco: só clipes já no disco; a busca no Pexels pelo Orbit precisa de SSH, que o modo automático bloqueou.
- Volume em -17 LUFS (o motor baixa quando há picos fortes, para não comprimir a voz; a regra aceita até -20).

## Pendente
- Aprovação da Dra. pela página (Jessica envia).
- Capa no padrão "Domingo com a Dra." (retrato real sentada em quadro 3D) e envio ao Orbit como rascunho: dom 22/11
  (R1) e dom 29/11 (R2) às 15h30. Precisa do SSH da VPS liberado.

## Próxima sessão
Depois do "aprovado": skill `leticia-reels-premium` passo 7 (backup do banco, mídia em `api:/app/media`, peças em
rascunho com `legendas.py`), capa com `capas_dra.py`.
