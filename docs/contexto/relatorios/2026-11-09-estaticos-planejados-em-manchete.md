# Estáticos planejados refeitos no estilo Manchete

## Pedido

"Pegue tudo que temos produzido e coloque nesses novos estilos, principalmente os estáticos."

## Feito

- `producao/estilos/manchete/conteudo_planejado.py` lê `apps/api/_saida_producao_1510/conteudo_<mes>.py` e monta, com o texto já aprovado, três modelos Manchete:
  - pergunta: a foto Pexels da peça dissolvendo no café, com a pergunta empilhada à esquerda;
  - frase: papel claro, fecho em faixa dourada;
  - Mito ou Lei: café, afirmação (riscada fino se for mito), carimbo MITO / É LEI, explicação e lei.
- Texto longo encolhe sozinho (`data-max`). A peça já gravada nunca é sobrescrita.
- 72 peças em `manchete/pecas/`: dezembro inteiro (13 perguntas, 13 frases, 14 Mito ou Lei) e novembro de 10/11 a 02/12 (32). O que é anterior a 10/11 já saiu e ficou de fora.
- As 72 entraram no editor (`manchete-nov-*`, `manchete-dez-*`; o editor tem 109 peças). `importar_estilos.py` ganhou `LOTES` para importar scripts com argumentos.
- Página de revisão: https://claude.ai/artifact/P2iDXq82BeeT4NjX5qumTA (privada).

## Verificado

- Todas as peças conferidas por folha de contato. A pergunta e a frase de 03/12, renderizadas pelo editor, têm diferença média de 0,7 e 1,1 em 255 em relação à peça pronta.
- Não verificado: celular real; revisão jurídica dos textos (são os mesmos já aprovados pela Dra.).

## Decisões e porquês

- Carrosséis ficaram como estão (a Jessica achou a grade harmoniosa com eles). Reels ganharam capa própria (relatório das capas).
- Nada foi trocado no Orbit: o acesso ao servidor foi negado pela permissão automática nesta sessão. Novembro está aprovado e agendado com a arte antiga, e trocar exige o ok da Dra. e esse acesso.
- Alterações de outras sessões em `manchete/gerar.py`, `legendas.md`, `flagrante_estaticos.py` e `motion-diario/` ficaram fora dos commits.

## Pendente

- Dra.: aprovar a arte nova.
- Jessica: liberar o acesso ao servidor para trocar a arte das peças agendadas (novembro) e dos rascunhos (dezembro), com backup antes.

## Próxima sessão

Com aprovação e acesso: backup do banco, subir os JPG para `/media` e trocar `corpo.imagem` das peças de pergunta, frase e Mito ou Lei (por data e chave). Para outro mês: `python conteudo_planejado.py <mes>` e `python ../../editor/importar_estilos.py` com um `LOTES` novo.

## Aprovação e troca no Orbit (mesmo dia)

- A Jessica aprovou ("Aprovadíssimo!") e pediu para alterar todas. O editorial produzido vai até 31/12/2026; não há plano de janeiro.
- `apps/api/_saida_producao_1510/trocar_arte_manchete.py` (commit 64692bd), roda no container. Troca só `corpo.imagem` das perguntas, frases e Mito ou Lei de 10/11 em diante, guarda a URL antiga em `corpo.imagem_anterior` e pula peça publicada ou ambígua. Sem `--aplicar`, só simula.
- Os 72 JPG estão prontos em `producao/estilos/manchete/envio/` com o prefixo `manchete-` (fora do git).
- Não aplicado: o SSH para a VPS foi negado duas vezes pela permissão automática. Falta a Jessica liberar `Bash(ssh -i ~/.ssh/orbit_vps:*)` e `Bash(scp -i ~/.ssh/orbit_vps:*)`.
- Passos quando liberar: backup do banco (`pg_dumpall`, conferir tamanho), scp dos JPG e de `conteudo_nov.py`, `conteudo_dez.py` e `trocar_arte_manchete.py` para `/tmp/manchete`, `docker compose cp` dos JPG para `api:/app/media`, rodar sem `--aplicar`, conferir e rodar com `--aplicar`, abrir 2 URLs públicas.
