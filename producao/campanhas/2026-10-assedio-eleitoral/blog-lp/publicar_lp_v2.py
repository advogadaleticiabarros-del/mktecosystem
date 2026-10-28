"""LP demissão pelo voto, versão com a seção do Espírito Santo (28/10/2026). Roda dentro do container da API, com o
HTML novo em /tmp/demissao-por-voto.html. Guarda a versão do ar em /tmp/bkp_lp_voto_v1.html antes de trocar."""
import asyncio
from app.services.central_google import _site_padrao
async def main():
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    atual = await s.ler("lp/demissao-por-voto.html")
    if atual:
        open("/tmp/bkp_lp_voto_v1.html", "w", encoding="utf-8").write(atual); print("backup feito")
    await sftp.upload(f"{raiz}/lp/demissao-por-voto.html", open("/tmp/demissao-por-voto.html", "rb").read())
    await sftp.close(); print("lp publicada")
asyncio.run(main())
