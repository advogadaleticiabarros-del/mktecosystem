"""Gestão do Perfil da Empresa pelo Orbit: tudo que ESCREVE no Google passa por aqui.

Interface (todas recebem um `GoogleApi` já autenticado):
- `publicar_post(api, conta, local, texto, botao, link, imagem_url)` -> {"name", "link"}
- `responder_avaliacao(api, review_name, texto)`
- `editar_perfil(api, local, descricao=, site=, servicos=)`: só os campos passados mudam
- `enviar_foto(api, conta, local, url_publica, categoria)`
- `definir_botao(api, local, tipo, url)`: botões "Agendar" etc. (cria ou atualiza)
E os rascunhos por IA, que nunca publicam sozinhos:
- `sugerir_resposta(ia, avaliacao)`, `sugerir_descricao(ia, perfil, palavras)`, `sugerir_post(ia, tema)`.

Todo texto passa por `verificar_texto_oab` antes de ir para o Google; se houver
problema que bloqueia, levanta `TextoBloqueadoOab` e nada é enviado.
"""
from urllib.parse import quote

from app.integrations.ai.base import AIClient
from app.integrations.social.google_api import GoogleApi
from app.services.conformidade_oab import bloqueia, verificar_texto_oab
from app.services.presenca_google import GSC_URL, INFO_URL, PLACE_URL, V4_URL

BOTOES_POST = {"LEARN_MORE", "BOOK", "CALL", "SIGN_UP"}
CATEGORIAS_FOTO = {"COVER", "PROFILE", "LOGO", "EXTERIOR", "INTERIOR", "AT_WORK", "TEAMS", "ADDITIONAL"}
LIMITE_POST = 1500
LIMITE_DESCRICAO = 750


class TextoBloqueadoOab(Exception):
    def __init__(self, problemas: list[dict]) -> None:
        super().__init__("; ".join(f"\"{p['trecho']}\": {p['motivo']}" for p in problemas))
        self.problemas = problemas


def _conferir(texto: str, contexto: str = "geral") -> None:
    problemas = verificar_texto_oab(texto, contexto)
    if bloqueia(problemas):
        raise TextoBloqueadoOab([p for p in problemas if p["nivel"] == "bloqueia"])


async def publicar_post(
    api: GoogleApi, conta: str, local: str, texto: str,
    botao: str | None = None, link: str | None = None, imagem_url: str | None = None,
) -> dict:
    if len(texto) > LIMITE_POST:
        raise ValueError(f"O post passa de {LIMITE_POST} caracteres.")
    _conferir(texto)
    corpo: dict = {"languageCode": "pt-BR", "summary": texto, "topicType": "STANDARD"}
    if botao:
        if botao not in BOTOES_POST:
            raise ValueError(f"Botão inválido: {botao}")
        corpo["callToAction"] = {"actionType": botao} if botao == "CALL" else {"actionType": botao, "url": link}
    if imagem_url:
        corpo["media"] = [{"mediaFormat": "PHOTO", "sourceUrl": imagem_url}]
    resultado = await api.chamar("POST", f"{V4_URL}/{conta}/{local}/localPosts", json=corpo)
    return {"name": resultado.get("name"), "link": resultado.get("searchUrl")}


async def responder_avaliacao(api: GoogleApi, review_name: str, texto: str) -> None:
    _conferir(texto, "resposta_avaliacao")
    await api.chamar("PUT", f"{V4_URL}/{review_name}/reply", json={"comment": texto})


async def editar_perfil(
    api: GoogleApi, local: str, *, descricao: str | None = None, site: str | None = None,
    servicos: list[dict] | None = None,
) -> list[str]:
    """Muda só os campos passados. Devolve os campos alterados (`updateMask`)."""
    corpo: dict = {}
    mascara: list[str] = []
    if descricao is not None:
        if len(descricao) > LIMITE_DESCRICAO:
            raise ValueError(f"A descrição passa de {LIMITE_DESCRICAO} caracteres.")
        _conferir(descricao)
        corpo["profile"] = {"description": descricao}
        mascara.append("profile.description")
    if site is not None:
        corpo["websiteUri"] = site
        mascara.append("websiteUri")
    if servicos is not None:
        _conferir(" ".join(f"{s['nome']} {s.get('descricao', '')}" for s in servicos))
        atual = await api.get(f"{INFO_URL}/{local}", {"readMask": "serviceItems,categories"})
        categoria = atual.get("categories", {}).get("primaryCategory", {}).get("name")
        estruturados = [i for i in atual.get("serviceItems", []) if "structuredServiceItem" in i]
        livres = [
            {"freeFormServiceItem": {
                "category": categoria,
                "label": {"displayName": s["nome"].strip(), "description": (s.get("descricao") or "").strip(),
                          "languageCode": "pt"},
            }}
            for s in servicos if s.get("nome", "").strip()
        ]
        corpo["serviceItems"] = estruturados + livres
        mascara.append("serviceItems")
    if not mascara:
        return []
    await api.chamar("PATCH", f"{INFO_URL}/{local}", params={"updateMask": ",".join(mascara)}, json=corpo)
    return mascara


async def enviar_foto(api: GoogleApi, conta: str, local: str, url_publica: str, categoria: str = "ADDITIONAL") -> dict:
    if categoria not in CATEGORIAS_FOTO:
        raise ValueError(f"Categoria de foto inválida: {categoria}")
    corpo = {"mediaFormat": "PHOTO", "locationAssociation": {"category": categoria}, "sourceUrl": url_publica}
    resultado = await api.chamar("POST", f"{V4_URL}/{conta}/{local}/media", json=corpo)
    return {"name": resultado.get("name"), "url": resultado.get("googleUrl")}


async def enviar_sitemap(api: GoogleApi, site_search_console: str, url_sitemap: str) -> None:
    """Avisa o Search Console do sitemap (idempotente: reenviar só pede nova leitura)."""
    await api.chamar(
        "PUT", f"{GSC_URL}/sites/{quote(site_search_console, safe='')}/sitemaps/{quote(url_sitemap, safe='')}"
    )


async def definir_botao(api: GoogleApi, local: str, tipo: str, url: str) -> dict:
    existentes = (await api.get(f"{PLACE_URL}/{local}/placeActionLinks")).get("placeActionLinks", [])
    meu = next((b for b in existentes if b.get("placeActionType") == tipo and b.get("isEditable", True)), None)
    if meu:
        return await api.chamar("PATCH", f"{PLACE_URL}/{meu['name']}", params={"updateMask": "uri"}, json={"uri": url})
    return await api.chamar("POST", f"{PLACE_URL}/{local}/placeActionLinks",
                            json={"uri": url, "placeActionType": tipo, "isPreferred": True})


# ---------------------------------------------------------------- Rascunhos por IA

VOZ = """Você escreve em nome da Dra. Letícia Barros, advogada (OAB/ES 39.948), em Vitória/ES.
Tom: acolhedor, direto, sem juridiquês, frases curtas, fala com "você", assina com "eu".
Regras da OAB (obrigatórias): sem promessa de resultado, sem autoelogio ou comparação, sem preço,
desconto ou "grátis", sem apelo de urgência ("ligue já"), sem "me chama". CTA sempre impessoal."""


async def _escrever(ia: AIClient, prompt: str, contexto: str = "geral") -> str:
    texto = (await ia.generate_text(prompt)).strip().strip('"')
    problemas = [p for p in verificar_texto_oab(texto, contexto) if p["nivel"] == "bloqueia"]
    if problemas:
        motivos = "; ".join(f"\"{p['trecho']}\" ({p['motivo']})" for p in problemas)
        texto = (await ia.generate_text(f"{prompt}\n\nA versão anterior foi recusada por: {motivos}. Reescreva sem isso.")).strip().strip('"')
    return texto


async def sugerir_resposta(ia: AIClient, avaliacao: dict) -> str:
    prompt = f"""{VOZ}

Escreva a resposta pública da Dra. a esta avaliação do Google.
- Agradeça pelo nome ({avaliacao.get('autor', '')}), de 1 a 3 frases, calorosa e natural, sem emoji em excesso.
- SIGILO PROFISSIONAL: não confirme que a pessoa é cliente, não fale de processo, causa, acordo, valores ou do caso.
- Nota baixa: reconheça a experiência, sem discutir, e convide a conversar pelos canais do escritório.
- Responda só com o texto da resposta.

Nota: {avaliacao.get('nota')} estrelas
Comentário: {avaliacao.get('comentario') or '(sem comentário)'}"""
    return await _escrever(ia, prompt, "resposta_avaliacao")


async def sugerir_descricao(ia: AIClient, perfil: dict, palavras: list[str]) -> str:
    prompt = f"""{VOZ}

Reescreva a descrição do Perfil da Empresa no Google deste escritório.
- Até 700 caracteres, em parágrafos curtos, sem emojis e sem links.
- Cite a cidade ({perfil.get('cidade')}) e a região atendida de forma natural.
- Use naturalmente os assuntos que as pessoas buscam: {', '.join(palavras[:12]) or 'direitos da gestante, demissão, rescisão'}.
- Não use "especialista" (a não ser que já esteja na descrição atual e seja título dela).
- Responda só com o texto.

Descrição atual:
{perfil.get('descricao', '')}

Serviços: {', '.join(s['nome'] for s in perfil.get('servicos', []))}"""
    texto = await _escrever(ia, prompt)
    return texto[:LIMITE_DESCRICAO]


async def sugerir_post(ia: AIClient, tema: str) -> str:
    prompt = f"""{VOZ}

Escreva um post para o Perfil da Empresa no Google sobre: {tema}
- De 400 a 900 caracteres. Abra com a situação concreta da pessoa, explique o direito em linguagem simples,
  termine com uma frase impessoal como "Se esse é o seu caso, procure uma advogada de confiança."
- Sem hashtags, sem links no texto, no máximo 1 emoji.
- Responda só com o texto do post."""
    return (await _escrever(ia, prompt))[:LIMITE_POST]
