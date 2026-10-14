---
name: leticia-criativo-pergunta
description: Use quando a usuária pedir um "criativo pergunta" (imagem única de Instagram, formato "Me faça uma pergunta") para a Dra. Letícia Barros. Cobre escolha de tema, foto e legenda SEO.
---

# Criativo "Me faça uma pergunta" (imagem única, 1080×1350)

> **Regras obrigatórias:** `C:/Users/prosy/mktecosystem/docs/MANUAL_CONTEUDO_REDES.md` (OAB, Meta, specs, design system, checklist). Em conflito, o manual vence esta skill.


Formato mais usado no Instagram real dela (@adv.leticiabarros2). Template
validado (foto sem fundo + selo dourado + balão de pergunta + perfil) em
`_teste_pergunta_squad_gerar.py` (protótipo — ainda não é pipeline oficial
do Orbit, é gerado por script pontual). Sempre seguir esta ordem, sem pular
etapa, mesmo que a usuária peça de forma resumida:

**Papel no funil do dia:** conteúdo de **relacionamento**, junto com a frase
de impacto (ver [[orbit-estrategia-crescimento-instagram]]) — objetivo é
comentário e conversa, não autoridade nem alcance frio. Pode ocupar o
horário da manhã como alternativa à frase, ou um horário próprio de
relacionamento à parte, dependendo do que a usuária combinar pro dia.

## 1. Tema

Se a usuária não trouxe o tema pronto, oferecer **10 sugestões** de
pergunta/assunto, checando o que já foi coberto recentemente (blog, outros
criativos, carrosséis) pra não repetir tema nem redação. Formato da
pergunta: direta, primeira pessoa, como a pessoa realmente perguntaria
("Fui demitida. Até quando posso processar a empresa?").

## 2. Foto

Depois que ela escolher o tema, **pedir o caminho da foto sem fundo** (PNG
recortado) que combina com a pergunta escolhida — nunca gerar nem supor,
a usuária indica o arquivo. Se o tema tiver banco de fotos próprio (ex:
`IDOSAS APOSENTADORIA E BEM ESTAR` pra aposentadoria), pode sugerir de lá,
mas a escolha final da foto específica é dela.

## 3. Renderizar

Elementos fixos do template (não inventar layout novo):
- Fundo dourado texturizado + marca d'água diagonal do selo
- Foto sem fundo, recortada, canto inferior direito, sombra sutil
- Selo circular dourado (logo) no topo — usar
  `C:\Users\prosy\Desktop\PROJETOS\modelo-visual-site\assets\logo\logo-800x800.png`
  (trocado em 2026-08-16 pelo pedido da usuária, "vai aparecer mais" —
  substitui o antigo `apps/api/app/assets/logo-leticia.png`)
- Balão de pergunta: topo "Me faça uma pergunta:" + corpo com a pergunta
- Rodapé: avatar + `@adv.leticiabarros2` + verificado + especialidade
- Acabamento dourado fixo (barras topo/rodapé,
  `apps/api/app/assets/acabamento-dourado.png`) por cima do render final
- **`.conteudo` sempre alinhado ao topo** (`padding: 108px 96px 0`, sem
  `justify-content: center`), nunca centralizado verticalmente — mesmo
  quando a foto ainda não foi definida e a peça for gerada só com
  selo+balão+rodapé, é preciso sobrar espaço vazio na parte inferior pra
  colocar a foto depois sem precisar re-renderizar o resto.

## 4. Legenda (SEO, respondendo a pergunta)

Voz sempre via skill `voz-leticia`. Formato do squad
`@softwarehouseexponencial/blog-escritor-seo` (título com emoji, negrito,
subtítulos com emoji, bullets com emoji, hashtags) — ver skill
`leticia-carrossel` seção 5 pra estrutura exata. Não é o mesmo texto do
balão da imagem — a legenda responde a pergunta de verdade, otimizada pra
SEO (palavras-chave que alguém buscaria no Google/Instagram sobre o tema).

Regras inegociáveis:
- Nunca "deficiência" → "necessidades especiais"
- Nunca travessão (—) na legenda
- CTA sempre impessoal: **"Procure uma advogada de confiança"** — nunca
  "me chama", "sem compromisso", "fale comigo", nenhuma oferta direta
  (ética OAB)
- **CTA de engajamento obrigatório**, além do jurídico: puxar comentário de
  verdade, tipo "me conta nos comentários se isso já aconteceu com você" ou
  "manda sua pergunta que eu respondo no próximo post" — é o que gera o
  sinal de conversa que é o objetivo desse formato (ver seção 6).

## 5. Mostrar antes de publicar

Mostrar a imagem renderizada e a legenda pra usuária aprovar antes de
considerar pronto.

## 6. Métricas a observar depois de publicado

Comentários, respostas em DM e perguntas novas recebidas — é o sinal de que
o formato está gerando a conversa que é o objetivo dele.

## 7. Agendar

Publicação ainda é manual (a usuária posta na Meta). Registrar no
Calendário do Orbit: `canal="instagram"`, `formato="post"`,
`content_piece_id=None`, `status="pronto"`, data/horário combinados com
ela.
