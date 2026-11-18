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

## Versões B (17/11/2026, manhã)
- Pedido: "Mantenha esses dois vídeos, ficaram bons! Mas parece o mesmo. O vídeo 1 é o que é o trabalho intermitente, o 2
  é estudo de caso, não chegou nenhum cliente, é fictício, então pode fazer também. [...] No final escolhemos qual utilizar."
- Feito: R3 `o-que-e-o-intermitente-3.mp4` (70 s) e R4 `intermitente-estudo-de-caso-4.mp4` (84,7 s) na mesma pasta; as
  versões A ficaram intactas. Cortes em `falas_v2.py` e `falas_v2_r4.py`, cenas `reel3`/`reel4` em `serie.py`, legendas
  3 e 4 em `legendas.py` (mesmas datas das versões A que substituem), página refeita com as quatro versões agrupadas por
  vídeo (mesmo link).
- Verificado: `fala.py montar` (os avisos que sobraram são os mesmos trocados do Whisper aceitos na versão A), cor
  BT.709, `--checar` ok, `conferir.py` sem avisos nos dois (-17,6 e -17,0 LUFS, pico -1,9 e -1,6 dBTP, 11 Mbps), folhas
  de quadros revisadas; o R3 foi renderizado de novo porque um rótulo do relógio caía sobre a legenda. Não verificado:
  escuta com som.
- Decisões: o atendimento do R3 entrou porque a Jessica disse que é fictício; no R4 a tela diz "situação hipotética"
  (a própria Dra. fala "vamos colocar 3, 4 anos"). O "danoso" continua fora (contradiz o "não tira direitos").

## Reels de teste (17/11/2026)
- Pedido: "Em primeiro momento, vamos postar no Reels teste. Todos, e depois vamos escolher 2 ou 3 para postar na grade."
- Feito: backup do banco (`antes-testes-serie23-20261117-1007.sql.gz`, 1,5 MB), 4 MP4 em `api:/app/media`, 4 peças
  Trial Reels com graduação MANUAL agendadas para 17/11 (09:30, 11:30, 14:30, 16:30) por
  `producao/reels/series/23-novos-reels-3/subir_testes.py`.
- Verificado: o script imprimiu os 4 agendamentos; as 4 URLs de mídia respondem 206 (pedido parcial ok). Não verificado
  ainda: a publicação na Meta (acontece nos horários).

## Seção "Reels de teste" no Desempenho (17/11/2026)
- Pedido: "Se o Orbit não está coletando, precisamos de uma seção de Reels de teste lá, para sabermos do desempenho
  desses Reels" e "para os próximos".
- Diagnóstico: o Orbit já coleta o teste (ele vem na lista `/media` da Meta). O de 27/10 (id 18117094946119300) tem
  0 visualizações e 0 de alcance também quando lido direto da Meta, campo a campo, sem erro: ou o teste não foi
  entregue, ou a API não conta as visualizações de teste. Só o app do Instagram tira a dúvida.
- Feito (commit `95793f2`): seção "Reels de teste" na tela Desempenho (`services/desempenho.py`, `_reels_teste`):
  cada teste dos últimos 60 dias com visualizações, alcance, envios, salvos, curtidas, tempo médio e a situação
  (agendado, aguardando coleta, menos de 24 h, 0 visualizações, vai bem ou abaixo da meta), mais a meta (70% da
  mediana dos últimos 10 Reels do feed ou 3 envios + salvamentos). `teste_reels.views_referencia` tira os testes da
  referência (antes o teste zerado puxava a mediana para baixo, inclusive na liberação automática da grade).
- Verificado: 401 testes passando (4 novos).
- Deploy em 18/11/2026 (pedido "publica"): backup `/root/orbit-backups/antes-secao-reels-teste-20261118-1238.sql.gz`
  (1,6 MB), API refeita com `95793f2`. Em produção, `montar_desempenho` devolveu a seção com os 5 testes (os 4 da série
  23 e o de 27/10) e meta de 50 visualizações. Os horários saíam em UTC (12:31 em vez de 09:31): corrigido para o
  horário de Brasília (`FUSO_PADRAO`), com teste, e publicado de novo.
- Números em 18/11 (menos de 24 h para três deles): 2A com 1 visualização; 1A, 2B e 1B com 0. O 1B já passou de 24 h
  com 0, como o teste de 27/10.

## Pendente
- Conferir no app do Instagram se o teste de 27/10 teve visualizações (decide se a API conta os testes).
- Escolher 2 ou 3 para a grade pelo desempenho dos testes (e pela Dra.).
- Capa no padrão "Domingo com a Dra." (retrato real sentada em quadro 3D) para os escolhidos, e peças da grade como
  post novo.

## Próxima sessão
Ver a seção Reels de teste no Desempenho depois de 24 h dos testes; para os escolhidos, skill `leticia-reels-premium`
passo 7 e capa com `capas_dra.py`.
