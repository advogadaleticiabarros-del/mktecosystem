"""Checagem de texto contra a publicidade proibida para advogados (Provimento 205/2021 e
Código de Ética da OAB), usada antes de qualquer texto ir para o Google em nome da Dra.

Interface: `verificar_texto_oab(texto, contexto)` devolve a lista de problemas
`{"trecho", "motivo", "nivel"}`. `nivel` "bloqueia" impede a publicação; "atencao" só avisa.
`contexto="resposta_avaliacao"` liga também a checagem de sigilo profissional
(resposta pública não pode confirmar que a pessoa é cliente nem falar do caso dela).
"""
import re

REGRAS: list[tuple[str, str, str]] = [
    (r"\bgarant\w*", "Promessa de resultado é proibida.", "bloqueia"),
    (r"\b100\s?%", "Promessa de resultado é proibida.", "bloqueia"),
    (r"\b(sucesso|vit[óo]ria|resultado)s? (certo|certa|garantid[oa])", "Promessa de resultado é proibida.", "bloqueia"),
    (r"\bganh(e|a|ar|amos) (a |sua |seu )?(causa|a[çc][ãa]o|processo)", "Promessa de resultado é proibida.", "bloqueia"),
    (r"\bmelhor(es)? (advogad|escrit[óo]rio|op[çc][ãa]o)", "Autoelogio e comparação com colegas são proibidos.", "bloqueia"),
    (r"\b(n[ºo°]\.?\s?1|n[úu]mero 1|l[íi]der)\b", "Autoelogio e comparação com colegas são proibidos.", "bloqueia"),
    (r"\bgr[áa]tis\b|\bgratuit\w*|\bsem custo\b|\bfree\b", "Oferta de serviço gratuito como chamariz é captação de clientela.", "bloqueia"),
    (r"\bdesconto|\bpromo[çc]|\bR\$\s?\d|\bparcel(a|e|amos)\w*", "Preço, desconto e promoção não podem ser anunciados.", "bloqueia"),
    (r"\bligue j[áa]|\bn[ãa]o perca|\b[úu]ltimas vagas|\bvagas limitadas|\bcorra\b", "Apelo de urgência é mercantilização (captação).", "bloqueia"),
    (r"\bespecialista\b", "Só use \"especialista\" se a Dra. tiver o título de especialização na área; senão, troque por \"atuação em\".", "atencao"),
]

REGRAS_SIGILO: list[tuple[str, str, str]] = [
    (r"\bseu (processo|caso)|\bsua (a[çc][ãa]o|causa|audi[êe]ncia|senten[çc]a)|\bacordo\b|\bindeniza[çc]",
     "Sigilo profissional: a resposta pública não pode falar do caso nem confirmar que a pessoa é cliente.", "bloqueia"),
]


def verificar_texto_oab(texto: str, contexto: str = "geral") -> list[dict]:
    regras = REGRAS + (REGRAS_SIGILO if contexto == "resposta_avaliacao" else [])
    problemas = []
    for padrao, motivo, nivel in regras:
        for achado in re.finditer(padrao, texto or "", re.IGNORECASE):
            problemas.append({"trecho": achado.group(0), "motivo": motivo, "nivel": nivel})
    return problemas


def bloqueia(problemas: list[dict]) -> bool:
    return any(p["nivel"] == "bloqueia" for p in problemas)
