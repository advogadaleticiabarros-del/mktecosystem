# Calculadora do 13º salário (LP de captação), 06/11/2026

## Pedido
Calculadora do 13º numa landing page para captar clientes de forma orgânica, com todas as situações e fórmulas, e o
resultado mostrado só depois de nome, WhatsApp e e-mail.

## O que foi feito
- `lp/calculadora-13-salario.html`: 3 etapas (dados de trabalho → contato → resultado), FAQ com schema (SEO),
  Meta Pixel, `/js/conversoes.js` (o `generate_lead` dispara sozinho quando o CRM responde OK).
- `lp/js/calculo-13.js`: função pura `calcular13` (também publicada no site, em `/lp/js/`), com 11 testes em
  `lp/js/calculo-13.test.js` (`node lp/js/calculo-13.test.js`).
- Lead vai para `crm.advogadaleticiabarros.com.br/api/public/lead` com nome, WhatsApp, e-mail, área trabalhista,
  marca `[LP calculadora-13]`, situação, salário e resultado; `utm_campaign` padrão `calculadora-13-2026`.
  Honeypot `website`, consentimento LGPD obrigatório, nada guardado no navegador.

## Regras usadas (fontes)
- Avos: mês com 15 dias ou mais conta (Lei 4.090/1962, Decreto 10.854/2021).
- 1ª parcela sem desconto até 30/11/2026; 2ª até 20/12, que é domingo → 18/12.
- Remuneração: salário + insalubridade (10/20/40% do mínimo R$ 1.621) + periculosidade 30% + média de variáveis.
- Demissão: aviso indenizado projeta 30 + 3 dias/ano (até 90; metade no acordo, art. 484-A); justa causa zera;
  pedido de demissão sem projeção. Pagamento na rescisão.
- Afastamento INSS e meses com mais de 15 faltas injustificadas saem dos avos.
- INSS 2026 progressivo (Portaria MPS/MF 13/2026; teto R$ 8.475,55). IR exclusivo do 13º pela tabela mensal,
  dependente R$ 189,59, redução da Lei 15.270/2025 (zera até R$ 5.000; 978,62 − 0,133145 × bruto até R$ 7.350),
  conferida com o exemplo oficial (R$ 5.900 → R$ 345,92).
- Não usa o desconto simplificado no IR do 13º (estimativa conservadora); a página avisa que é estimativa.

## Teste
Playwright em 390 px e 1280 px com o envio ao CRM simulado (nenhum lead falso criado): resultado só aparece
depois do contato, sem erro de JS, sem rolagem lateral; conta conferida à mão.

## Pendente
- ~~Publicar~~ **feito em 09/11** com o ok da Jessica: `producao/campanhas/2026-11-calculadora-13/publicar_calculadora.py`
  (roda no container `vps-api-1`, backup em `/tmp/bkp_calc13/` se já houver versão). Conferido no ar: 200 nos dois
  arquivos e fluxo completo em 390 px e 1280 px, com o envio ao CRM interceptado (nenhum lead de teste criado).
- Divulgação: link na bio, Stories, 1º comentário dos 4 Reels do 13º (10, 13, 17 e 20/11), Google Business.

## v2 clara (09/11/2026)
Pedido: página mais clara, cor suave e profissional dentro do design system, sem "cara de IA", cálculo mais fácil,
comissão e adicionais já visíveis e botão de "adicionar mais" evidente. Feito com a skill `impeccable` (skills.sh).
- Base no estilo **Papel e Ouro** (`docs/ESTILO_PAPEL_E_OURO.md`): papel `#F7F2EA`, café `#2B231D`, ouro `#B4914F` só
  em fios, faixas e marca-texto (nunca em letra sobre papel); títulos EB Garamond 500, texto Inter.
- Saíram: selo acima do título, botão em degradê, brilhos, cartões com faixa lateral, ✓ em texto.
- Layout em 2 colunas no computador (título e prazos à esquerda, calculadora à direita); resultado em forma de
  **recibo** (como a peça "Recibo do 13º"), com total em marca-texto dourado.
- Formulário: comissões, horas extras/noturno e adicional (insalubridade ou periculosidade num só campo) à vista;
  "Antes de 2026 / Entrei em 2026" no lugar da data obrigatória; botão tracejado dourado com ícone para afastamento,
  faltas, dependentes e 1ª parcela já recebida. Comissões e horas extras vão separadas para o CRM.
- Rótulos das parcelas encurtados em `calculo-13.js` (cálculo igual; 11 testes passam).
- Teste Playwright 390 e 1366 px: R$ 3.924,20 bruto → R$ 3.564,70 líquido conferido à mão; sem erro, sem rolagem lateral.
- Detector da skill: contraste do placeholder e do verde do WhatsApp corrigidos; avisos de Inter e fundo creme
  mantidos de propósito (são da marca).
- **v2 no ar em 09/11** com o ok da Jessica, conferida no site (celular e computador). Script
  (`publicar_calculadora.py`, backup da v1 em `/tmp/bkp_calc13_v1/` no container).
