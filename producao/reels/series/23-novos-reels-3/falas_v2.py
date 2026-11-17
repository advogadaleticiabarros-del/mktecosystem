"""Série 23, versões B (17/11/2026). Jessica: "parece o mesmo. O vídeo 1 é o que é o trabalho intermitente, o 2 é estudo
de caso; não chegou nenhum cliente, é fictício, então pode fazer também. Os que você fez, mantenha." As versões A
(intermitente-13-na-diaria-1, intermitente-de-fachada-2) ficam intactas; no fim ela escolhe.
R3 (IMG_2092) O que é o contrato intermitente: abre com o atendimento (fictício, liberado pela Jessica), explica a
   convocação e a recusa, o antigo bico que ganhou nome e por que o 13º e as férias não chegam em dezembro.
   Base e cortes: os mesmos de falas.py R1 (FGTS na diária, "não tem direito a férias", "nada mais vai receber" e
   "danoso" saem).
R4 (IMG_2093) Estudo de caso (hipotético: "vamos colocar 3, 4 anos"): o caso -> as provas -> a lei (art. 443 §3º, juízes
   que validam, julgados que questionam) -> levar ao Judiciário -> o desfecho (a diária vira salário; 13º, férias e FGTS
   à parte). Base: CLT arts. 9º, 443 §3º e 452-A. Corte: "ameaça" (frase invertida) e o trecho final truncado.
"""
from pathlib import Path

VIDEOS = Path(__file__).resolve().parents[1] / "work" / "videos"
VEL = 1.05
BR = Path(r"C:\Users\prosy\Desktop\NOVOS REELS\3")
SRC = BR / "IMG_2092.MOV"
FONTES = {3: BR / "IMG_2092.MOV", 4: BR / "IMG_2093.MOV"}
VOCABULARIO = ("contrato intermitente, décimo terceiro, férias, um terço, diária, convocação, bico, FGTS, CLT, "
               "artigo 443, subordinado, alternância, jurisprudência, julgados, Judiciário, Letícia Barros")

FALAS = {
    3: [(8.10, 13.05, "Hoje chegou um atendimento sobre contrato intermitente"),
        (21.15, 32.50, "Claro que nessa situação provavelmente o trabalhador já sabia que ele estava inserido nessa "
                       "modalidade de contrato, mas a grande maioria das pessoas não sabem e entram com um contrato intermitente"),
        (40.40, 48.70, "ele é convocado com três dias e pode recusar a convocação com até 24 horas, então ele não precisa "
                       "ir mas ele não receberia por esse dia."),
        (49.22, 53.07, "Esse contrato ele é o antigo extra, é o antigo bico", "fixo"),
        (53.72, 63.00, "que a gente fazia, era convocado para ir trabalhar e recebia por hora, recebia pelo dia trabalhado. "
                       "Esse é o contrato intermitente, agora ele tem um nome.", "fixo"),
        (66.52, 80.85, "não é que ele retira direito de trabalhador, mas só que lá no final do ano "
                       "agora que é período de décimo terceiro o trabalhador fica esperando receber o décimo terceiro e não "
                       "tem porque ele recebe já está incluso lá no valor da diária,", "fixo"),
        (81.25, 83.45, "assim como também ele não tem direito", "fixo"),
        (84.42, 91.88, "a receber o valor da férias, não tem direito a receber um terço de férias porque no valor do dia, "
                       "no valor daquela hora já está inserido.", "fixo"),
        (100.21, 106.47, "se o dia de trabalho for 150 reais, esse dia ele engloba décimo terceiro, férias", "fixo"),
        (112.45, 115.40, "Meu nome é Letícia Barros e aqui nesse perfil falo sobre seus direitos.")],
    4: [# "E o que que acontece nesse caso" (0,95 a 3,3) tem "que que": entra a partir de "o trabalhador"; "Estudo de caso" vai na tela
        (3.31, 9.68, "o trabalhador trabalhou em contrato intermitente, não sabia que era "
                     "contrato intermitente, ia trabalhar todos os dias,", "fixo"),
        (11.15, 15.30, "era um contrato aí sem essa alternância de atividade,"),
        (15.55, 24.28, "trabalhou ele durante anos, vamos colocar 3, 4 anos, todos os dias, e aí chegava no final do ano, "
                       "não tinha décimo terceiro, chegava no final do ano, não tinha férias", "fixo"),
        (25.62, 29.80, "tendo esse trabalhador as provas de que ele era subordinado,", "fixo"),
        (30.05, 42.30, "dessa não alternância de períodos que ele sempre trabalhou todos os dias, tendo ele essa comprovação, "
                       "testemunhas que provem que ele ia trabalhar, esse contrato pode ser questionado,", "fixo"),
        (70.62, 80.58, "Claro que como o contrato intermitente ele é regularizado dentro da CLT, ele está previsto no "
                       "artigo 443,", "fixo"),
        (82.08, 84.27, "parágrafo 3 da CLT,", "fixo"),
        (89.70, 95.30, "existe muita jurisprudência, existe muito juiz que entende como válido o contrato intermitente,"),
        (96.30, 100.10, "mas também existem alguns julgados,"),
        (42.70, 48.85, "a gente pode sim levar aos olhos do judiciário pra gente questionar esse contrato,"),
        (50.95, 69.95, "Receberia esse valor que você recebeu na diária, você receberia os reflexos dele, então esse seria "
                       "o seu salário e não englobaria aí 13º, férias, FGTS, então você poderia cobrar na justiça essa "
                       "diferença."),
        (163.30, 166.10, "Meu nome é Letícia Barros e aqui nesse perfil falo sobre seus direitos.")],
}
