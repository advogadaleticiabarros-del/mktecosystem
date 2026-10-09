# Auditoria do perfil @adv.leticiabarros2 (09/10/2026)

Método: skill `instagram-marketing` → `ig-profile-optimizer` (9 partes do perfil), com os
dados lidos pela Graph API do Orbit, filtrada pelas regras da OAB
(`docs/MANUAL_CONTEUDO_REDES.md`). Meta da usuária: crescer em média 30 seguidores/mês.

Estado em 09/10/2026: 415 seguidores, 443 seguindo, 298 posts.

## Placar

| # | Parte | Situação | Por quê |
|---|---|---|---|
| 1 | Foto de perfil | Conferir no app | A API não avalia; precisa ser rosto grande, fundo limpo, contraste alto |
| 2 | Campo NOME (o que a busca do Instagram indexa) | **Refazer** | "Advogada \| Direito Trabalhista, Direito das Gravidas e Famílias": sem o nome dela, longo, "Gravidas" sem acento |
| 3 | @ | Ok | adv.leticiabarros2 (o "2" é herança; não vale trocar agora) |
| 4 | Bio | **Refazer (OAB)** | "Atendimento humano, exclusivo e personalizado / 📲 Fale comigo ⬇": "fale comigo" é oferta direta (vetada), e a bio não diz o que ela publica nem para quem |
| 5 | Link | Melhorar | Página inicial do site; para crescer, o link deve levar ao conteúdo (blog/série) |
| 6 | Categoria | Conferir | Usar "Advogado(a)" |
| 7 | Destaques | Conferir | Proposta abaixo (4 a 6, na ordem da próxima pergunta de quem chega) |
| 8 | Grade (9 primeiros) | Ok desde out/2026 | Identidade café e dourado consistente |
| 9 | Fixados (até 3) | **Definir** | Usar as melhores provas (abaixo) |

## Antes → depois

**NOME** (até ~30 caracteres visíveis; leva a palavra que as pessoas pesquisam):
- Antes: `Advogada | Direito Trabalhista, Direito das Gravidas e Famílias`
- Depois (recomendado): `Letícia Barros | Advogada Trabalhista`

**Bio** (até 150 caracteres; sem oferta de serviço, sem "especialista"):

Opção A (posicionamento gestante, regra da usuária de 31/07/2026):
```
A advogada da gestante trabalhadora.
Direito do Trabalho e de Família sem juridiquês.
Vitória/ES · OAB/ES 39.948
👇 Artigos no blog
```

Opção B (mais ampla):
```
Seus direitos no trabalho, na gravidez e na família, explicados sem juridiquês.
Vitória/ES · OAB/ES 39.948
👇 Artigos no blog
```

**Link:** blog (`advogadaleticiabarros.com.br/blog`) ou uma página de links com blog + série
da gestante. Evitar página com oferta de consulta.

**Destaques** (capas no padrão café e dourado, nomes curtos): Comece aqui · Gestante ·
Trabalho · Família · Na TV · Dúvidas.

**Fixados:**
1. Vídeo da TV Tribuna sobre a licença-maternidade adotiva (25/09): melhor desempenho
   recente (45 curtidas, 9 comentários) e prova de autoridade.
2. Reel 1/3 da série da gestante (quando publicado): diz para quem é o perfil.
3. Carrossel "pensão de R$ 300" (10/10) ou o post de família que mais salvar.

**Extra:** seguir mais contas do que tem seguidores (443 × 415) passa sinal fraco; reduzir
aos poucos, sem pressa.

## Teste do cabeçalho

Lendo só foto + NOME + bio + link + primeira linha da grade, uma gestante de Vitória
entende em 3 segundos que ali tem os direitos dela explicados, e que é uma advogada
real (nome + OAB)? Com as mudanças acima, sim.

## O que foi aplicado no Orbit

`REGRAS_LEGENDA` em `apps/api/app/routers/content.py`, presente em todo prompt que
gera legenda: gancho nos 125 caracteres antes do "mais", um único convite de salvar ou
enviar, 3 a 5 hashtags dimensionadas (nicho + área + local), nada inventado e lista de
marcas de texto de IA. A skill está instalada no projeto (`skills-lock.json`).
