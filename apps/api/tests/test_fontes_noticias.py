from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import httpx
import pytest

from app.integrations.noticias.base import BuscadorMultiplo, Noticia
from app.integrations.noticias.google_news import GoogleNewsRSS


def _rss():
    agora = datetime.now(timezone.utc)
    recente, antiga = format_datetime(agora - timedelta(days=1)), format_datetime(agora - timedelta(days=40))
    return f"""<?xml version="1.0"?><rss><channel>
<item><title>TST garante estabilidade a gestante - TST</title><link>https://news.google.com/x1</link>
<pubDate>{recente}</pubDate><description>&lt;a&gt;Decisão da SDI&lt;/a&gt;</description>
<source url="https://www.tst.jus.br">TST</source></item>
<item><title>Notícia velha - g1</title><link>https://news.google.com/x2</link><pubDate>{antiga}</pubDate>
<source url="https://g1.globo.com">g1</source></item>
</channel></rss>"""


@pytest.mark.anyio
async def test_google_news_le_titulo_sem_veiculo_site_e_descarta_antigas():
    pedidos = []

    def responder(request):
        pedidos.append(request.url)
        return httpx.Response(200, text=_rss())

    noticias = await GoogleNewsRSS(transport=httpx.MockTransport(responder)).buscar("gestante", 7)

    assert len(noticias) == 1
    n = noticias[0]
    assert n.titulo == "TST garante estabilidade a gestante"
    assert n.fonte == "TST" and n.site == "https://www.tst.jus.br"
    assert n.trecho == "Decisão da SDI"
    assert "when:7d" in str(pedidos[0].params["q"])


@pytest.mark.anyio
async def test_buscador_multiplo_segue_quando_uma_fonte_cai():
    class Ok:
        async def buscar(self, c, d):
            return [Noticia("t", "u", "f", "", None)]

    class Cai:
        async def buscar(self, c, d):
            raise RuntimeError("fora")

    assert len(await BuscadorMultiplo([Cai(), Ok()]).buscar("x", 7)) == 1
    with pytest.raises(RuntimeError):
        await BuscadorMultiplo([Cai()]).buscar("x", 7)
