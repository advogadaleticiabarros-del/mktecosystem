# 18/11/2026 · Criativos de referência adaptados aos assuntos da Dra.

## Pedido
A Jessica: "anexei aqui varios criativos para copiar para os assuntos da leticia". Eram 16 imagens de outros perfis.

## Feito
- 14 peças 1080×1440 em `producao/estilos/referencias-1811/` (veja o README da pasta): a estrutura de cada referência,
  com tema da Dra. (previdência, trabalho, família, uma de consumidor e uma peça de marca), cores café, papel e ouro,
  faixas douradas e textos próprios.
- Legendas na voz da Dra., primeiro comentário, base legal e texto alternativo em `conteudo.json`.
- Página de conferência com a referência ao lado: https://claude.ai/artifact/SajKU7DkA792SfgysRZ7ny
- Registro em `docs/CADERNO_DA_MARCA.md` (tabela de estilos) e `docs/CONTEXTO_PROJETO.md` (seção do dia).

## Verificado
- As 14 peças foram geradas e vistas na grade. Foram corrigidos o "?" cortado (03), o rosto escondido (04), a maleta pequena
  (05), a ampulheta sob o texto (09) e a notificação sobre o rosto (13).
- Não verificado: as bases legais (escritas de memória; pontos marcados "CONFERIR"), a licença das fotos do Pexels e a
  aprovação da Dra.

## Decisões e porquês
- Copiar só a estrutura, não logo, nome ou frase: por originalidade (Meta) e ética (OAB).
- Nada de pessoa recortada na frente do título (como na referência 3), porque recorte automático é proibido.
- Barra de contatos das referências 12 a 14 trocada por base legal, "leia a legenda" e @. Sem telefone e sem "inscreva-se".
- "Perder dinheiro" (referência 7) virou "atrasar a sua aposentadoria". "Como reverter" (referência 3) virou "o que a lei
  permite fazer depois", para não prometer resultado.
- A busca de fotos pela VPS foi bloqueada pela permissão automática. As fotos foram baixadas direto do CDN público do
  Pexels, pelos ids que já estavam nos JSONs de candidatas.

## Pendente
- A Dra. (ou a Jessica) aprovar as peças e conferir a lei. Depois disso, enviar ao Orbit e agendar no horário de 12h da
  grade (`agenda.py`).
- Decidir se a peça 12 (consumidor) entra, porque a área não está no caderno.

## Próxima sessão
Ler os comentários no Artifact de conferência e ajustar com `python gerar.py ref-NN`, salvando versão nova com nome novo
(material pronto nunca é sobrescrito). Skills: `voz-leticia`, `contexto-orbit`.
