import json
from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from app.integrations.noticias.base import Noticia
from app.models.pauta import Pauta
from app.models.tenant import Tenant, TenantConfig
from app.services.jornalista import apurar, verificacao_das_fontes

SEGUNDA = date(2026, 10, 5)
QUINTA = date(2026, 10, 8)


def _n(titulo, url, fonte, dias_atras=1):
    return Noticia(
        titulo=titulo, url=url, fonte=fonte, trecho=f"Trecho: {titulo}",
        publicado_em=datetime(2026, 10, 8, tzinfo=timezone.utc) - timedelta(days=dias_atras),
    )


GESTANTE_TST = _n("TST garante estabilidade a gestante em contrato temporário", "https://tst.jus.br/n1", "TST")
GESTANTE_G1 = _n("Gestante em contrato temporário tem estabilidade, decide TST - g1", "https://g1.globo.com/a", "g1")
PIX_BLOG = _n("Banco terá de devolver Pix de golpe, diz juíza", "https://blogqualquer.com/pix", "Blog Qualquer")


class BuscadorFalso:
    def __init__(self, noticias, falhar_em=None):
        self.noticias = noticias
        self.consultas = []
        self.falhar_em = falhar_em

    async def buscar(self, consulta, dias):
        self.consultas.append((consulta, dias))
        if self.falhar_em and self.falhar_em in consulta:
            raise RuntimeError("fora do ar")
        return self.noticias


class RedatorFalso:
    """Devolve pautas apontando para os grupos numerados que recebeu no material."""

    def __init__(self, pautas):
        self.pautas = pautas
        self.prompts = []

    async def generate_text(self, prompt):
        self.prompts.append(prompt)
        return "```json\n" + json.dumps({"pautas": self.pautas}) + "\n```"


def _pauta_redator(grupos, manchete, relevancia=70, area="Trabalhista", urgencia="media"):
    return {
        "grupos": grupos,
        "manchete": manchete,
        "gancho": "Decisão saiu esta semana.",
        "fatos": "O TST decidiu que a gestante tem estabilidade.",
        "o_que_muda": "Quem engravida no contrato temporário não pode ser dispensada.",
        "area": area,
        "angulo": "direitos",
        "urgencia": urgencia,
        "prazo": None,
        "relevancia": relevancia,
        "relevante_para_conteudo": True,
        "local_es": False,
        "formatos": {"carrossel": "3 direitos", "frase": "Gravidez não é motivo", "pergunta": "Posso ser dispensada?"},
    }


async def _tenant(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={"areas": ["Trabalhista", "Família"]}, identidade_visual={},
                        ctas={}, regras_compliance={}, canais={}))
    await db.commit()
    return tenant


def _grupo_de(prompt, url):
    """Número do grupo em que a URL apareceu no material enviado ao redator."""
    for linha in prompt.splitlines():
        if url in linha:
            return int(linha.split("]")[0].split("[")[-1])
    raise AssertionError(f"{url} não está no material")


@pytest.mark.anyio
async def test_mesmo_fato_em_dois_veiculos_vira_uma_pauta_confirmada_com_fontes_reais(db_session):
    tenant = await _tenant(db_session)
    buscador = BuscadorFalso([GESTANTE_TST, GESTANTE_G1])

    class Redator(RedatorFalso):
        async def generate_text(self, prompt):
            g = _grupo_de(prompt, GESTANTE_TST.url)
            self.pautas = [_pauta_redator([g], "Gestante temporária tem estabilidade")]
            return await super().generate_text(prompt)

    pautas = await apurar(db_session, tenant.id, buscador, Redator([]), QUINTA)

    assert len(pautas) == 1
    p = pautas[0]
    assert p.titulo == "Gestante temporária tem estabilidade"
    assert p.origem == "jornalista"
    assert {f["url"] for f in p.apuracao["fontes"]} == {GESTANTE_TST.url, GESTANTE_G1.url}
    assert p.apuracao["verificacao"]["nivel"] == "oficial"
    assert p.apuracao["formatos"]["pergunta"] == "Posso ser dispensada?"
    assert "TST decidiu" in p.conteudo_bruto and GESTANTE_TST.url in p.conteudo_bruto
    assert p.fonte == "TST"


def test_verificacao_por_regra_fixa():
    assert verificacao_das_fontes([{"nome": "TST", "url": "https://tst.jus.br/x"}])["nivel"] == "oficial"
    assert verificacao_das_fontes([{"nome": "g1", "url": "https://g1.globo.com/a"},
                                   {"nome": "Folha", "url": "https://folha.uol.com.br/b"}])["nivel"] == "confirmada"
    unica = verificacao_das_fontes([{"nome": "Blog", "url": "https://blogqualquer.com/x"}])
    assert unica["nivel"] == "fonte_unica"
    assert "conferir" in unica["texto"].lower()


@pytest.mark.anyio
async def test_grupo_inexistente_citado_pelo_redator_e_descartado(db_session):
    tenant = await _tenant(db_session)
    redator = RedatorFalso([_pauta_redator([99], "Pauta inventada")])
    pautas = await apurar(db_session, tenant.id, BuscadorFalso([PIX_BLOG]), redator, QUINTA)
    assert pautas == []


@pytest.mark.anyio
async def test_tema_ja_trabalhado_nos_ultimos_30_dias_nao_volta(db_session):
    tenant = await _tenant(db_session)
    db_session.add(Pauta(tenant_id=tenant.id, titulo="Gestante temporária tem estabilidade", angulo="direitos",
                         area="Trabalhista", origem="manual", fonte="manual", relevante_para_conteudo=True))
    await db_session.commit()
    redator = RedatorFalso([_pauta_redator([1], "Gestante temporária tem estabilidade")])

    pautas = await apurar(db_session, tenant.id, BuscadorFalso([GESTANTE_TST]), redator, QUINTA)

    assert pautas == []
    assert "Gestante temporária tem estabilidade" in redator.prompts[0]  # avisado para evitar


@pytest.mark.anyio
async def test_segunda_feira_a_pauta_mais_relevante_vira_manchete_do_jornal(db_session):
    tenant = await _tenant(db_session)
    redator = RedatorFalso([
        _pauta_redator([1], "Pauta menor", relevancia=40),
        _pauta_redator([2], "Pauta principal", relevancia=90),
    ])
    pautas = await apurar(db_session, tenant.id, BuscadorFalso([GESTANTE_TST, PIX_BLOG]), redator, SEGUNDA)

    origens = {p.titulo: p.origem for p in pautas}
    assert origens == {"Pauta principal": "jornalista_manchete", "Pauta menor": "jornalista"}
    assert [p.titulo for p in pautas] == ["Pauta principal", "Pauta menor"]  # mais relevante primeiro


@pytest.mark.anyio
async def test_pedido_com_foco_busca_o_assunto_em_janela_maior(db_session):
    tenant = await _tenant(db_session)
    buscador = BuscadorFalso([PIX_BLOG])
    redator = RedatorFalso([_pauta_redator([1], "Golpe do Pix: quando o banco devolve", area="Consumidor")])

    pautas = await apurar(db_session, tenant.id, buscador, redator, QUINTA, foco="golpe do Pix")

    assert all("golpe do Pix" in c for c, _ in buscador.consultas)
    assert all(d == 30 for _, d in buscador.consultas)
    assert pautas[0].apuracao["verificacao"]["nivel"] == "fonte_unica"
    assert pautas[0].apuracao["pedido"] == "golpe do Pix"


@pytest.mark.anyio
async def test_consulta_que_falha_nao_derruba_a_apuracao(db_session):
    tenant = await _tenant(db_session)
    buscador = BuscadorFalso([GESTANTE_TST], falhar_em="Família")
    redator = RedatorFalso([_pauta_redator([1], "Gestante temporária tem estabilidade")])
    pautas = await apurar(db_session, tenant.id, buscador, redator, QUINTA)
    assert len(pautas) == 1


@pytest.mark.anyio
async def test_sem_noticias_nao_chama_o_redator(db_session):
    tenant = await _tenant(db_session)
    redator = RedatorFalso([])
    assert await apurar(db_session, tenant.id, BuscadorFalso([]), redator, QUINTA) == []
    assert redator.prompts == []
    assert (await db_session.execute(select(Pauta))).scalars().all() == []


@pytest.mark.anyio
async def test_aceita_chave_traduzida_e_numero_em_texto(db_session):
    tenant = await _tenant(db_session)
    sugestao = _pauta_redator([], "Golpe do Pix: quando o banco devolve", area="Consumidor")
    del sugestao["grupos"]
    sugestao["groups"] = ["1"]
    pautas = await apurar(db_session, tenant.id, BuscadorFalso([PIX_BLOG]), RedatorFalso([sugestao]), QUINTA)
    assert len(pautas) == 1


def test_selo_olha_so_o_dominio_e_nao_conta_o_mesmo_jornal_duas_vezes():
    falso_oficial = verificacao_das_fontes([{"nome": "Boqnews", "url": "https://boqnews.com/stf-decide-inss"}])
    assert falso_oficial["nivel"] == "fonte_unica"
    mesmo_jornal = verificacao_das_fontes([
        {"nome": "Folha PE", "url": "https://news.google.com/x", "site": "https://www.folhape.com.br"},
        {"nome": "folhape.com.br", "url": "https://www.folhape.com.br/noticia", "site": "https://www.folhape.com.br/noticia"},
    ])
    assert mesmo_jornal["nivel"] == "fonte_unica"
    oficial = verificacao_das_fontes([{"nome": "stf noticias", "url": "https://news.google.com/y",
                                       "site": "https://noticias.stf.jus.br"}])
    assert oficial["nivel"] == "oficial"


@pytest.mark.anyio
async def test_manchete_sem_exclamacao_e_gestante_vira_trabalhista(db_session):
    tenant = await _tenant(db_session)
    sugestao = _pauta_redator([1], "TST condena demissão na licença!", area="Direito da Gestante CLT")
    pautas = await apurar(db_session, tenant.id, BuscadorFalso([GESTANTE_TST]), RedatorFalso([sugestao]), QUINTA)
    assert pautas[0].titulo == "TST condena demissão na licença"
    assert pautas[0].area == "Trabalhista"
