"""Série 19 · Contrato intermitente (gravação de 26/10/2026, NOVOS REELS/VIDEO 1: IMG_0384 + IMG_0385 unidos em bruto.mov).
2 Reels (escolha da Jessica, 26/10/2026): R1 "O que é e como funciona", R2 "O problema: quando vira fraude".

Fatos (CLT art. 452-A, Lei 13.467/2017):
- convocação com pelo menos 3 dias corridos de antecedência (§1º) -> mantido;
- 1 dia útil para responder, silêncio = recusa (§2º); a recusa não descaracteriza a subordinação (§3º);
- ao fim de cada período de serviço: remuneração, férias proporcionais + 1/3, 13º proporcional, DSR e adicionais (§6º);
- FGTS e INSS recolhidos pelo empregador com base nos valores pagos no mês (§8º): não vêm no pagamento;
- trabalho contínuo todos os dias, sem convocação real, pode levar ao reconhecimento de contrato comum (art. 9º, fraude).
Cortes:
- "recusar de trabalhar com até 24 horas" / "prazo de 24 horas" / "24 horas para você recusar": a lei dá 1 dia útil (tela corrige);
- "FGTS" dentro do valor do dia (68-72 s): FGTS é depositado, não pago junto (tela: "FGTS depositado todo mês");
- trecho dos 150 reais (200-209 s): truncado ("terceiro teste");
- "por tempo determinado" (191-200 s): ela mesma se corrige; "na lei da justiça" (157 s): ininteligível;
- "a maioria das empresas, grandes empresas" (178-191 s): generalização sem base e fala baixa demais; saiu.
"""
from pathlib import Path

SRC = Path(__file__).resolve().parent / "bruto-1080.mp4"  # cópia 1080 do bruto 4K (o HEVC 10 bits em 4K estourava a memória)
VIDEOS = Path(__file__).resolve().parents[1] / "work" / "videos"
VEL = 1.05
VOCABULARIO = ("contrato intermitente, contrato por hora, CLT, FGTS, 13º, férias, aviso prévio, verbas rescisórias, "
               "convocação, empregador, juristas trabalhistas, carteira de trabalho, Letícia Barros, perfil")
FECHO = (245.40, 248.40, "Meu nome é Letícia Barros e aqui nesse perfil eu falo sobre seus direitos.")

# Revisão de 27/10/2026 ("os erros e gagueiras ainda estão aparecendo"): pontas medidas na transcrição literal (com
# hesitação) e nos silêncios a -34/-38 dB; cada trecho novo foi ouvido isolado antes de montar. "fixo" = a ponta não
# escorrega para a pausa vizinha (era assim que o "vai ser, vai ser" e o "estará, estará" voltavam).
FALAS = {
    1: [(0.70, 3.95, "Você sabia que o contrato por hora já existe?"),
        (5.65, 8.20, "Já existe, o nome dele é contrato intermitente."),
        (8.45, 9.70, "Como que funciona?"),
        (10.20, 19.95, "A pessoa que quer te contratar, ou seja, um empregador, ele te convoca para trabalhar pelo menos aí "
                       "com três dias de antecedência,"),
        (20.05, 21.45, "podendo você recusar"),
        (24.05, 28.90, "Então você vai confirmar se você vai estar disponível para trabalhar naquele dia,"),
        (52.20, 55.00, "E aí como que você vai receber por essas horas?"),
        (56.18, 59.80, "Vai ser acertado com você o valor da sua hora.", "fixo"),        # sem o primeiro "vai ser,"
        (59.95, 62.75, "Então ao chegar no final do dia você recebe,", "fixo"),
        (65.50, 69.90, "nesse valor que você está recebendo já vai vir 13º,", "fixo"),   # sem "nesse valor que você estará, estará"
        (71.00, 72.30, "e férias.", "fixo"),
        (72.85, 77.80, "Então não vai ter lá no final do ano o valor do 13º para você receber."),
        (79.95, 81.95, "Esse é o contrato intermitente."),
        FECHO],
    2: [(117.05, 128.45, "Muitos juristas trabalhistas consideram esse tipo de contrato muito danoso para o trabalhador. Por quê? "
                         "Por falta da informação correta para o trabalhador."),
        (128.50, 133.60, "O trabalhador acredita que está trabalhando em um contrato normal, um contrato de CLT normal,"),
        (134.30, 139.10, "quando você é mandado embora, você tem direito a aviso prévio, 13º, férias,", "fixo"),  # sem o "né"
        (143.30, 152.30, "E aí o trabalhador acredita que está nesse contrato, mas aí quando chega lá no final, vê que não está, "
                         "que o contrato dele é o contrato intermitente."),
        (152.50, 153.62, "E aí que está o problema.", "fixo"),
        (165.30, 168.20, "Doutora, mas a pessoa não está recebendo diariamente?"),
        (173.62, 178.10, "Se ela entender esse tipo de contrato, ok. E concordar, ok.", "fixo"),
        # "o problema é que a maioria das empresas, grandes empresas, né, elas..." (178-191 s) saiu inteiro: o miolo é dito
        # 15 a 25 dB abaixo da voz normal, sem ponto limpo de corte, e o "essa" arrastado vinha junto
        (209.55, 212.62, "Agora quando a pessoa se disponibiliza a trabalhar todos os dias,", "fixo"),
        (212.80, 214.03, "não está sendo convocada.", "fixo"),
        (214.42, 218.14, "Trabalhei lá um mês, trabalhei dois meses, trabalhei três meses.", "fixo"),  # sem o "ah"
        (219.92, 223.60, "Entende-se que já é um contrato de carteira de trabalho comum.", "fixo"),
        (225.65, 228.20, "Porque aquela pessoa está indo trabalhar todos os dias."),
        (228.95, 231.50, "Ah não, mas aí eu convoco, ela pode recusar.", "fixo"),           # sem o "pode," arrastado
        (231.82, 233.95, "Mas só que a pessoa funcionária sabe disso?", "fixo"),
        (237.96, 244.40, "A característica do contrato só funciona no papel e na prática você está tendo um funcionário sem ter.", "fixo"),
        FECHO],
}
