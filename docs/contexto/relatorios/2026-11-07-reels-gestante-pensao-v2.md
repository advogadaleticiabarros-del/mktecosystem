# 07/11/2026 · Reels Gestante e insalubridade (1/3 a 3/3) e Pensão: mito dos 30%, versão 2

## Pedido
"Agora faça os de gestante e também substitua pelo que já está programado, faça a série inteira", "pensao-mito-30 esse
também" e "procure efeitos sonoros melhores".

## O que mudou
- Visual igual ao da V2 aprovada no 13º:
  - tudo no eixo central (x=540);
  - pares de pílulas simétricos;
  - carimbos centralizados;
  - foto com rosto ganha desfoque e o véu escuro (`VEU_ROSTO`).
- Narração, trechos e fatos iguais à v1 (`serie2.py`).
- **Efeitos sonoros v3** (`work/som3.py`): gravações reais da Mixkit no lugar dos sintetizados. A licença Mixkit Sound
  Effects Free License permite uso comercial em vídeo, sem atribuição. Mesmos momentos e níveis do som2.

| Efeito | Mixkit |
|---|---|
| whoosh | 1491 Cinematic whoosh fast transition |
| boom | 788 Cinematic whoosh deep impact |
| pop | 2925 Dry pop up notification alert |
| carimbo | 2589 Wood hard hit |
| brilho | 866 Fairy magic sparkle |
| po | 3062 Fairy sparkle whoosh |

- Roteiros em `producao/reels/series/13-reels-procedural/work/serie_gest_v2.py` (números 11, 12, 13 e 15).
- Conferência:
  - `--checar` deu "área limpa: ok" nos 4. O único aviso de LEITURA é a assinatura do fechamento, igual à v1.
  - Volume entre -13,9 e -14,5 LUFS.

## Produção
- Backup em `/root/orbit-backups/antes-reels-gestante-v2.sql.gz`.
- Mídia nova:
  - `/app/media/<nome>-v2.mp4` (com trilha, como a postagem anterior);
  - `<nome>-v2-sem-musica.mp4`.
- Peças trocadas por `subir3/trocar_video_v2_gestante.py`. O link antigo fica em `corpo.video_antes_v2`, e os arquivos
  antigos continuam no servidor.
- Datas mantidas:
  - gestante 1/3 em 24/11;
  - gestante 2/3 em 27/11;
  - gestante 3/3 em 01/12;
  - pensão em 11/12;
  - todas às 21h.

## Disco
O C: tinha 730 MB livres. Apaguei os pacotes de envio `.tar`, que eram cópias das pastas ao lado, e os quadros de cada
render. Sobram cerca de 680 MB, então é preciso liberar espaço antes do próximo vídeo.
