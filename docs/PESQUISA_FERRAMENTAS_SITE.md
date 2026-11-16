# Ferramentas gratuitas para o site da Dra. Letícia: o que mais fazer

Pesquisa de 16/11/2026, pedida pela Jessica junto com as calculadoras de rescisão e de licença-maternidade.

**Pergunta:** que outras ferramentas trazem mais gente do Google e mais contatos, sem ferir as regras da OAB?

## De onde vêm os dados

1. **Search Console do site:** 28 dias até 15/11/2026, coleta diária do Orbit, consulta só de leitura em `social_metrics`.
   - 11.080 aparições e 127 cliques, contra 5.268 e 70 nos 28 dias anteriores.
   - Posição média 8,0.
2. **Concorrentes da Grande Vitória**, lidos em 16/11 (ver `producao/site/prototipo-home-2026-11-16/comparativo.html`).
   - O Ezequiel Ribeiro tem calculadoras de rescisão, horas extras e juros abusivos.
   - Ninguém mais na região tem ferramentas.
3. **Mercado nacional, por busca na web:**
   - calculadoras de pensão (Smargiassi, Debit, Calcula Centro);
   - BPC/LOAS (Ribeiro Cavalcante, Calculadora Brasil);
   - jornada da EC 141 (Senior e Conta Azul, feitas para empresas).

## O que as pessoas já buscam e encontram a Dra.

| Tema | Buscas no Google (exemplos) | Aparições em 28 dias | Posição |
|---|---|---|---|
| 13º na licença-maternidade | "quem está de licença maternidade recebe 13" | ~80 | 6 a 9 |
| Pensão atrasada | "o genitor não pagou a pensão, o que fazer", "como cobrar pensão atrasada do pai" | ~100 | 8 a 10 |
| Licença de 180 dias | "180 dias licença maternidade", "licença maternidade mudou para 180 dias" | ~40 | 10 a 37 |
| Insalubridade da limpeza | "qual a porcentagem de insalubridade para auxiliar de limpeza" | ~15 | 5 a 8 |
| Divórcio | "quanto custa um divórcio", "quanto tempo demora um divórcio" | ~35 | 40 a 74 |
| Fim da 6x1 | "fim da escala 6x1 foi promulgado?" (página com 235 aparições) | ~235 | 8 |

Rescisão, FGTS e seguro-desemprego quase não aparecem hoje. O site ainda não tem conteúdo forte nesses temas, e a calculadora de rescisão é a porta de entrada para eles.

## Ranking das próximas ferramentas

Critérios: busca que já existe para o site, encaixe no público (gestante, mãe solo, trabalhador CLT), risco na OAB e esforço.

1. **Calculadora da nova jornada (fim da 6x1, EC 141)**: URGENTE, vale a partir de 16/12/2026.
   - O que mostra:
     - a jornada máxima de cada um a partir de 16/12/2026 (42 h, com 2 folgas) e de 16/12/2027 (40 h);
     - quantas horas a mais de hoje viram hora extra;
     - quanto vale a hora extra com o mesmo salário (a emenda proíbe reduzir salário).
   - Por quê:
     - o artigo da 6x1 já tem 235 aparições;
     - as calculadoras que existem são para o RH das empresas;
     - serve também para a LP de empresas (B2B).
   - Esforço: baixo. Regra: EC 141, publicada no DOU de 16/10/2026.
   - Cuidado: algumas fontes falam em 15/12 ou 17/12; o artigo da Dra. usa 16/12/2026, com base no texto da emenda ("2 meses").
2. **Calculadora da pensão atrasada.**
   - O que mostra:
     - quanto está devendo, com correção pelo INPC e juros de 1% ao mês;
     - quais parcelas permitem pedir a prisão (as 3 últimas antes da ação e as que vencerem durante ela, CPC art. 528 e Súmula 309 do STJ);
     - quais vão para penhora.
   - Por quê:
     - é o tema com mais aparições depois do 13º (cerca de 100, na posição 8 a 10);
     - é o público central da Dra. (mães solo);
     - os concorrentes só calculam "quanto pagar", não "quanto cobrar".
   - Esforço: médio. Precisa da tabela do INPC, que o Orbit pode atualizar todo mês.
3. **"Ainda dá tempo de cobrar?" (prazo para entrar na Justiça do Trabalho).**
   - O que mostra:
     - informada a data da saída, a data-limite de 2 anos;
     - o período de 5 anos que ainda pode ser cobrado (CF art. 7º, XXIX).
   - Por quê: é a pergunta que mais converte em contato, porque a pessoa descobre que o prazo está correndo.
   - Esforço: muito baixo. Cabe como bloco dentro da calculadora de rescisão e como página própria.
4. **"Fui demitida grávida: o que posso pedir?"**
   - O que mostra:
     - confirma a estabilidade (ADCT art. 10, II, b; STF Tema 497);
     - estima o período de salários até 5 meses após o parto, com 13º, férias e FGTS desse período.
   - Por quê: é o centro do nicho da Dra., e a rescisão já marca "gestante" no CRM.
   - Esforço: médio, reaproveitando `calculo-rescisao.js` e `calculo-licenca.js`.
   - OAB: mostrar como "período protegido pela lei", nunca como "valor que você vai ganhar".
5. **Calculadora de insalubridade e periculosidade.**
   - O que mostra:
     - 10, 20 ou 40% do salário mínimo (R$ 1.621 em 2026) e 30% do salário;
     - o caso de quem limpa banheiro de uso coletivo, que tem direito ao grau máximo (Súmula 448 do TST).
   - Por quê:
     - a busca já aparece na posição 5;
     - o artigo do banheiro é o mais visto do site (3.656 aparições);
     - a LP de insalubridade já existe.
   - Esforço: baixo.
6. **BPC/LOAS: renda por pessoa da família.**
   - O que mostra: a soma da renda dividida pelo número de pessoas; abaixo de 1/4 do mínimo (R$ 405,25 em 2026) cumpre o critério.
   - Também avisa:
     - que o BPC de outro membro da família não entra na conta (LOAS art. 20, § 14);
     - que acima disso a Justiça pode reconhecer o direito, com prova da necessidade.
   - Por quê: a LP do BPC para crianças já existe; os concorrentes nacionais têm, os da região não.
   - Esforço: baixo.
7. **Seguro-desemprego (número de parcelas e valor em 2026).**
   - Por quê: busca nacional muito grande e complemento natural da rescisão.
   - Concorrência: forte (governo e grandes portais), então vale como bloco dentro da rescisão, não como aposta principal.
   - Esforço: médio.
8. **Horas extras e adicional noturno.**
   - Por quê: o Ezequiel tem; é útil para o trabalhador; liga com a nova jornada.
   - Esforço: médio.

**Não recomendado agora:**
- **Calculadora de "quanto pagar de pensão".**
  - Não existe percentual fixo em lei, e as faixas das calculadoras nacionais divergem (15% a 33%, 20% a 30%…).
  - Um número na tela vira expectativa de resultado, o que é delicado pela OAB.
  - Melhor um guia "como o juiz define o valor".
- **Simulador de custo de divórcio.** As buscas existem, mas a Dra. está na posição 40 a 74. O problema ali é conteúdo e ranking, não ferramenta.

## Regras para qualquer ferramenta nova

- Mesmo modelo das três que já existem:
  - cálculo numa função pura com testes (`lp/js/*.test.js`);
  - página gerada por `lp/_gerar_calculadoras.py`;
  - resultado liberado depois de nome, WhatsApp e e-mail, com envio ao CRM e a tag `[LP calculadora-…]`;
  - marcação `WebApplication` + `FAQPage` para o Google;
  - aviso do Provimento 205/2021.
- Fonte legal em cada regra, conferida no Planalto ou no tribunal antes de publicar, e alinhada com o que a Dra. já escreveu no blog.
- Nada de "você vai ganhar", nota de cliente, número de casos ou valor de indenização como chamariz.
- Toda calculadora nova entra:
  - no bloco "Ferramentas gratuitas" da home;
  - no rodapé das outras calculadoras;
  - no `sitemap.xml` e no `llms.txt`, avisando o IndexNow.

## Já feito nesta rodada

- `lp/calculadora-rescisao.html` e `lp/calculadora-licenca-maternidade.html`, com os cálculos em `lp/js/calculo-rescisao.js` e `lp/js/calculo-licenca.js` (19 testes).
- A pergunta "quem está de licença-maternidade recebe 13º?" foi incluída na calculadora de licença. É a busca com mais aparições do site.
- O bloco "Ferramentas gratuitas" entrou na prévia da home.
- **Ainda não publicado:** espera a escolha da versão da home e a revisão da Dra.
