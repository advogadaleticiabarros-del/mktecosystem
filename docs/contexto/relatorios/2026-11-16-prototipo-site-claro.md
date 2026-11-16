# Prévia do site no estilo da Bio e comparação com concorrentes do ES (16/11/2026)

## Pedido
- Melhorar o site advogadaleticiabarros.com.br "sem que prejudique o nosso alcance ou ranking no Google".
- "Deixar bonito como o link da Bio, fácil dos clientes encontrarem no Google."
- "Faz em HTML para mim primeiro, para que eu possa analisar. Faça os dois, claro e escuro."
- "Pesquise os melhores sites e advogados do ES para podermos comparar."

## Feito
Nada foi alterado no site no ar. Tudo está em `producao/site/prototipo-home-2026-11-16/`:

- **`modelo.html`:** a fonte das duas prévias da home.
  - Mantém o head do site atual: title, description, canonical e og.
  - GA4, Pixel e JSON-LD ficam fora da prévia para não contar visita falsa. Na publicação, entram sem mudança.
  - Mantém o H1, os textos e todos os links internos.
  - Usa `<base href>` para o site real, assim fotos e links funcionam no arquivo local.
- **`home-clara.html`** e **`home-escura.html`:**
  - geradas com `sed 's/{{TEMA}}/claro|escuro/' modelo.html`;
  - têm uma barra no canto para trocar de versão;
  - **Clara:** toda em papel;
  - **Escura:** topo café com a foto da Bio; o resto continua em papel, com a faixa café da chamada final como acento nas duas.
- **`comparativo.html`** e a pasta `concorrentes/`: tabela técnica, prints e lições de 8 sites da Grande Vitória.
- **`_prints.py`:** gera os prints das prévias (Playwright com `channel="chrome"`).
- **`celular.html`:** as duas versões dentro de molduras de celular (iframes de 390 px), lado a lado. Foi pedida depois de "como vai ficar no celular". Os arquivos `.html` neste computador abrem no VS Code; para ver como página, abrir pelo `chrome.exe`.
- **Correção no celular:** o e-mail comprido do bloco de Contato empurrava a página para 408 px. Agora tem `overflow-wrap:anywhere` e `min-width:0` nas colunas, e a largura confere em 360, 390 e 430 px nas duas versões.

Mudanças de texto na prévia, por regra da OAB e da Meta:
- saíram os números "+500 clientes", "100%", "5.0 no Google" e "5+ anos" (selo);
- saiu "eu faço acontecer";
- "compromisso com resultados" saiu da frase de apoio;
- "melhores estratégias" virou "caminhos jurídicos possíveis";
- "maiores suas chances" virou "melhor";
- o widget Elfsight virou um bloco com link "Ver todas as avaliações no Google". No site real, o widget volta com carregamento sob demanda.

Rodada 2, pedido "nas comparações, vamos copiar o que achar válido e evitar o que está ruim":
- **H1:** agora é "Advogada trabalhista e de família em Vitória-ES", como fazem Ezequiel, JBDS e Lopes & Campos. "Seus direitos não podem esperar." virou `<p class="destaque">`, com o mesmo tamanho grande.
- **Telefone no menu:** entrou o link para o WhatsApp.
- **Seção "Onde atendo":**
  - cidades da Grande Vitória, endereço e horário;
  - link de rota para o Google Maps, sem mapa embutido, para não pesar.
- **Seção "Perguntas frequentes":**
  - cinco perguntas, com JSON-LD `FAQPage`;
  - temas: atendimento online, gestante demitida (ADCT art. 10, II, b e STF Tema 497), prazo de 2 anos com cobrança de 5 (CF art. 7º, XXIX), pensão atrasada (CPC art. 528 e Súmula 309 do STJ) e honorários.
- **`comparativo.html`:** cada lição tem a marca "na prévia" ou "depende", e entrou a lista "O que evitamos de propósito".

Rodada 3, pedido "faça tudo e inclua uma pesquisa sobre o que mais podemos fazer; mais calculadoras (rescisão, licença-maternidade)":
- **Calculadora de rescisão:**
  - página `lp/calculadora-rescisao.html`, cálculo em `lp/js/calculo-rescisao.js`, 12 testes em `calculo-rescisao.test.js`;
  - calcula saldo de salário, aviso proporcional, 13º e férias com 1/3, FGTS com depósito, multa e saque, INSS e IR só sobre saldo e 13º, prazo de 10 dias e o aviso para a gestante;
  - reaproveita o INSS, o IR e os avos de `calculo-13.js`.
- **Calculadora de licença-maternidade:**
  - página `lp/calculadora-licenca-maternidade.html`, cálculo em `lp/js/calculo-licenca.js`, 7 testes;
  - mostra 120 ou 180 dias, início até 28 dias antes do parto, contagem a partir da alta (ADI 6327), adoção (ADI 7.495), estabilidade, amamentação e o prazo para pedir a prorrogação.
- **As duas páginas saem de `lp/_gerar_calculadoras.py`:**
  - reaproveita o `<style>` da calculadora do 13º;
  - captura o contato e envia ao CRM com as tags `[LP calculadora-rescisao]` (área trabalhista) e `[LP calculadora-licenca]` (área gestante);
  - no `file://`, não envia ao CRM e o Pixel não carrega.
- **Prévia da home:** entrou a seção "Ferramentas gratuitas" com as três calculadoras. Os fundos das seções foram realternados.
- **Pesquisa:** `docs/PESQUISA_FERRAMENTAS_SITE.md`, com o Search Console de 28 dias, concorrentes e mercado, e o ranking das próximas ferramentas. O resumo também entrou no `comparativo.html`.

## Verificado
- Prints no celular (390 px) e no computador (1366 px) das duas versões: sem rolagem horizontal no comparativo.
- As imagens da prévia existem no site, todas com 200.
- A foto do escritório aparece vazia no print de página inteira só por causa do `loading=lazy`.
- Medições da home atual: 818 KB e 1,6 s de carregamento no celular. O peso da prévia **não foi medido de forma comparável**, porque as imagens vêm de outro domínio.
- Concorrentes:
  - title, description, H1, schema e sitemap lidos por HTTP;
  - peso e tempo medidos no Chrome headless.
- **Não verificado:**
  - posições reais no Google para cada concorrente: a raspagem do Google foi barrada pela trava de segurança e a busca usada tem pouco resultado do Brasil;
  - a lista de concorrentes veio da busca, não de um ranking.

## Decisões e porquês
- Fotos: a prévia usa `bio/leticia-bio.webp`, a mesma da Bio, em vez da `hero-leticia-sem-fundo`.
- Fontes: só EB Garamond e Inter, em vez de três famílias.
- Dourado do texto sobre papel: `#7E5F2E` por contraste. O `#B8935A` da Bio fica só em fios e detalhes.
- As letras de fundo do topo ficaram mascaradas só atrás da foto: na primeira versão, atrapalhavam a leitura do título.
- Os itens do "Como posso ajudar" usam os mesmos links das LPs de hoje, mais a calculadora do 13º.
- O H1 foi mantido de propósito. A troca para "Advogada trabalhista e de família em Vitória-ES" é a lição 3 do comparativo e espera o ok dela.

- Rodada 2, conferida nas duas versões em 360, 390, 1024 e 1366 px:
  - largura sem passar da tela;
  - um único H1;
  - JSON-LD da FAQ válido, com 5 perguntas;
  - menu com o telefone sem quebrar em 1024 px.

- Rodada 3:
  - os testes de cálculo passam (13º com 11, rescisão com 12, licença com 7);
  - o teste no Chrome, a 390 e 1366 px, percorre as duas calculadoras do começo ao resultado sem erro de JavaScript e sem passar da largura;
  - os valores na tela batem com os testes (rescisão de exemplo: líquido de R$ 9.675,14, saque do FGTS de R$ 14.845,60);
  - os links da home abrem as calculadoras;
  - **não verificado:** o envio real ao CRM, porque a prévia local não envia.

## Pendente (decide a Jessica)
- Publicar as calculadoras junto com a home:
  - subir por SFTP `lp/calculadora-rescisao.html`, `lp/calculadora-licenca-maternidade.html`, `lp/js/calculo-rescisao.js` e `lp/js/calculo-licenca.js`;
  - incluir no `sitemap.xml` e no `llms.txt`, avisar o IndexNow e testar um envio real ao CRM;
  - criar a imagem `og:image` das duas.
- Próxima ferramenta pela pesquisa: **nova jornada da EC 141**, que vale a partir de 16/12/2026.
0. **A Dra. confere as respostas da FAQ antes de publicar.** Principalmente a de honorários ("seguem a tabela da OAB/ES, contrato por escrito"): não sei se a primeira conversa é gratuita, então a resposta não promete isso.
1. Escolher entre Clara e Escura, ou pedir ajustes.
2. Aprovar ou não a troca do H1 (lição 3) e a FAQ com schema na home (lição 4).
3. Depois do ok, publicar a home:
   - backup da raiz em `/root/orbit-backups/`;
   - GA4, Pixel, JSON-LD, `conversoes.js` e o formulário com o mesmo `id="contactForm"` e o mesmo JS de envio ao CRM;
   - IndexNow;
   - conferência de title, description, canonical, JSON-LD e links iguais.
4. Uma ou duas semanas depois, o mesmo visual em Sobre, Contato, Áreas e no modelo dos artigos (`render_artigo_blog.py` do Orbit).

## Próxima sessão
- Ler este relatório e abrir `comparativo.html`.
- Aplicar a escolha dela no `modelo.html` e gerar a versão final da home a partir do `index.html` real, baixado por SFTP da VPS (usuário `siteleticia`). Só o `<body>` e o CSS trocam; o `<head>` atual fica.
- Skills: `contexto-orbit`, `leticia-seo-local`, `impeccable`.
