# Marketing OS — Design v1 (Módulo Conteúdo)

## Contexto e visão

Plataforma SaaS multi-tenant de marketing com IA. O objetivo de longo prazo é atender
múltiplos negócios em múltiplos segmentos (jurídico, software, proteção veicular) a
partir de uma única engine — cada negócio é um *tenant*, configurado por dados, não
por código.

**Tenant 0:** Advogada Letícia Barros (jurídico — trabalhista/previdenciário/família/
consumidor). Tenants futuros conhecidos: Prosystem (software), empresa de proteção
veicular. Nenhum deles além da Letícia é construído na v1 — só a arquitetura já não
os bloqueia.

A visão completa do produto (pesquisa de tendências, distribuição multi-canal, Canva
automático, vídeo, publicação agendada, moderação de comentários, CRM, analytics,
aprendizado contínuo, tráfego pago, dashboard geral) foi decomposta em módulos. Este
documento cobre apenas a primeira fatia: o **Módulo Conteúdo**, a primeira volta
completa do ciclo `pesquisar → planejar → gerar → revisar/aprovar → guardar`.

## Escopo da v1

**Dentro do escopo:**
1. **Pesquisar (automático, sob demanda):** buscar fontes jurídicas públicas e
   sugerir temas com potencial.
2. **Planejar:** usuário escolhe um tema sugerido ou digita um tema livre.
3. **Gerar:** IA produz artigo de blog + carrossel (5 slides) + legenda + roteiro de
   stories, na voz do tenant.
4. **Revisar/Aprovar:** tela de edição inline, aprovar/rejeitar/regenerar.
5. **Guardar:** peça aprovada persistida; linha embrionária gravada na memória de
   marketing (sem métricas ainda).

**Fora do escopo v1 (deliberadamente adiado):**
- Publicação automática (blog ou redes sociais) e agendamento.
- Coleta de métricas e o loop de aprendizado (`marketing_memory` fica com schema
  criado, mas dormente — não há dados reais para aprender ainda).
- CRM, tráfego pago, múltiplos usuários/permissões, billing.
- Fontes de pesquisa frágeis: Instagram de TRTs (sem API pública estável) e
  "tendências sociais" (fonte de baixa confiabilidade). Podem entrar em iteração
  futura.

## Arquitetura

```
apps/
  web/   → Next.js (React) — dashboard, planejamento, aprovação
  api/   → FastAPI — API pura, orquestração, integrações
```

Dentro de `api/`, organização modular (estilo ERP — cada módulo isolado):

```
core/          → config, db, tenant middleware, auth (JWT)
tenants/       → cadastro de tenant + tenant_config (voz, identidade, regras)
content/       → MÓDULO 1: pautas, geração, peças, aprovação — onde a v1 vive
brain/         → marketing_memory (schema criado, não consultado ainda na v1)
integrations/  → clients de IA e fontes externas, atrás de interface
```

Princípios que valem desde a v1:
- **`tenant_id` em toda tabela.** Só a Letícia está cadastrada, mas nenhum dado é
  gravado sem isolamento por tenant.
- **Voz, identidade visual e regras de compliance são config do tenant (dado no
  banco), nunca código.** Isso é o que permite cadastrar a Prosystem depois sem
  tocar na engine.
- **IA atrás de uma interface** (`integrations/ai`). V1 usa Gemini (mesma API já
  usada no CRM e no fluxo de conteúdo da Letícia); trocar ou somar OpenAI/Claude
  depois não exige mudar o módulo `content`.
- **Sem Redis/Celery na v1.** A busca de fontes é *sob demanda* (botão "Buscar
  sugestões"), não um cron das 7h — evita infraestrutura assíncrona antes de haver
  necessidade real. Entra quando a v1 de publicação/agendamento exigir.
- **Deploy:** API + Postgres no Railway (mesmo provedor já usado pelo CRM); web no
  Vercel.

## Modelo de dados

```
tenants           → a marca. Linha 1 = Letícia.
  id, nome, slug, nicho, ativo

tenant_config      → tudo que hoje é "config da Letícia" vira dado
  tenant_id, voz (JSON), identidade_visual (JSON: cores/fontes/logo),
  ctas (JSON: whatsapp, blog_url), regras_compliance (JSON), canais (JSON)

pautas             → banco de temas, buscados ou manuais
  id, tenant_id, titulo, angulo, area, origem ('buscada' | 'manual'),
  fonte (texto, ex. "STJ - Informativo 812"), status, criado_em

content_pieces      → cada peça gerada
  id, tenant_id, pauta_id, tipo (artigo|carrossel|legenda|stories),
  corpo (JSON/HTML), status (rascunho|revisao|aprovado|rejeitado),
  versao, criado_em

marketing_memory    → o "Cérebro". Schema criado agora, consultas começam
                       só quando existir módulo de analytics.
  id, tenant_id, content_piece_id, tema, angulo, formato,
  metricas (JSON, vazio), aprendizado (texto, null)

users               → 1 usuário (você) na v1. JWT simples.
  id, email, nome, role
```

## Fluxo detalhado (pipeline v1)

**1. Pesquisar (sob demanda)**
Usuário clica "Buscar sugestões de hoje". O backend busca, em páginas públicas
estruturadas:
- Informativos de Jurisprudência (STJ, STF, TST)
- Jurisprudência em Teses (STJ)
- Súmulas e temas novos

*Deliberadamente fora:* DJe/Diário Oficial (ruído, publicações brutas sem valor
editorial direto) — confirmado pelo usuário como não relevante.

A IA lê o material buscado e filtra/ranqueia por: tema simples de explicar,
trabalhista (linha de maior volume/facilidade), potencial de captar cliente. O
resultado é gravado em `pautas` com `origem='buscada'`.

**2. Planejar**
Tela lista as pautas sugeridas (mais recentes primeiro) + campo livre para tema
manual (`origem='manual'`). Usuário escolhe uma.

**3. Gerar**
IA gera, na voz do tenant (`tenant_config.voz`, hoje espelhando a skill
`voz-leticia` e o PLAYBOOK semanal): artigo de blog (~1.200–1.800 palavras),
carrossel (5 slides), legenda, roteiro de stories. Regras inegociáveis do PLAYBOOK
(conformidade OAB, Manual de Proibições, dois ângulos direitos/sinceridade) entram
como parte fixa do prompt, não como sugestão.

**4. Revisar/Aprovar**
Tela mostra as peças geradas lado a lado. Usuário edita inline, e por peça:
aprova, rejeita, ou pede regeneração (volta ao passo 3 com o mesmo tema).

**5. Guardar**
Peças aprovadas viram `content_pieces` com `status='aprovado'`. Cada uma gera uma
linha em `marketing_memory` com tema/ângulo/formato preenchidos e
métricas/aprendizado nulos — o embrião que o futuro módulo de analytics vai
popular.

## Tratamento de erro (v1, enxuto)

- Falha ao buscar fontes externas → mensagem "sugestões indisponíveis agora, digite
  um tema manual". Não bloqueia o fluxo.
- Falha/timeout na geração de IA → erro visível + botão "tentar novamente". Sem
  fila de retry automática — no volume da v1 (1 usuário, geração sob demanda), a
  complexidade de retry automático não se paga ainda.

## Testes (v1, enxuto)

- Testes de integração da API (pytest): parse de 1 fonte de pesquisa, pipeline de
  geração ponta a ponta com IA mockada, aprovação grava com `tenant_id` correto.
- Sem suíte E2E de UI na v1 — validação manual da tela de aprovação.

## Reuso do repositório `blogautomaticoleticia`

| Ativo existente | Papel na v1 |
|---|---|
| Skill `voz-leticia` + `PLAYBOOK-CONTEUDO-SEMANAL.md` | Base do prompt de geração; conteúdo de `tenant_config.voz` |
| CSS real em produção (`pages.css` do site, ver abaixo) | `tenant_config.identidade_visual` |
| `squads/juridico/conteudo/pautas-fora-da-caixa.md` | Seed inicial de `pautas` |
| Templates `blog-article.html`, `criativo-4x5.html`, `story-9x16.html` | Templates de render das peças |

**Divergência encontrada e corrigida:** os arquivos de memória
`squads/design-system/_memory/brand-guidelines.md` e `design-tokens.md` (extraídos
em 22/06/2026) descrevem um **tema claro** (azul `#1a3a5c`, fundo off-white
`#f8f6f0`, duas fontes). Isso está **desatualizado**. Verificado direto no CSS
publicado (`advogadaleticiabarros.com.br/css/pages.css?v=20260626`) e no
`blog/index.html` ao vivo, o design real em produção é um **tema escuro**, que
bate com a descrição do PLAYBOOK:

```
--fundo-escuro:  #231E1A   (base)
--fundo-alt:     #2E2720
--fundo-card:    #352E26
--dourado:       #C9A962   (padrão — CTAs, destaques)
--dourado-dark:  #B8943F
--dourado-light: #D4BC7D
--areia:         #E8DED1   (texto claro sobre fundo escuro)
--areia-light:   #F2EBE0
--branco:        #FAF6F0 / #FFFFFF
--cafe:          #3D2B1F
--whatsapp:      #25D366   (único valor que batia com a memória antiga)

fontes: Cormorant Garamond (títulos grandes) + Playfair Display (subtítulos)
        + Inter (corpo) — três fontes, não duas.
raios:  --radius-sm/md/lg/xl → 8px / 12px / 20px / 30px
sombras: glow dourado (--shadow-gold, --dourado-glow*)
```

`tenant_config.identidade_visual` da Letícia é semeado com esta paleta (a real),
não com o conteúdo dos arquivos de memória do design-system, que devem ser
atualizados ou descartados separadamente.

**Segunda divergência (não bloqueia a v1, mas precisa resolução antes do módulo de
publicação):** `_config/hosting.yaml` aponta o blog para GitHub Pages, enquanto o
PLAYBOOK e o histórico do projeto descrevem publicação via SFTP/Hostinger. A v1 não
publica nada automaticamente, então isso fica registrado para quando o módulo de
publicação for desenhado.

## Uso do repositório ECC (affaan-m/ECC)

Não é código de produto — é um plugin de ferramentas para o Claude Code (agentes,
skills, comandos). Papel na v1:
- **Apoio ao desenvolvimento:** agentes `fastapi-reviewer`, `database-reviewer`,
  `code-architect` usados durante a implementação para revisar o código escrito.
- **Metodologia de captura de voz:** a skill `brand-voice` do ECC vira o processo
  padrão para capturar a voz de um tenant futuro que não tenha, como a Letícia tem,
  um playbook manual já pronto.
- **Anotado para o futuro (não usado na v1):** a skill `social-publisher`
  (integração com o serviço SocialClaw) é candidata a poupar a construção manual
  de integrações com 8+ redes sociais quando o módulo de publicação for desenhado.

## Roadmap de módulos seguintes (fora do escopo deste documento)

1. Publicação automática do blog (resolver a divergência SFTP vs. GitHub Pages).
2. Distribuição social + agendamento.
3. Analytics + ativação do loop de aprendizado (`marketing_memory` passa a ser
   lida, não só escrita).
4. CRM, tráfego pago.
5. Segundo tenant (Prosystem) — primeiro teste real de que a arquitetura
   multi-tenant generaliza fora do jurídico.
