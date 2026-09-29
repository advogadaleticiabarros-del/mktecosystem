import json
from datetime import date, datetime, timedelta, timezone

import httpx
import pytest
from sqlalchemy import select

from app.integrations.radar.openai_pesquisador import OpenAIPesquisador
from app.integrations.radar.tavily_gemini_pesquisador import TavilyGeminiPesquisador
from app.models.pauta import Pauta
from app.models.tenant import Tenant, TenantConfig
from app.services.radar_juridico import Achado, parse_achados, rodar_radar

SEGUNDA = date(2026, 9, 28)
TERCA = date(2026, 9, 29)


class PesquisadorFalso:
    def __init__(self, achados):
        self.achados = achados
        self.chamadas = []

    async def pesquisar(self, areas, evitar, hoje):
        self.chamadas.append({"areas": areas, "evitar": evitar, "hoje": hoje})
        return self.achados


def _achado(titulo, relevante=True, area="Trabalhista"):
    return Achado(
        titulo=titulo,
        resumo=f"Resumo de {titulo}",
        area=area,
        angulo="direitos",
        fonte="TST",
        url="https://tst.jus.br/noticia",
        relevante_para_conteudo=relevante,
    )


async def _tenant(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(
        TenantConfig(
            tenant_id=tenant.id,
            voz={"areas": ["Trabalhista", "Previdenciário"]},
            identidade_visual={}, ctas={}, regras_compliance={}, canais={},
        )
    )
    await db_session.commit()
    return tenant


@pytest.mark.anyio
async def test_radar_cria_pautas_com_fonte_e_resumo(db_session):
    tenant = await _tenant(db_session)
    pesquisador = PesquisadorFalso([_achado("Horas extras de motorista de aplicativo")])

    pautas = await rodar_radar(db_session, tenant.id, pesquisador, TERCA)

    assert len(pautas) == 1
    p = pautas[0]
    assert p.origem == "radar_juridico_satelite"
    assert p.fonte == "TST"
    assert p.status == "sugerida"
    assert p.data_editorial == TERCA
    assert "Resumo de Horas extras" in p.conteudo_bruto
    assert "https://tst.jus.br/noticia" in p.conteudo_bruto
    assert pesquisador.chamadas[0]["areas"] == ["Trabalhista", "Previdenciário"]


@pytest.mark.anyio
async def test_radar_descarta_temas_repetidos_dos_ultimos_30_dias(db_session):
    tenant = await _tenant(db_session)
    db_session.add_all([
        Pauta(tenant_id=tenant.id, titulo="Revisão da vida toda: STF encerra julgamento",
              angulo="direitos", area="Previdenciário", origem="manual", fonte="manual",
              relevante_para_conteudo=True, status="sugerida"),
        Pauta(tenant_id=tenant.id, titulo="Tema antigo demais", angulo="direitos",
              area="Trabalhista", origem="manual", fonte="manual",
              relevante_para_conteudo=True, status="sugerida",
              criado_em=datetime.now(timezone.utc) - timedelta(days=45)),
    ])
    await db_session.commit()
    pesquisador = PesquisadorFalso([
        _achado("Revisão da vida toda: STF encerra o julgamento"),  # repetido
        _achado("Tema antigo demais"),  # fora da janela, pode voltar
        _achado("Salário-maternidade para autônomas"),
        _achado("Salário maternidade para autônomas"),  # duplicado no próprio lote
    ])

    pautas = await rodar_radar(db_session, tenant.id, pesquisador, TERCA)

    assert [p.titulo for p in pautas] == ["Tema antigo demais", "Salário-maternidade para autônomas"]
    assert "Revisão da vida toda: STF encerra julgamento" in pesquisador.chamadas[0]["evitar"]
    assert "Tema antigo demais" not in pesquisador.chamadas[0]["evitar"]


@pytest.mark.anyio
async def test_segunda_feira_primeiro_relevante_vira_manchete_do_jornal(db_session):
    tenant = await _tenant(db_session)
    pesquisador = PesquisadorFalso([
        _achado("Tema técnico processual", relevante=False),
        _achado("Gestante demitida tem direito a estabilidade"),
        _achado("FGTS na rescisão indireta"),
    ])

    pautas = await rodar_radar(db_session, tenant.id, pesquisador, SEGUNDA)

    origens = {p.titulo: p.origem for p in pautas}
    assert origens["Gestante demitida tem direito a estabilidade"] == "radar_juridico_manchete"
    assert origens["Tema técnico processual"] == "radar_juridico_satelite"
    assert origens["FGTS na rescisão indireta"] == "radar_juridico_satelite"


@pytest.mark.anyio
async def test_radar_persiste_no_banco_e_limita_a_8(db_session):
    tenant = await _tenant(db_session)
    temas = ["FGTS", "BPC LOAS", "Pensão alimentícia", "Guarda compartilhada", "Horas extras",
             "Auxílio-doença", "Insalubridade", "Divórcio", "Plano de saúde", "Assédio moral",
             "Aposentadoria especial", "Superendividamento"]
    pesquisador = PesquisadorFalso([_achado(t) for t in temas])

    await rodar_radar(db_session, tenant.id, pesquisador, TERCA)

    salvas = (await db_session.execute(select(Pauta))).scalars().all()
    assert len(salvas) == 8


def test_parse_achados_aceita_bloco_de_codigo_e_ignora_itens_invalidos():
    texto = """Aqui está:
```json
{"achados": [
  {"titulo": "Tema A", "resumo": "r", "area": "Família", "angulo": "direitos",
   "fonte": "STJ", "url": "https://stj.jus.br/a", "relevante_para_conteudo": true},
  {"resumo": "sem título"}
]}
```"""
    achados = parse_achados(texto)
    assert len(achados) == 1
    assert achados[0].titulo == "Tema A"
    assert achados[0].fonte == "STJ"


def test_parse_achados_texto_sem_json_retorna_vazio():
    assert parse_achados("não encontrei nada hoje") == []


RESPOSTA_OK = {"achados": [{"titulo": "Tema X", "resumo": "r", "area": "Trabalhista",
                            "angulo": "direitos", "fonte": "TST", "url": "https://x",
                            "relevante_para_conteudo": True}]}


@pytest.mark.anyio
async def test_openai_pesquisador_usa_web_search_e_le_output_text():
    enviado = {}

    def handler(request: httpx.Request) -> httpx.Response:
        enviado["url"] = str(request.url)
        enviado["auth"] = request.headers["Authorization"]
        enviado["body"] = json.loads(request.content)
        return httpx.Response(200, json={"output": [
            {"type": "web_search_call", "status": "completed"},
            {"type": "message", "content": [{"type": "output_text", "text": json.dumps(RESPOSTA_OK)}]},
        ]})

    p = OpenAIPesquisador(api_key="sk-teste", model="modelo-x", transport=httpx.MockTransport(handler))
    achados = await p.pesquisar(["Trabalhista"], ["Tema velho"], TERCA)

    assert [a.titulo for a in achados] == ["Tema X"]
    assert enviado["url"] == "https://api.openai.com/v1/responses"
    assert enviado["auth"] == "Bearer sk-teste"
    assert enviado["body"]["model"] == "modelo-x"
    assert enviado["body"]["tools"] == [{"type": "web_search"}]
    assert "Tema velho" in enviado["body"]["input"]
    assert "Trabalhista" in enviado["body"]["input"]


class TavilyFalso:
    def __init__(self):
        self.consultas = []

    async def search(self, query, max_results=5, topic="general", days=None):
        self.consultas.append({"query": query, "topic": topic, "days": days})
        return [{"title": f"Notícia sobre {query}", "url": "https://noticia", "content": "conteúdo"}]


class IAFalsa:
    def __init__(self):
        self.prompts = []

    async def generate_text(self, prompt):
        self.prompts.append(prompt)
        return json.dumps(RESPOSTA_OK)

    async def generate_json(self, prompt):
        raise AssertionError("não usado")


@pytest.mark.anyio
async def test_tavily_gemini_pesquisa_noticias_recentes_por_area():
    tavily, ia = TavilyFalso(), IAFalsa()
    p = TavilyGeminiPesquisador(tavily=tavily, ai=ia)

    achados = await p.pesquisar(["Trabalhista", "Família"], ["Tema velho"], TERCA)

    assert [a.titulo for a in achados] == ["Tema X"]
    assert any("Trabalhista" in c["query"] for c in tavily.consultas)
    assert any("Família" in c["query"] for c in tavily.consultas)
    assert all(c["topic"] == "news" and c["days"] for c in tavily.consultas)
    assert "Tema velho" in ia.prompts[0]
    assert "https://noticia" in ia.prompts[0]
