---
name: leticia-seo-local
description: Use quando a usuária pedir para "rankear melhor", "aparecer no Google", falar de SEO/GEO, ou quando for hora do checklist mensal de SEO local. Cobre Google Business Profile, títulos/meta das páginas e backlinks — não é sobre velocidade técnica do site (isso é outra frente, já tratada à parte).
---

# SEO local da Letícia Barros — checklist periódico

Criado em 05/08/2026, depois de investigar por que
`advogadaleticiabarros.com.br` não aparecia para "advogado trabalhista"
mesmo com o site tecnicamente saudável (rápido, sem erros de
acessibilidade, todas as páginas de área publicadas). Descoberta: **o
gargalo não é técnico, é de autoridade/histórico** — tempo de existência
do domínio e do perfil, volume de avaliações, backlinks. Isso não se
resolve com ajuste de código, é construção ao longo do tempo. Esta skill
existe pra transformar isso num processo repetível em vez de reinvestigar
do zero a cada conversa.

## Quando rodar

Sugestão: **1x por mês**, ou sempre que a usuária perguntar "por que não
apareço no Google" / "como ranquear mais". Rodar o checklist inteiro leva
uns 20-30 minutos.

## 1. Google Business Profile (o que mais pesa em busca local)

Acesso: business.google.com, perfil "Letícia Barros | Advocacia para
Gestantes e Trabalhadores" (já verificado, 5,0 estrelas).

- [ ] **Eficácia do perfil** (círculo no topo do painel) — se não estiver
      quase cheio, clicar em "Preencha as informações" e resolver o que
      pedir (geralmente foto ou dado faltando).
- [ ] **Avaliações**: comparar quantidade com concorrentes que aparecem no
      topo da busca-alvo (ver seção 4). Se estiver bem atrás, planejar
      pedido de avaliação a clientes recentes satisfeitos — pedir
      especificamente que mencionem a área jurídica no comentário (ex:
      "resolveu meu caso trabalhista"), isso ajuda o Google a casar o
      termo de busca com o perfil.
- [ ] **Publicações**: postar novidade no próprio Google Business (não só
      Instagram) pelo menos 1x por semana — sinaliza atividade contínua.
- [ ] **Serviços**: já bem populado (ex: "Ações em Litisconsórcio",
      "Reconhecimento de Vínculo Empregatício", "Reversão de Justa Causa"
      — checar se cobre as áreas atuais do site: Trabalhista, Família,
      Previdenciário, Consumidor, Cível, Assessoria Jurídica,
      Extrajudiciais). Adicionar serviço novo sempre que uma área nova
      ganhar LP no site (ver [[leticia-blog-artigo]] e o padrão `lp-v3`).
- [ ] **Categorias**: confirmar categoria principal + secundárias batem
      com os termos que a usuária quer competir (ex: "Advogado de direito
      do trabalho" + "Advogado" + "Escritório de advocacia").

## 2. Títulos e descrições das páginas do site

Cada página de área (`areas/*.html`, `lp-v3/*.html`) deve ter `<title>`
com a **frase exata** que a pessoa pesquisaria, não só o nome da
advogada. Comparar com o padrão dos concorrentes que aparecem no topo do
Google para aquele termo (ex: "Advogado Trabalhista ES", "Advogado
Trabalhista | Escritório no ES" — termo primeiro, marca depois ou nem
aparece).

- [ ] Home (`index.html`): título hoje é "Letícia Barros | Advocacia e
      Consultoria Jurídica" — genérico, sem palavra-chave. Se a usuária
      quiser competir por termo amplo (ex: "advogada Vitória ES"), vale
      testar incluir isso no título da home.
- [ ] Páginas de área: já seguem o padrão certo (ex: "Direito Trabalhista
      | Letícia Barros Advocacia") — manter esse padrão em toda LP nova.

## 3. Backlinks (menções de fora apontando pro site)

O que mais separa quem aparece nos resultados orgânicos de baixo
(Jusbrasil, diretórios jurídicos, imprensa local) de quem não aparece.

- [ ] Perfil no Jusbrasil está completo e linkando pro site?
- [ ] Perfil na OAB/ES tem o site cadastrado?
- [ ] Alguma matéria de imprensa local (Vitória/Grande Vitória) menciona
      o escritório? Se surgir oportunidade de entrevista/matéria, sempre
      pedir link pro site.
- [ ] Diretórios jurídicos gratuitos (Doutor Advogado, Advogados
      Associados, etc.) — cadastro é rápido e gera backlink de baixo
      esforço.

## 4. Checar concorrência do termo-alvo

Antes de decidir o que priorizar, pesquisar o termo real no Google (ex:
"advogado trabalhista Vitória ES") e anotar:
- Quantas avaliações têm os perfis "Locais" que aparecem no mapa
- Tempo de atividade deles (aparece no card, ex: "Mais de 3 anos de
  atividade")
- Se aparecem no orgânico abaixo do mapa, o que o título deles diz

Isso dá a régua real de quanto falta, em vez de comparar com um número
abstrato.

## O que NÃO é problema técnico (não perder tempo aqui)

Desempenho de carregamento (PageSpeed), acessibilidade e estrutura HTML
já foram tratados numa sessão de otimização em 04-05/08/2026 (imagens
comprimidas, rastreadores adiados, CSS de ícones reduzido, labels de
formulário corrigidos). O site está tecnicamente saudável — não é aí que
está o gargalo de ranking. Ver git/histórico de publicação em
`blogautomaticoleticia/lp-v3/` e `areas/` para o que já foi feito.
