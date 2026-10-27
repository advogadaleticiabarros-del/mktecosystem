"""Série 20 · gravação de 26/10/2026, NOVOS REELS/VIDEO 2: IMG_0387 + IMG_0388 + IMG_0390 unidos em bruto.mov (0-54,9 s,
54,9-143,0 s, 143,0-202,3 s). Um tema por arquivo, um Reel por tema; estilo tela dividida (escolha da Jessica, 27/10/2026).

Fatos:
- R1 gestante no contrato de experiência: estabilidade da confirmação da gravidez até 5 meses após o parto (ADCT, art. 10,
  II, "b"); vale no contrato por prazo determinado, inclusive de experiência (TST, Súmula 244, III); o desconhecimento do
  empregador não afasta o direito (Súmula 244, I), então "comunica ao RH" é conselho, não condição (tela não diz que é
  obrigatório); dispensa no período: reintegração ou indenização do período (Súmula 244, II) -> "a não ser que indenize".
- R2 limbo previdenciário: afastamento acima de 15 dias vai ao INSS (Lei 8.213/91, arts. 59-60); alta do INSS e médico da
  empresa dizendo inapta: o empregador responde pelos salários do período (jurisprudência do TST) -> mantido.
- R3 intervalo interjornada: 11 horas consecutivas entre duas jornadas (CLT, art. 66); horas suprimidas pagas como extras
  (TST, OJ 355 da SDI-1) -> mantido.
Cortes (gaguejo e recomeço, achados na transcrição literal de 27/10/2026):
- R1: "entrar no, pra trabalhar" (fica "Imagina você trabalhar numa empresa"); "E agora? E agora você tem estabilidade"; "a partir do momento que você engravidou";
  "ele não vai poder te ser mandado embora. Não vai."; "desde, até, é..., cinco meses" (fica "até cinco meses").
- R2: primeiro "o limbo previdenciário," (repetido); "responsável pelo, por esse pagamento"; "que ficou doente"; a primeira versão de "chegando lá no médico do
  trabalho..." (refeita logo depois, mais limpa).
- R3: "11 horas da noite, 10 horas da noite" (fica só "10 horas da noite"); "você" arrastado antes de "precisa ter direito"; "até para o trabalhador ter direito a essa saúde, ter direito a
  esse descanso" (recomeço); "a empresa deixa de cumprir".
"""
from pathlib import Path

SRC = Path(__file__).resolve().parent / "bruto.mov"
VIDEOS = Path(__file__).resolve().parents[1] / "work" / "videos"
VEL = 1.05
VOCABULARIO = ("estabilidade da gestante, contrato de experiência, concepção, parto, RH, limbo previdenciário, INSS, médico do "
               "trabalho, apta, interjornada, escala, hora extra, Letícia Barros, perfil")
FECHO_LIMBO = (139.72, 142.95,  # não usado: a transcrição literal saiu embolada; vale o FECHO3, mais limpo
     "Meu nome é Letícia Barros e aqui nesse perfil falo sobre os seus direitos.", "fixo")
FECHO3 = (199.25, 202.05, "Meu nome é Letícia Barros e aqui nesse perfil falo sobre os seus direitos.", "fixo")

# Pontas medidas na transcrição literal e nos silêncios a -38 dB; os trechos duvidosos foram ouvidos isolados antes.
# "fixo": a ponta não escorrega para a pausa vizinha, onde estava o gaguejo.
FALAS = {
    1: [(0.95, 2.02, "Imagina você", "fixo"),                              # sem "entrar no,"
        (2.76, 9.45, "trabalhar numa empresa, toda empolgada, feliz da vida, e vai lá e engravida.", "fixo"),
        (10.70, 12.48, "No contrato de experiência.", "fixo"),
        (13.38, 14.32, "E agora?", "fixo"),
        (16.58, 20.45, "Você tem direito à estabilidade da gestante, a estabilidade provisória.", "fixo"),
        (21.25, 23.97, "A partir do momento da concepção,", "fixo"),
        (25.70, 28.00, "descobriu que está grávida, comunica ao RH.", "fixo"),
        (28.40, 31.05, "Comunica, porque esse RH não vai poder te mandar embora.", "fixo"),
        (31.50, 33.58, "Ah, doutora, mas o contrato é por prazo determinado.", "fixo"),
        (33.60, 34.73, "Quando acabar o contrato,", "fixo"),
        (36.80, 38.14, "não vai poder te ser mandada embora.", "fixo"),
        (38.20, 43.20, "A não ser que a empresa indenize o seu período de estabilidade,", "fixo"),
        (43.40, 46.72, "que vai desde o momento que você descobriu que estava grávida,", "fixo"),
        (47.45, 47.74, "até", "fixo"),
        (48.93, 50.60, "cinco meses após o parto.", "fixo"),
        FECHO3],
    2: [(60.05, 63.95, "O limbo previdenciário é quando a pessoa que está doente,", "fixo"),
        (65.00, 73.20, "tem carteira assinada, precisou ficar afastada do trabalho por mais de 15 dias e aí foi encaminhada "
                       "para o INSS.", "fixo"),
        (73.90, 84.10, "Depois do período que o INSS tem que te manter encostada lá, ele considerou que você não está doente, "
                       "que você precisa retornar ao trabalho.", "fixo"),
        (98.30, 104.70, "Chegando lá no trabalho, o médico do trabalho considera que você não está apta para voltar para o "
                        "seu posto de trabalho.", "fixo"),
        (105.30, 108.20, "E aí ele te devolve lá para o INSS.", "fixo"),
        (109.20, 114.40, "E aí o INSS vai falar bem assim, olha, ela não está doente, ela precisa voltar para o trabalho.", "fixo"),
        (115.05, 124.40, "E aí você está nesse limbo previdenciário, você não está nem recebendo da empresa, nem recebendo "
                         "do INSS.", "fixo"),
        (125.00, 132.60, "E aí nessa situação você precisa procurar a justiça caso a empresa não te pague os seus salários.", "fixo"),
        (132.70, 135.88, "Para você receber esse período, quem vai ser responsável", "fixo"),
        (136.20, 138.95, "por esse pagamento é a empresa.", "fixo"),           # sem o "pelo," do recomeço
        FECHO3],
    3: [(143.85, 149.10, "Quando eu trabalhava por escalas, muitas das vezes eu saía de uma escala", "fixo"),
        (151.28, 154.25, "10 horas da noite, por exemplo.", "fixo"),           # sem "10 horas," dito duas vezes
        (154.45, 161.55, "E aí no outro dia eu já tinha que entrar no primeiro turno, então eu já tinha que começar a trabalhar "
                         "7 horas da manhã.", "fixo"),
        (161.65, 167.70, "Com o sistema de escala, falta de funcionário, enfim, isso não pode e é vedado pela lei.", "fixo"),
        (168.95, 181.20, "Precisa ter direito a pelo menos 11 horas de descanso. Então desde o fim da sua jornada até o início da sua próxima jornada, tem que ter um intervalo de 11 "
                         "horas de descanso.", "fixo"),
        (181.26, 183.70, "Até para assegurar a sua saúde.", "fixo"),
        (190.05, 192.25, "Se a empresa não cumpre isso,", "fixo"),
        (194.12, 195.70, "ela precisa de pagar hora extra.", "fixo"),
        (195.80, 199.25, "A empresa está violando direitos trabalhistas.", "fixo"),
        FECHO3],
}
