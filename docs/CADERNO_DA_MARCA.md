# Caderno da marca: Letícia Barros

Montado em 10/11/2026, a pedido da Jessica ("organize tudo que fizemos essa semana, monte um caderno com os estilos").
Junta, num lugar só, a identidade, a voz, os estilos de peça, a edição de vídeo, os Reels, os quadros (séries) e a grade
do feed. Os detalhes de cada estilo continuam nos documentos citados; este caderno é o mapa.
O mesmo conteúdo aparece no Orbit, na página **Caderno** (`/caderno`).

Prioridade em qualquer conflito: **OAB > Meta > identidade > criatividade** (`docs/MANUAL_CONTEUDO_REDES.md`).

---

## 1. Quem é a marca

- **Letícia Barros, a advogada da mulher que trabalha.** Vitória/ES, OAB/ES 39.948. Direito do trabalho,
  previdência e família. Instagram `@adv.leticiabarros2`.
- **Público:** mulheres que trabalham (CLT), gestantes e mães, maioria negra e miscigenada. Nas fotos com pessoas,
  usar mais pessoas negras, sem deixar de usar pessoas brancas (regra de 10/10/2026).
- **Personalidade (nova, 10/11/2026):** "não é só mais um feed de advogada". O perfil pega a vida real no flagra
  (a mensagem do chefe às 23h47, o holerite, o atestado recusado) e responde com a lei citada. Tem humor de situação,
  ritmo de manchete e acabamento de revista. Nunca promete resultado, nunca oferece serviço.
- **Promessa:** "Eu explico, sem juridiquês. E vou até o fim com você."

## 2. Identidade visual

| Item | Regra |
| --- | --- |
| Cores | Papel `#EFE6D9`, areia `#E8DED1`, café `#231E1A` / `#1E1814`, dourado `#C9A962` |
| Dourado | Sempre **metálico com brilho** (degradê com reflexo), nunca ouro liso (09/11/2026) |
| Faixas | Faixa dourada no topo e no rodapé de toda peça ("não tire minha identidade") |
| Títulos | **EB Garamond** (nunca Cormorant: acento solto), destaque em itálico dourado |
| Texto | Inter, algarismos alinhados, nada abaixo de 22 px |
| Acabamento | Fosco, com fibra de papel ou grão; marca d'água da logo onde couber |
| Fotos | Foto inteira e real (Pexels), um objeto ou gesto do tema; **sem recorte automático em peça** (exceto a moldura da Moldura Viva, aprovada) |
| Rosto da Dra. | Imagem original, sem filtro nem grão (26/10/2026) |
| Feed | **Claro**: papel predomina; café e foto escura entram como acento, nunca dois escuros seguidos na grade (10/11/2026) |
| Grade | Formato 1080×1440 (3:4); tudo que importa entre y 240 e 1680 no Reels |

## 3. Voz (como ela escreve)

Resumo da skill `voz-leticia` (fonte: artigos reais dela).

1. Abre com a **dor concreta**, nunca com a lei.
2. Fala com **você** e assina com **eu** ("vou ser honesta com você").
3. Lei sempre **traduzida** logo depois de citada.
4. **Valida antes de explicar** ("não é frescura").
5. Trata a leitora no feminino ("vamos juntas").
6. Explica por **contraste**.
7. CAIXA ALTA só no ponto que decide o caso.
8. **A prova é o clímax** ("essa é a parte decisiva").

Legenda padrão de rede: gancho curto → explicação → "O que vale saber" com 📌 → pergunta para comentar → "Salve e
mande para…" → "Cada caso tem detalhes. Procure uma advogada de confiança." → assinatura e OAB → **até 5 hashtags**.
Primeiro comentário com 📚 base legal e 💬 pergunta. Proibido: "me chama", "eu te ajudo", "sem compromisso",
promessa de resultado, selo de verificado falso.

## 4. Estilos de estático

| Estilo | Quando usar | Como é | Documento e código |
| --- | --- | --- | --- |
| **Manchete** (padrão desde 09/11) | Todo estático avulso; par do Flagrante | Título como manchete, faixa de ouro, objeto ou foto forte; papel claro ou café | `docs/ESTILO_MANCHETE.md`, `producao/estilos/manchete/` (34 peças + 72 do plano) |
| **Papel e Ouro** | Peças de marca e "fora da caixa" (Errata, Recibo, "Doutora, é rapidinho") | Revista em papel fosco, ouro em poucos pontos | `docs/ESTILO_PAPEL_E_OURO.md`, `producao/estilos/papel-e-ouro/` |
| **Verbete** | Apresentação e datas de marca (1º de janeiro) | Página de dicionário: "Letícia Barros: a advogada da mulher que trabalha" | `docs/ESTILO_VERBETE.md` |
| **Palavra de Ouro** | Acento escuro na grade, temas fortes | Uma palavra em ouro, foto P&B, fundo fosco | `docs/ESTILO_PALAVRA_DE_OURO.md` |
| **Objeto em Cena** | Teste (05/11), em espera | Objeto do tema em cena real | `producao/estilos/objeto-em-cena/` |
| **Carrossel Ouro editorial** | Carrosséis de conteúdo | Capa com foto do tema; última página com retrato real da Dra. | `docs/PROCESSO_PRODUCAO_CARROSSEL.md` |
| **Carrossel contínuo** | Em espera (6 opções para a Dra. escolher) | Páginas que continuam uma na outra | `producao/estilos/carrossel-referencias/` |

Ajuste fino à mão: editor de artes em `producao/editor` (ler `peca.json` antes de continuar uma peça).

## 5. Reels

### 5.1 Flagrante (motion, sem voz)
Uma cena do dia a dia "pega no flagra" (mensagem do chefe, holerite, ponto), efeitos sonoros reais, sem música nem
narração, 20 a 22 s, pergunta final em marca-texto e fechamento fixo ("Leia a legenda", seguir e compartilhar).
O 23h47 foi o post de maior alcance do mês (840 contas). Capa própria **textura** (café com fibra).
`docs/ESTILO_FLAGRANTE.md`, `producao/estilos/papel-e-ouro/motion-diario/NN_assunto.py`.
Estoque em 11/11: 33 episódios prontos; 30 agendados até 26/02; 3 na reserva (guarda, pausa no banheiro,
estacionamento) para 02, 05 e 09/03.

### 5.2 Mito ou Lei (Reels Flagrante com roleta)
Afirmação na tela no 1º segundo, "Responda antes da roleta parar", meia roleta com cliques, carimbo MITO (vermelho) ou
LEI (dourado) com batida seca, resposta e base legal, cartão "Seguir". Capa **Moldura Viva** (papel claro, foto do tema
saindo da moldura; nunca repetir foto). `mito_lei.py video MM-DD` já gera a capa.
`docs/ESTILO_FLAGRANTE.md` (seção Mito ou Lei), `docs/ESTILO_MOLDURA_VIVA.md`.

### 5.3 Domingo com a Dra. (gravação dela)
Vídeo original da Dra. falando, aos **domingos às 15h30** (melhor alcance de Reels no domingo nos dados do perfil).
Capa própria em papel claro com o rosto dela tirado do vídeo: `producao/reels/capas_dra.py`.
Edição: skill `leticia-reels-premium` (fala.py até "fala ok", conferir.py até "sem avisos"), voz original só com
ganho, **sem música**, -14 LUFS, H.264 11 Mbps, punch-in nas emendas, 3D em 1 ou 2 momentos, uma versão por vídeo.
Motor moderno (ângulos, janela 3D, legenda nova) em teste com o Limbo 1/2: `producao/reels/motor-moderno/`.
Sempre perguntar o estilo: inteiro com banco de imagens e/ou tela dividida.

### 5.4 Regras de todo Reels
- Instagram: **19h no máximo** (às 21h não tinha alcance, 10/11/2026); `agenda.py` aplica.
- Reels de série: terça e sexta Flagrante, segunda/quarta/sábado Mito ou Lei, domingo Dra.
- TikTok tem grade e editorial próprios (`docs/ESTRATEGIA_TIKTOK.md`).
- Material pronto nunca é sobrescrito: versão nova é arquivo novo.

## 6. Quadros (séries fixas)

| Quadro | Formato | Dia | O que entrega |
| --- | --- | --- | --- |
| **Mito ou Lei** | Reels com roleta | seg, qua, sáb 19h | Desfaz um boato com a lei; meta: salvamentos |
| **Flagrante** | Reels motion | ter, sex 19h | A cena que todo mundo já viveu; meta: compartilhamento |
| **Manchete do dia** | Estático | 12h | O par estático do Flagrante ou um tema forte; meta: alcance |
| **Domingo com a Dra.** | Reels gravado | dom 15h30 | Rosto e voz da Dra.; meta: confiança e seguidores |
| **Você sabia?** | Manchete (layout 08) | quando couber | Direito pouco conhecido |
| **Errata / Recibo / Verbete** | Papel e Ouro | datas especiais | Peças de marca, para lembrar quem ela é |
| **Frase** | Papel claro | quinta 19h, domingo 12h | Frase de impacto do tema da semana |

## 7. Grade do feed (desde 10/11/2026)

2 publicações por dia: **post às 12h e Reels às 19h** ("quando sair reels pode sair as outras publicações ao meio dia").
Carrossel ao meio-dia é o melhor horário de carrossel do perfil (412 contas de alcance médio).

| Dia | 12h | 19h |
| --- | --- | --- |
| seg | carrossel ou estático | Reels Mito ou Lei |
| ter | Manchete (par do Flagrante) | Reels Flagrante |
| qua | carrossel ou estático | Reels Mito ou Lei |
| qui | carrossel ou Manchete | frase (papel claro) |
| sex | Manchete (par do Flagrante) | Reels Flagrante |
| sáb | carrossel ou Manchete | Reels Mito ou Lei |
| dom | frase ou estático | Reels da Dra. às 15h30 |

**Por semana:** 6 Reels (3 Mito ou Lei, 2 Flagrante, 1 da Dra.), 3 carrosséis ou estáticos de conteúdo, 3 Manchetes,
2 frases. Total: 14 no feed. Blog: segunda e quinta 9h. LinkedIn: terça e quinta 8h.
Editorial dia a dia (até 28/02/2027): `docs/EDITORIAL_DO_FEED.md`.

## 8. O que fizemos na semana (04 a 10/11/2026)

- **04/11** Pesquisa de design premium; nascem os estilos Palavra de Ouro, Verbete e Papel e Ouro.
- **05/11** Estilo Manchete; editor de artes no navegador; skill do LinkedIn; teste Objeto em Cena.
- **06/11** Calculadora do 13º (LP) e Reels 23h47 + artigo do WhatsApp fora do horário.
- **07/11** Reels do 13º, gestante e pensão com efeitos sonoros reais.
- **09/11** Estilo Flagrante (33 episódios), capas textura, link na bio novo, calculadora do 13º v2, Manchete vira o
  padrão do estático (72 peças trocadas no Orbit), carrossel contínuo em espera.
- **10/11** Mito ou Lei vira Reels com roleta e carimbo (27 vídeos), capas Moldura Viva, motor moderno dos Reels da Dra.,
  Reels às 19h, grade de 2 posts por dia, caderno da marca e editorial até 31/01/2027.

## 9. Onde está cada coisa

| O quê | Onde |
| --- | --- |
| Regras OAB e Meta, checklist | `docs/MANUAL_CONTEUDO_REDES.md` |
| Estratégia e plano até dezembro | `docs/ESTRATEGIA_CRESCIMENTO_ORGANICO.md`, `docs/PLANO_CRESCIMENTO_OUT_DEZ_2026.md` |
| Mídia paga | `docs/MIDIA_PAGA_META_ADS.md` (interesses cruzados) |
| Estado técnico do Orbit | `docs/CONTEXTO_PROJETO.md` |
| Relatórios de cada tarefa | `docs/contexto/relatorios/` |
| Agenda (regras de horário) | `apps/api/app/services/agenda.py` |
| Feed planejado com imagens | `apps/api/_saida_producao_1510/ver_feed.py` (só leitura) |
