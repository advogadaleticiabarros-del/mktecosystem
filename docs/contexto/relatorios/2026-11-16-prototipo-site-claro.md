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

Mudanças de texto na prévia, por regra da OAB e da Meta:
- saíram os números "+500 clientes", "100%", "5.0 no Google" e "5+ anos" (selo);
- saiu "eu faço acontecer";
- "compromisso com resultados" saiu da frase de apoio;
- "melhores estratégias" virou "caminhos jurídicos possíveis";
- "maiores suas chances" virou "melhor";
- o widget Elfsight virou um bloco com link "Ver todas as avaliações no Google". No site real, o widget volta com carregamento sob demanda.

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

## Pendente (decide a Jessica)
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
