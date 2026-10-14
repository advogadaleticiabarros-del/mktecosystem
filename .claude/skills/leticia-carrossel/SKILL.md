---
name: leticia-carrossel
description: Use quando for criar um carrossel de Instagram/Facebook (5 slides) para a Dra. Letícia Barros. Cobre escolha de fotos, dois estilos de template (Orbit padrão e squad-design), texto e agendamento.
---

# Carrossel da Letícia (5 slides, 1080×1350)

> **Regras obrigatórias:** `C:/Users/prosy/mktecosystem/docs/MANUAL_CONTEUDO_REDES.md` (OAB, Meta, specs, design system, checklist). Em conflito, o manual vence esta skill.


**Papel no funil do dia:** conteúdo da **tarde** — autoridade. Objetivo é
salvamento e visita ao perfil, não alcance bruto. Se a usuária estiver
montando o calendário do dia, esse é o formato do meio (depois da frase da
manhã, antes do Reels da noite) — ver
[[orbit-estrategia-crescimento-instagram]].

## 1. Fotos

- Se o tema tiver pasta própria em
  `C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\` (ex:
  `IDOSAS APOSENTADORIA E BEM ESTAR` pra aposentadoria/INSS/idosos, `BPC`
  pra BPC/LOAS/autismo), usar direto, sem perguntar de novo.
- Sem pasta própria: perguntar à usuária qual pasta/foto usar antes de
  gerar qualquer coisa.
- 1 foto diferente por slide (não repetir a mesma foto em sequência).
- **Regra fixa: o último slide (CTA "Procure uma advogada") sempre usa uma
  foto da própria Letícia**, da pasta
  `C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\Advogada`,
  nunca uma foto do banco genérico de tema. Pedido pela usuária em
  17/08/2026. Foto padrão usada até agora:
  `Gemini_Generated_Image_rrg4ylrrg4ylrrg4.png` (advogada em escritório,
  revisando documentos).
- **Checar cada foto de perto antes de aplicar**: nunca usar foto com marca
  de terceiro visível (logo de roupa, marca de produto) nem com dado
  pessoal de outra pessoa legível (nome em pulseira de hospital, etc.).
  Aconteceu em 17/08/2026: uma foto só foi reprovada depois de aplicada no
  render final, porque o logo (Ralph Lauren) só ficou visível com o
  overlay escuro do template por cima — vale reconferir a versão renderizada
  final, não só a foto crua, antes de considerar pronto.

## 2. Escrever o texto

- Voz sempre via skill `voz-leticia`.
- Nunca "deficiência" — trocar por "necessidades especiais".
- CTA do último slide é sempre impessoal: **"Procure uma advogada"** — nunca
  "Me chama", nunca oferta direta (viola ética OAB). Slides do meio: convite
  neutro "Arraste pro lado ›".
- **"Arraste pro lado ›" só nos slides 2-4, nunca no slide 5 (o último).**
  Erro cometido em 16/08/2026: os 13 carrosséis do calendário de agosto
  saíram todos com "Arraste pro lado ›" no slide final, o que não faz
  sentido (não tem próximo slide pra arrastar). O slide 5 fecha só com o
  texto decisivo + CTA, sem convite de arrastar.
- Cada slide: uma ideia curta. Slide 1 = a dor/gancho. Slides 2-4 = os
  direitos/fatos. Slide 5 = ponto decisivo + CTA.
- **Gancho do slide 1 precisa parar o dedo, não só explicar.** Evitar
  formato "Foi sancionada a lei X. O que muda de verdade?" (explicativo
  demais, baixo poder de parada — testado em 2026-07-30, resultado foi
  100+ visualizações mas **0 salvamentos e 0 compartilhamentos**). Preferir
  frases que geram curiosidade ou tensão: "O que ELES não estão te
  contando sobre [tema]", contraste direto, ou uma pergunta que a pessoa
  já está se fazendo, tipo "Isso vale pro seu caso agora?".
- **SEO/GEO:** repetir o termo de busca principal do tema não só na legenda,
  mas no texto do slide 1 (o gancho) — é o que aparece na capa do carrossel
  e o que o Instagram/Google indexam com mais peso visual.

## 3. Renderizar (dois estilos disponíveis — ofereça os dois se a usuária não tiver preferência clara)

**Estilo A — pipeline oficial do Orbit** (`render_criativo.py`,
`renderizar_slide`): mais simples, um bloco de texto por slide, foto de
fundo opcional. É o que o publicador automático do Instagram usa de verdade
(`instagram_publisher.py`) quando o carrossel nasce dentro do Orbit com
`content_piece_id` válido.

```python
from app.services.render_criativo import renderizar_slide
await renderizar_slide(
    texto="...", indice=i, total=5,
    identidade_visual=identidade_visual,  # de TenantConfig
    caminho_saida=str(caminho),
    foto_path=str(BANCO / "foto.jpg"),  # opcional
    foto_posicao="center top",  # ajustar conforme a foto
)
```

**Estilo B — squad-design** (`carrossel-4x5.html` em
`C:\tmp\blogautomaticoleticia\squads\@squad-design\criativos-estaticos\templates\`):
kicker + headline com destaque dourado (`<em>`) + texto de apoio — visual
mais forte, gancho mais editorial. Preferido quando a usuária achar o texto
do estilo A fraco/genérico (já aconteceu — ela pediu v2 nesse estilo em
2026-07-22). Renderizar via Playwright com substituição direta dos
placeholders `[IMAGEM_FUNDO]`, `[LOGO_SRC]`, `[PAGER]`, `[KICKER]`,
`[HEADLINE]`, `[TEXTO]`, `[FOOT]` (ver `_teste_aposentadoria_v2_gerar.py`
como referência de script, se ainda existir, ou recriar o padrão).

**Sempre**, nos dois estilos: aplicar o acabamento dourado fixo (barras de
gradiente topo/rodapé, `apps/api/app/assets/acabamento-dourado.png`,
composição via `Image.alpha_composite`) — regra de marca fixa, nunca
opcional. No estilo A isso já está embutido em `renderizar_slide`. No
estilo B, aplicar manualmente depois do screenshot.

## 4. Mostrar antes de publicar

Sempre mostrar os slides renderizados (pelo menos o 1 e o último) e a
legenda pra usuária aprovar antes de considerar pronto. Se ela disser que
não gostou do gancho/texto, oferecer uma v2 com copy diferente antes de
insistir na v1.

## 5. Legenda

Formato do squad `@softwarehouseexponencial/blog-escritor-seo`
(`C:\tmp\blogautomaticoleticia\squads\@softwarehouseexponencial\blog-escritor-seo`),
sempre usado pra legenda:
- Título com emoji no topo (`# 👵 Gancho da legenda`)
- Parágrafo de abertura com **negrito** nos termos-chave
- Subtítulos com `##` e emoji (ex: "⚖️ A regra que mudou em 2026:")
- Bullets com emoji-ícone (📌 💰 ✅) em vez de `-` simples
- Hashtags no final (3-5, específicas do tema, CamelCase; o Instagram limita a 5 desde 18/12/2025)

Os exemplos reais desse squad (`legenda-carrossel-1.md`/`-2.md` no root de
`blogautomaticoleticia`) têm CTA de oferta direta e tom de venda ("Fale com
a gente AGORA", "Não demore!") — **usar só a estrutura visual, nunca copiar
o tom**. CTA sempre impessoal ("procure uma advogada de confiança"), sem
travessão (—), sem "sem compromisso"/"grátis", sem "deficiência".

- **CTA de engajamento obrigatório, além do CTA jurídico.** Incluir sempre
  uma frase pedindo salvamento e/ou compartilhamento explicitamente, tipo
  "Salva esse post pra quando precisar" ou "Manda pra quem tá passando por
  isso agora". Confirmado em 2026-07-30: carrossel sem esse pedido
  explícito saiu com 0 salvamentos e 0 compartilhamentos mesmo em tema de
  alta relevância — é o maior alavancador desses dois sinais, que são os
  que mais importam pro papel de autoridade desse formato (ver seção 6).

## 6. Métricas a observar depois de publicado

Se a usuária pedir avaliação de desempenho, olhar: salvamentos,
compartilhamentos, % de pessoas que chegam até o último slide, e visitas ao
perfil geradas. Curtida sozinha não indica se o carrossel está cumprindo o
papel de autoridade/salvamento.

## 7. Agendar

Publicação de carrossel no Instagram ainda é manual (a usuária posta na
Meta). Registrar no Calendário do Orbit:

- `canal="instagram"`, `formato="carrossel"`
- `content_piece_id=None` (conteúdo fora do fluxo automático do Orbit —
  isso é seguro, o publicador automático pula silenciosamente qualquer
  agendamento sem `content_piece_id`)
- `data_agendada`/`horario` combinados com a usuária
- `status="pronto"`
