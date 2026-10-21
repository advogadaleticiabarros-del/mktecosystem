"""Validação das ferramentas premium (21/10/2026): mesmos trechos de montar_falas_v2.py da série 18, agora com o
texto esperado de cada um, para `py fala.py montar falas.py`.
Roda como C:\\tmp\\videos-reels\\18-limbo-previdenciario\\validacao-premium\\fontes\\falas.py (VIDEOS = ../work/videos).
Resultado: "fala ok" nos dois Reels (41,2 s e 34,1 s); uma nota no trecho 4 ("médico do" ouvido como "médio de":
o corte ali tira só silêncio, pico -41 dB)."""
from pathlib import Path

SRC = Path(r"C:\Users\prosy\Downloads\IMG_0330.MOV")
VIDEOS = Path(__file__).resolve().parents[1] / "work" / "videos"
VEL = 1.05
VOCABULARIO = "limbo previdenciário, INSS, inapto, jurisprudência majoritária, Letícia Barros"
FECHO = (183.80, 186.75, "Meu nome é Letícia Barros e aqui nesse vídeo eu falo sobre seus direitos.")

FALAS = {
    1: [(0.00, 3.95, "Você sabe o que é limbo previdenciário?"),
        (4.45, 12.88, "Limbo previdenciário é quando o empregado está inapto para voltar às atividades no trabalho,"),
        (13.66, 16.70, "seja por doença, acidente de trabalho,"),
        (23.85, 36.62, "por exemplo, quando o trabalhador vai na consulta do médico do trabalho e sai de lá com um atestado "
                       "escrito inapto, e aí ele vai para o INSS."),
        (37.00, 44.25, "Chegando lá, o INSS considera que ele está em alta, que ele não tem nenhum tipo de benefício para ele receber."),
        (64.40, 66.30, "E aí o trabalhador fica nesse limbo,"),
        (67.20, 70.22, "não tem nem dinheiro do INSS"),
        (73.20, 76.10, "e não tem nem dinheiro vindo da empresa."),
        (84.40, 87.55, "O trabalhador muitas vezes pode ficar aí por meses.", "fixo"),
        FECHO],
    2: [(96.30, 98.95, "Durante esse período, no limbo previdenciário,"),
        (100.00, 103.80, "quem é responsável por esse trabalhador? É a empresa."),
        (103.80, 111.30, "Porque o trabalhador não pode ser prejudicado por não voltar para a empresa, porque não é culpa dele, "
                         "ele está doente."),
        (121.00, 122.95, "Quem vai pagar esses salários,"),
        (124.98, 127.48, "segundo a jurisprudência majoritária,"),
        (131.40, 132.30, "é a empresa."),
        (135.95, 142.95, "Ah, mas ele não trabalhou, mandou pro INSS, a empresa não tem mais essa responsabilidade."),
        (145.40, 146.10, "Errado."),
        (150.85, 155.95, "Se o trabalhador não conseguiu nenhum benefício do INSS, quem tem que pagar? É a empresa."),
        (166.25, 167.95, "Tem que receber, mesmo sem trabalhar."),
        (179.35, 182.95, "Então a empresa tem que pagar como se o trabalhador estivesse de atestado."),
        FECHO],
}
