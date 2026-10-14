---
name: leticia-frase
description: Use sempre que a usuária digitar "frase" (ou pedir um card de frase de impacto). Formato tipográfico pensado pra compartilhamento — sem foto, só texto forte + assinatura.
---

# Frase de impacto (card tipográfico, 1080×1350, pensado pra compartilhar)

> **Regras obrigatórias:** `C:/Users/prosy/mktecosystem/docs/MANUAL_CONTEUDO_REDES.md` (OAB, Meta, specs, design system, checklist). Em conflito, o manual vence esta skill.


Criado em 2026-07-23 a pedido da usuária, especificamente pra engajamento/
compartilhamento — diferente das outras skills (que respondem uma pergunta
ou explicam um direito), aqui o objetivo é uma frase curta e validadora que
a pessoa reposta sem precisar clicar em nada. Gatilho: sempre que a usuária
digitar a palavra **"frase"**, usar esta skill.

**Papel no funil do dia:** conteúdo da **manhã** — compartilhamento.
Objetivo é a pessoa mandar pra alguém no direct/Stories, não autoridade nem
alcance frio. Ver [[orbit-estrategia-crescimento-instagram]].

## 1. A frase

- Curta (ideal até ~20 palavras) — cabe em 1-3 linhas grandes na tela.
- **Afirmação geral de direito/validação, nunca conselho de caso
  específico** — é uma declaração, não uma instrução (isso é o que a torna
  compartilhável, e também o que mantém dentro da ética OAB).
- Usa a técnica de **contraste** da voz da Letícia (marca #6 da skill
  `voz-leticia`): nomeia o que a pessoa pensa que é, e vira ao contrário.
  Ex: *"Pai não ajuda a criar o próprio filho. Ele cumpre uma obrigação."*
- Destacar em `<em>` a palavra/trecho que é o golpe decisivo da frase (fica
  dourado automaticamente no render).
- Se a usuária não trouxer a frase pronta, perguntar o tema/sentimento que
  ela quer validar antes de escrever (ex: mães cobrando pensão, mulher que
  teve demissão discriminatória, trabalhador que não sabe seus direitos) —
  não inventar tema sozinho.
- Nunca "deficiência" → "necessidades especiais" (regra geral de conteúdo).

## 2. Renderizar

```python
from app.services.render_criativo import renderizar_frase_impacto

await renderizar_frase_impacto(
    frase_html='Pai não ajuda a criar o próprio filho.<br>Ele cumpre <em>uma obrigação</em>.',
    identidade_visual=identidade_visual,  # de TenantConfig
    caminho_saida=str(caminho),
)
```

Template: `app/templates/frase_impacto.html` — aspas decorativas grandes,
frase centralizada em Playfair Display, `<em>` vira dourado, assinatura
(logo + "Letícia Barros" + OAB/ES 39.948) embaixo, moldura + acabamento
dourado já embutidos (mesma regra de marca do carrossel). Usar `<br>` na
frase pra controlar quebra de linha manualmente se o quebra automático
ficar estranho.

## 3. Legenda

Formato do squad `@softwarehouseexponencial/blog-escritor-seo` (título com
emoji, negrito, subtítulos com emoji, bullets com emoji, hashtags) — mesma
estrutura usada em `leticia-carrossel` e `leticia-criativo-pergunta`.
**Legenda completa e explicativa, não resumida** (a usuária corrigiu isso em
2026-07-27: mesmo o card sendo só a frase, a legenda precisa explicar o
direito por trás dela, com SEO/GEO de verdade — abrir validando o
sentimento, contexto jurídico explicado com 2-4 bullets, CTA impessoal no
final ("procure uma advogada de confiança"), hashtags).
- **SEO/GEO:** usar naturalmente os termos que a pessoa pesquisaria sobre o
  tema (não só sinônimos genéricos) — mesma lista de termos-base em
  [[orbit-estrategia-crescimento-instagram]].
- **CTA de engajamento obrigatório:** pedir explicitamente pra
  compartilhar/mandar pra alguém ou salvar — não deixar implícito. Ex:
  "Manda esse post pra quem precisa ouvir isso hoje" / "Salva pra não
  esquecer". Confirmado em 2026-07-30 (carrossel do mesmo dia sem esse
  pedido saiu com 0 compartilhamento e 0 salvamento).

## 4. Mostrar antes de publicar

Mostrar o card renderizado e a legenda pra usuária aprovar.

## 5. Métricas a observar depois de publicado

Compartilhamentos em Stories, comentários, e alcance entre não-seguidores —
esses três indicam se a frase está cumprindo o papel de compartilhamento.
Curtida sozinha não é o sinal certo pra esse formato.

## 6. Agendar

`canal="instagram"`, `formato="post"`, `content_piece_id=None`,
`status="pronto"`, data/horário combinados com ela.
