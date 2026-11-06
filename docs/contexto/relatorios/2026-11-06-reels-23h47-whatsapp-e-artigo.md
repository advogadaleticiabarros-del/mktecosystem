# Relatório · Reels 23h47 (WhatsApp fora do horário) e artigo do blog (06/11/2026)

## Pedido
Jessica: "Poste esse já no perfil da Dra. Letícia, lembre-se SEO e para aparecer em pesquisas na IA. Crie também um
artigo para hoje e coloque na legenda que mais informações estão no artigo." Vídeo:
`producao/estilos/papel-e-ouro/motion-23h47/23h47-motion.mp4`. Depois do rascunho: "publica todos". Na escolha do
horário: "Trocar com o do 13º".

## Feito
- Artigo no ar: https://advogadaleticiabarros.com.br/blog/chefe-manda-mensagem-no-whatsapp-fora-do-horario-preciso-responder.html
  (corpo em `motion-23h47/artigo/artigo.html`, script `artigo/publicar_artigo.py`, capa = quadro 8,5 s do Reels).
  Ângulo novo (preciso responder? hora extra/sobreaviso?), com link para o artigo antigo de assédio moral digital.
- Reels agendado hoje 21h no Orbit (peça `e757b4bb-a9ff-484e-a1b1-f716e6ad7233`, agendamento `475601ca`), vídeo em
  `/app/media/reels-23h47-whatsapp.mp4`, legenda em `motion-23h47/legenda.json`, link do artigo no 1º comentário,
  `rotulo_ia: false` (só efeitos sonoros, sem narração). Script `subir_reels.py`.
- Os Reels do 13º desceram uma vaga (`trocar_reels_13.py`): 2/3 → 10/11, 3/3 → 13/11, proporcional → 17/11,
  4 regras → 20/11 (vaga que estava livre). Nada depois de 20/11 mudou.

## Verificado
- Artigo: 200, `article-hero` presente, `blog-grid` zero, FAQPage no schema, card no índice, URL no sitemap e no
  llms.txt, capa 200. Bing 200; IndexNow 403 (problema antigo da chave).
- Vídeo público responde 206 video/mp4. Lista de Reels conferida depois da troca.
- Backup do banco antes: `/root/orbit-backups/antes-reels-23h47.sql.gz`.

## Pendente
- Conferir às 21h15 se o Reels saiu (publicador automático).
- Search Console: Inspecionar URL > Solicitar indexação do artigo.
