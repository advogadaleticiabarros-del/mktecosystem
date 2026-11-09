"""Revisão de textos de 09/11/2026: leitura rápida, concordância e precisão legal. Só peças do editor;
os JPG prontos de producao/estilos não mudam e cada peça guarda original.json ("Voltar ao original").
None = tira o texto (assinatura repetida no cabeçalho, já presente no rodapé)."""
from acervo import Acervo

MUDA = {
    "manchete-01-te-disseram": {"texto-4": "<i>gestantes</i>", "texto-6": "<i>estabilidade?</i>"},
    "manchete-04-cabelo": {"texto-5": "A lei proíbe discriminação para contratar ou para manter no emprego."},
    "manchete-09-exame": {"texto-5": "ATÉ 3 DIAS:"},
    "manchete-10-banheiro": {"texto-4": "Controlar assim pode ser abuso. A Justiça do Trabalho já deu indenização por isso."},
    "manchete-13-doar-sangue": {"texto-5": "Doação comprovada dá 1 dia de folga, sem desconto, a cada 12 meses de trabalho."},
    "objeto-em-cena-01-te-disseram": {"texto-3": "Mesmo que a empresa não saiba, vale a estabilidade. O que conta é a gravidez já existir na data da dispensa."},
    "palavra-de-ouro-01-hora-extra": {"texto-5": "Com adicional de pelo menos 50% sobre a hora normal."},
    "palavra-de-ouro-03-assinar": {"texto-2": None},
    "palavra-de-ouro-04-gravida": {"texto-5": "Gravidez não é justa causa para demitir. CLT, art. 391."},
    "palavra-de-ouro-06-burnout": {"texto-3": "Está na CID-11 como fenômeno ligado ao trabalho.<br>Letícia Barros · OAB/ES 39.948"},
    "palavra-de-ouro-grito-C-boca": {"texto-2": None},
    "papel-e-ouro-clara-05-gritar": {"texto-2": None},
    "papel-e-ouro-fora-04-errata": {"texto-8": "<i>Demitido sem justa causa</i><br>recebe o 13º proporcional."},
    "verbete-01-leticia-barros": {"texto-6": "<b>2.</b> Atua em direito do trabalho, das gestantes e das famílias.",
                                  "texto-7": "<i>Ex.: “Foi a Letícia Barros quem explicou o art. 391.”</i>"},
}

if __name__ == "__main__":
    ac = Acervo(".")
    for peca, trocas in MUDA.items():
        doc = ac.abrir(peca)
        ids = {e["id"] for e in doc["elementos"]}
        assert set(trocas) <= ids, (peca, set(trocas) - ids)
        doc["elementos"] = [e if e["id"] not in trocas else {**e, "html": trocas[e["id"]]}
                            for e in doc["elementos"] if not (e["id"] in trocas and trocas[e["id"]] is None)]
        ac.salvar(peca, doc)
        print(peca)
