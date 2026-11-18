# Reels curtos também como Reels de teste (18/11/2026)

**Pedido:** entender por que os Reels de teste não têm visualizações; depois, "todos os reels curtos que ainda estão para sair, vamos jogar para reels teste, mas mantenha a data de publicação normal" e "é para publicar duas vezes". Teste no mesmo dia às 10h.

**Investigação (Meta consultada ao vivo)**
- Os 5 testes (27/10 e os 4 de 17/11) têm 0 ou 1 visualização na própria Meta: não é erro de coleta.
- Status da conta verde; opção "Teste" aparece no app; `trial_params` vale para todas as versões da API; os Reels normais alcançam quem não segue (105 contas em 7 dias, 1.071 em 28).
- Causa não provada: envio de teste pela API ou o tipo de vídeo (os 5 eram gravações longas da Dra.).

**Feito**
- `producao/reels/testes/teste_dos_curtos.py`: cópia `trial` (graduação MANUAL) de cada Reels curto agendado, às 10h do mesmo dia; o normal das 19h não mudou. 74 testes de 18/11/2026 a 09/03/2027 (o de hoje às 17h).
- Backup antes: `/root/orbit-backups/antes-testes-curtos-20261118.sql.gz`.

**Como ler**
- Se os testes dos curtos tiverem visualizações, o problema era o tipo de vídeo (gravações longas). Se ficarem em 0, o problema é o envio de teste pela API.
- Números na seção "Reels de teste" do Desempenho, a partir de 19/11.

**Atenção**
- O mesmo vídeo sai duas vezes no mesmo dia; o Instagram pode tratar a segunda como repetida. Vale comparar o alcance dos Reels normais das próximas semanas com os anteriores (60 a 75 visualizações).
- Reels curtos novos na grade precisam rodar o script de novo.
