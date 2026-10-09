# Processo de produção de carrossel (playbook)

Versão de 08/10/2026. Origem: estudo "Carrosséis que Engajam", seção "Como produzir
melhor" (https://claude.ai/code/artifact/dabf1113-7a4b-4592-8ceb-5cd3a9bc44a0).
Regras de forma em `docs/MANUAL_CONTEUDO_REDES.md`; estratégia em
`docs/ESTRATEGIA_CRESCIMENTO_ORGANICO.md`.

Princípio: texto primeiro, arte depois, e a mesma fábrica para todos os carrosséis.

## Do tema ao post

1. **Roteiro antes da arte.** Escrever como texto: capa (número exato + palavra-chave),
   segunda capa (gancho que funciona sozinho, porque o Instagram reexibe o carrossel a
   partir do slide 2 para quem não deslizou), itens (uma ideia por slide), slide
   salvável (checklist, prazo, documentos) e fechamento (frase da Letícia + "salve e
   mande" + "procure uma advogada"). Se o roteiro não prende lido, a arte não salva.
2. **Fato conferido na fonte primária** (lei, decisão, data). Afirmação sem fonte
   confirmada sai do texto.
3. **Arte no modelo fixo do Orbit.** Hoje: `apps/api/_saida_producao_1510/carrossel_v3.py`
   (capa com foto inteira e título de alto contraste, foto em todo slide, números
   grandes, faixas douradas). Em construção: modelo editorial v4 (abaixo).
4. **Fotos.** Fotos reais da Letícia na capa e no fechamento (perfil do Instagram até a
   sessão de fotos); Pexels curado à mão para os slides de conteúdo. Nunca imagem de IA
   representando a Letícia; nunca foto com bandeira/urna/dinheiro estrangeiro, texto em
   inglês, marca de terceiro ou nudez.
5. **Legenda, primeiro comentário e música** (biblioteca comercial da Meta).
6. **Aprovação no Editorial e publicação automática.**

## Investimento de maior impacto

Sessão de fotos de meio dia: 40 a 60 fotos da Letícia no escritório (estudando,
atendendo, apontando, pensando, sorrindo), com espaço livre acima da cabeça para
título. Substitui a foto de banco nas capas.

## Pendências no Orbit

| Mudança | Por quê | Situação (08/10/2026) |
| --- | --- | --- |
| Modelo de carrossel dentro do render oficial (hoje em script) | Todo carrossel gerado sai no padrão aprovado | A fazer |
| Gerador escrever a segunda capa e o slide salvável | Segunda chance do algoritmo; salvamentos | A fazer (prompt) |
| Sugestão automática de fotos Pexels por slide, com escolha humana | Curadoria hoje é manual | A fazer; chave ligada |
| Publicar carrossel com vídeo misturado | Maior engajamento por post (Socialinsider) | A fazer; Graph API aceita vídeo em carrossel |
| Música | Carrossel com música pode ir para a aba Reels | Verificar API; senão pelo app |
| Teste A/B mensal | Decidir com dado do próprio perfil | Relatório na tela Crescimento |

## Testes A/B (próximas 4 semanas, um carrossel de cada)

Capa banco × foto real · só imagens × imagens + 1 vídeo de 5 s · sem × com música ·
7 × 10 slides. Medir alcance, visitas ao perfil, salvamentos, % até o último slide.

## Direção visual editorial (v4, pedido de 08/10/2026)

Referências aprovadas pela Letícia: carrosséis editoriais de advogadas (fundo papel com
textura, serifa com itálico de destaque, objetos e pessoas recortados vazando a borda,
linhas e arcos que atravessam os slides, cabeçalho discreto com nome e área, marca-texto,
número/letra gigante ao fundo). Tradução na identidade dela:

- Ritmo alternado: capa escura com foto recortada da Letícia → slides claros (areia com
  textura de papel) → slide escuro café → slide com foto → fechamento escuro.
- Cormorant Garamond (títulos, itálico no destaque) + Inter (texto), sempre com
  algarismos alinhados.
- Dourado para elementos (arcos, linhas, números gigantes, selos) e texto destacado só
  sobre fundo escuro. Em fundo claro o destaque é café itálico com sublinhado dourado
  (dourado sobre areia não tem contraste).
- Objetos recortados ligados ao tema (recorte feito na VPS em /root/recorte, rembg
  `isnet-general-use` para objetos e `u2net_human_seg` para pessoas).
- Carrossel renderizado como panorama contínuo (7 × 1080 px) e fatiado, para que arcos e
  recortes atravessem os slides.
- Faixas douradas de topo e rodapé em todos os slides (obrigatório).
