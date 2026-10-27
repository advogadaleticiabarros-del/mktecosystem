# Campanha: demissão por causa do voto (assédio eleitoral) · 27/10/2026

Pedido da Jessica, 27/10/2026, 12h: tema em alta depois do 2º turno (25/10). "Urgente, postar de imediato, ter
formulários para captação dos leads". Peças: landing page com formulário, artigo de blog (cliques e conversão),
carrossel, Stories, Reels animado com narração (voz da Dra. clonada das gravações dela). Depois, Reels com a Dra.
gravando (roteiro em `producao/reels/series/21-assedio-eleitoral/roteiro-gravacao.md`).

## Posição (vale para todas as peças)
- **Neutro**: nunca citar partido, candidato, presidente, deputado ou "lado". A frase-chave é "não importa em quem
  você votou". Isso protege a OAB da Dra. (Provimento 205/2021) e fala com todo trabalhador.
- **Informar a regra, não captar**: sem "me chama", "consulta gratuita", "entre com ação", promessa de resultado,
  valores. CTA: "procure uma advogada de confiança" ou ir à página com o passo a passo e o formulário.
- O formulário é para a pessoa **pedir orientação** ("Quero orientação sobre o meu caso"), nunca "garanta sua
  indenização". Mensagem de sucesso sem promessa.
- Não analisar caso em público; comentários respondidos só em tese ("cada caso precisa ser avaliado").
- Sem notícia de terceiro copiada: nossa leitura, nosso design.

## Fatos conferidos (27/10/2026)
- **Números do MPT**: 1.939 denúncias de assédio eleitoral no trabalho até o fim do 2º turno (25/10/2026), recorde,
  quase 10 vezes 2022. **140 denúncias só na segunda-feira 26/10**, maior número num único dia em 2026, em meio a
  publicações nas redes que incentivam a demissão de eleitores. Fontes: balanço do MPT citado por Metrópoles/
  francesnews (26/10), MPT-MG via RCWTV, BPMoney. Diferente de 2022, o pico veio **depois** da eleição.
  Usar "quase 2 mil denúncias" e "140 em um único dia".
- **Constituição**: art. 5º, VIII (ninguém é privado de direitos por convicção política); art. 14 (voto secreto).
- **Lei 9.029/1995**, art. 1º: proíbe prática discriminatória para acesso ou manutenção do emprego ("entre outros"
  motivos). Art. 4º: a dispensa discriminatória dá ao trabalhador, **à escolha dele**: (I) **reintegração** com
  ressarcimento integral do período de afastamento (salários corrigidos) **ou** (II) **o dobro** da remuneração do
  período de afastamento. Além disso, **dano moral** (indenização à parte).
- **Convenção 111 da OIT** (ratificada pelo Brasil): discriminação por **opinião política** no emprego é proibida.
- **Resolução TSE 23.755/2026** (alterou a 23.610/2019): propaganda e assédio eleitoral proibidos em ambiente de
  trabalho público ou privado; responde quem pratica e quem permite. Vale também em grupo de mensagens, rede social,
  transporte e evento da empresa.
- **Código Eleitoral, art. 301**: usar violência ou grave ameaça para coagir alguém a votar ou não votar em alguém é
  crime (reclusão até 4 anos), mesmo que não consiga o resultado. É o caso da **ameaça antes do voto**; a demissão
  **depois** do voto é discriminação trabalhista (Lei 9.029). Não misturar.
- **Denúncia**: site do MPT (mpt.mp.br), "Denuncie", pode ser sigilosa. Também o sindicato.
- **Limite honesto**: faltar ao trabalho para ir a manifestação pode gerar falta, desconto ou advertência. O que a lei
  proíbe é demitir **por causa** da opinião, do voto ou de participar de ato fora do horário. Ofender a empresa ou
  colegas nas redes é outra discussão; cada caso é avaliado.
- **Provas que ajudam**: mensagens, áudios, prints de grupo e de post do chefe ou da empresa, e-mails, nomes de
  testemunhas, data da demissão perto da eleição, carta de dispensa. Guardar antes de sair do grupo da empresa.
- **Prazo**: a ação trabalhista tem prazo de 2 anos após o fim do contrato (CF, art. 7º, XXIX). Não usar como
  urgência de venda; só informar.
- Julgado que pode citar (público, não é caso da Dra.): TST, 7ª Turma, 2026, manteve R$ 600 mil de dano moral
  coletivo contra associações empresariais por assédio eleitoral (citar sem valor, se preferir).

## Palavras-chave (SEO e capa)
"demitido por causa do voto", "demissão por motivo político", "assédio eleitoral no trabalho", "dispensa
discriminatória", "posso ser demitido por causa do meu voto". Linha 1 da legenda e alt text com a palavra-chave.

## Formulário (landing page)
- Endereço: `https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html` (arquivo `lp/demissao-por-voto.html`
  neste repositório, publicado por SFTP em `public_html/lp/`).
- Envio: `POST https://crm.advogadaleticiabarros.com.br/api/public/lead`, igual a `lp/guia-direitos-gestante-trabalhadora.html`
  (mesmo payload; mensagem começa com `[LP demissao-por-voto]` + origem UTM + o que aconteceu).
- Campos: nome, WhatsApp, cidade/estado, "O que aconteceu?" (fui demitido / fui ameaçado de demissão / sofri pressão
  para votar / sou empresa e quero orientação), quando, mensagem curta opcional, ciência LGPD.
- UTM por canal: `utm_source=instagram|facebook|tiktok|linkedin|blog&utm_medium=carrossel|stories|reels|post|artigo&utm_campaign=assedio-eleitoral-2026`.

## Distribuição (Instagram: 1 publicação de feed por dia; Reels só terça e sexta 21h)
- Hoje 27/10 (terça): Stories assim que aprovados (link para a LP); carrossel no feed; artigo e LP no ar.
- Reels animado: terça 27/10 21h se ficar pronto e aprovado; senão sexta 30/10 21h.
- LinkedIn (empresas): "empresário, demitir por voto custa caro" (alerta de risco, compliance), link para o artigo.
- Facebook: carrossel + link do artigo no primeiro comentário. TikTok: o mesmo Reels na fila própria.
- **Impulsionamento**: tema político entra na categoria "temas sociais, eleições ou política" da Meta (exige
  autorização e "Pago por"). Não impulsionar sem essa configuração.
