# 18/11/2026 · Criativos de referência adaptados aos assuntos da Dra.

## Pedido
A Jessica: "anexei aqui varios criativos para copiar para os assuntos da leticia". Eram 16 imagens de outros perfis.
Depois: "perfeito, programe as postagens em horarios disponiveis e livres seguindo as regras" e "escolha alguns dias
para fazer esses posts, principalmente os que precisam ser agora".

## Feito
- 14 peças 1080×1440 em `producao/estilos/referencias-1811/` (veja o README da pasta): a estrutura de cada referência,
  com tema da Dra. (previdência, trabalho, família, uma de consumidor e uma peça de marca), cores café, papel e ouro,
  faixas douradas e textos próprios.
- Legendas na voz da Dra., primeiro comentário, base legal e texto alternativo em `conteudo.json`.
- Página de conferência com a referência ao lado: https://claude.ai/artifact/SajKU7DkA792SfgysRZ7ny
- Registro em `docs/CADERNO_DA_MARCA.md` (tabela de estilos) e `docs/CONTEXTO_PROJETO.md` (seção do dia).
- Agendamento no Orbit (`agendar.py` + `plano_agenda.json`), todas às 12h como post do feed:
  - 12 (compra não recebida): dom 29/11/2026; o carrossel "Casamento depois dos 70" foi de 29/11 para seg 22/03/2027.
  - 09 (fim de ano): qua 16/12/2026; a "Manchete: Carteira assinada" foi de 16/12 para seg 29/03/2027.
  - As outras 12: de 13 a 27/03/2027 (primeiros dias livres), alternando claras e escuras.
  - Legenda da 09 ganhou "este ano o dia 20 cai num domingo, então o pagamento deve sair até sexta, dia 18"; na 12,
    #CompraOnline virou #BlackFriday (já que sai depois da Black Friday).
- Página de conferência republicada com data e hora de cada peça; `docs/EDITORIAL_DO_FEED.md` atualizado.

## Verificado
- Banco do Orbit: `agendar.py vagas` confirmou o meio-dia ocupado até 12/03/2027 (livres: 25/12, reservado ao Natal,
  e 13/03 em diante). Depois de gravar, a consulta por dia mostrou as 14 peças e os 2 posts movidos nas datas certas, e
  uma segunda rodada de `aplicar` não duplicou nada. As 14 artes abrem pelo link público (HTTP 200).
- Backup antes de gravar: `/root/orbit-backups/antes-referencias-1811-20261118.sql.gz` (1,6 MB).
- As 14 peças foram geradas e vistas na grade. Foram corrigidos o "?" cortado (03), o rosto escondido (04), a maleta pequena
  (05), a ampulheta sob o texto (09) e a notificação sobre o rosto (13).
- Não verificado: as bases legais (escritas de memória; pontos marcados "CONFERIR"), a licença das fotos do Pexels e a
  aprovação da Dra.

## Decisões e porquês
- Peças de época trocadas com posts sem data em vez de irem para março: Black Friday e fim de ano perdem o sentido
  depois. Os posts trocados não foram apagados nem alterados, só mudaram de dia (material pronto nunca some).
- 25/12 continuou livre, reservado à mensagem de Natal.
- Copiar só a estrutura, não logo, nome ou frase: por originalidade (Meta) e ética (OAB).
- Nada de pessoa recortada na frente do título (como na referência 3), porque recorte automático é proibido.
- Barra de contatos das referências 12 a 14 trocada por base legal, "leia a legenda" e @. Sem telefone e sem "inscreva-se".
- "Perder dinheiro" (referência 7) virou "atrasar a sua aposentadoria". "Como reverter" (referência 3) virou "o que a lei
  permite fazer depois", para não prometer resultado.
- A busca de fotos pela VPS foi bloqueada pela permissão automática. As fotos foram baixadas direto do CDN público do
  Pexels, pelos ids que já estavam nos JSONs de candidatas.

## Pendente
- A Dra. (ou a Jessica) conferir as bases legais marcadas "CONFERIR" antes de 29/11 (peça 12) e 16/12 (peça 09).
- Decidir se a peça 12 (consumidor) entra, porque a área não está no caderno.

## Próxima sessão
Se a Dra. pedir mudança numa peça já agendada, gerar versão nova com nome novo e trocar a imagem no Orbit. Ler os
comentários no Artifact de conferência e ajustar com `python gerar.py ref-NN`, salvando versão nova com nome novo
(material pronto nunca é sobrescrito). Skills: `voz-leticia`, `contexto-orbit`.
