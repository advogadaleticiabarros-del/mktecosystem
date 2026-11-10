# Estilo Moldura Viva

Aprovado pela Jessica em 10/11/2026 ("Aprovadíssimo"). É a **capa padrão dos Reels Mito ou Lei** e pode ser usado em
outras peças depois. Nasceu de uma referência que ela mandou: foto emoldurada sobre papel, com a pessoa saindo do quadro.

## O que define o estilo

- **Fundo claro:** papel creme com fibra (degradê `#FBF7F0` → `#EFE6D9` → `#E2D3BB`) e um brilho dourado suave no canto. Serve para clarear o feed perto dos carrosséis e dos Reels Flagrante, que são escuros.
- **Ouro sempre metálico:** faixas douradas em cima e embaixo da área da grade e um fio fino em volta da foto, com o degradê com brilho (ver [[dourado-metalico-brilho]]).
- **Foto saindo da moldura:** a pessoa ou o objeto do tema passa por cima da borda de cima, por cima do fio dourado.
  - O recorte é feito com `rembg`, modelo `isnet-general-use`. O modelo padrão estoura a memória nesta máquina.
  - Se a pessoa já está cortada no alto da foto, ou se o que passaria da borda é só um fiapo, a capa fica sem o efeito. Nesse caso, a foto é enquadrada pela cabeça ou pelo centro.
- **Texto:**
  - "Mito ou Lei?" em EB Garamond itálico, com **Lei** em ouro profundo, para ler bem no papel.
  - A afirmação do vídeo entre aspas, em itálico, com até 3 linhas.
  - Os botões MITO (contorno café) e LEI (ouro). A resposta nunca aparece: fica para o vídeo.
- **Área segura:** tudo o que importa fica entre y = 240 e y = 1680, o recorte 3:4 da grade.

## Fotos (regra da Jessica, 10/11/2026)

- A foto precisa combinar com a afirmação, e não só com o assunto geral do dia.
- **Nunca repetir a mesma imagem em dois posts**, mesmo do mesmo tema: capa, pergunta, carrossel e qualquer outro post. As capas usam fotos Pexels novas, que ainda não estavam no banco (`_fotos_pexels`), uma por capa.

## Arquivos

- Gerador: `producao/estilos/papel-e-ouro/motion-diario/capas_mito_foto.py`.
  - A lista `FOTOS` define a foto de cada data, e o script verifica se há repetida.
  - A saída é `mito-lei/<MM-DD>-<slug>/capa-moldura-viva.jpg`, e o recorte fica guardado em `mito-lei/_recortes/`.
- No Orbit: `apps/api/_saida_producao_1510/capa_mito_reels.py` grava `corpo.capa`, e o publicador manda essa URL como `cover_url`.
- Para outra peça no mesmo estilo, reaproveite `pagina()` e `geometria()`, trocando o texto e o tamanho da moldura.

## Regra (10/11/2026)
As 27 capas foram aprovadas ("todos aprovados"). Todo Reels Mito ou Lei novo já sai com a sua capa Moldura Viva:
`mito_lei.py video` gera o vídeo e chama `capas_mito_foto.py` em seguida. Ver `docs/ESTILO_FLAGRANTE.md`.
