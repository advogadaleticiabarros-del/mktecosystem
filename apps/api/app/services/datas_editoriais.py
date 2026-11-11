"""Datas que pedem atenção no calendário editorial: feriados nacionais (vêm da BrasilAPI) e datas ligadas às áreas
da Dra. (trabalhista, previdenciário, família).

Interface: `datas_do_periodo(inicio, fim, feriados)` → `list[DataEditorial]` em ordem de data. É pura: quem chama
busca os feriados (`DadosBrasil.feriados`) e passa aqui. A `ideia` é só ponto de partida de pauta; a peça continua
passando pelo manual de conteúdo e pela conferência da OAB.
"""
from dataclasses import dataclass
from datetime import date, timedelta

from app.integrations.brasil import Feriado


@dataclass(frozen=True)
class DataEditorial:
    data: date
    nome: str
    tipo: str  # "feriado" | "comemorativa" | "prazo"
    area: str
    ideia: str


# (mês, dia, nome, tipo, área, ideia)
FIXAS = [
    (1, 24, "Dia Nacional do Aposentado", "comemorativa", "previdenciário",
     "Revisões e direitos de quem já se aposentou"),
    (3, 8, "Dia Internacional da Mulher", "comemorativa", "trabalhista",
     "Direitos da gestante, igualdade salarial, assédio no trabalho"),
    (4, 27, "Dia da Trabalhadora Doméstica", "comemorativa", "trabalhista",
     "Direitos da empregada doméstica (LC 150/2015)"),
    (4, 28, "Dia em Memória das Vítimas de Acidentes de Trabalho", "comemorativa", "previdenciário",
     "Acidente de trabalho: CAT, auxílio-acidente, estabilidade"),
    (8, 7, "Aniversário da Lei Maria da Penha", "comemorativa", "família", "Medidas protetivas e rede de apoio"),
    (8, 11, "Dia do Advogado", "comemorativa", "institucional", "Bastidores do escritório, sem autopromoção"),
    (10, 12, "Dia das Crianças", "comemorativa", "família", "Pensão alimentícia e guarda"),
    (11, 30, "Prazo da 1ª parcela do 13º salário", "prazo", "trabalhista", "Como é calculado e o que fazer se atrasar"),
    (12, 10, "Dia dos Direitos Humanos", "comemorativa", "institucional", "Dignidade no trabalho"),
    (12, 20, "Prazo da 2ª parcela do 13º salário", "prazo", "trabalhista", "Descontos na 2ª parcela e atraso"),
]

IDEIA_FERIADO = {
    "Dia do Trabalho": ("trabalhista", "Direitos que muita gente não conhece"),
    "Natal": ("trabalhista", "Trabalho em feriado: folga ou pagamento em dobro"),
}


def _segundo_domingo(ano: int, mes: int) -> date:
    d = date(ano, mes, 1)
    d += timedelta(days=(6 - d.weekday()) % 7)
    return d + timedelta(days=7)


def _moveis(ano: int) -> list[DataEditorial]:
    return [
        DataEditorial(_segundo_domingo(ano, 5), "Dia das Mães", "comemorativa", "trabalhista",
                      "Licença-maternidade, estabilidade da gestante, salário-maternidade"),
        DataEditorial(_segundo_domingo(ano, 8), "Dia dos Pais", "comemorativa", "família",
                      "Licença-paternidade, guarda compartilhada"),
    ]


def datas_do_periodo(inicio: date, fim: date, feriados: list[Feriado]) -> list[DataEditorial]:
    datas: list[DataEditorial] = []
    for f in feriados:
        area, ideia = next(((a, i) for chave, (a, i) in IDEIA_FERIADO.items() if chave.lower() in f.nome.lower()),
                           ("trabalhista", "Trabalho em feriado: folga ou pagamento em dobro"))
        datas.append(DataEditorial(f.data, f.nome, "feriado", area, ideia))
    for ano in range(inicio.year, fim.year + 1):
        datas += [DataEditorial(date(ano, m, d), n, t, a, i) for m, d, n, t, a, i in FIXAS]
        datas += _moveis(ano)
    vistas: set[tuple[date, str]] = set()
    unicas = []
    for d in sorted(datas, key=lambda d: (d.data, d.tipo != "feriado")):
        if inicio <= d.data <= fim and (d.data, d.nome) not in vistas:
            vistas.add((d.data, d.nome))
            unicas.append(d)
    return unicas
