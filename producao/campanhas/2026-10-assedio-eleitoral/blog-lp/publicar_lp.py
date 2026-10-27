import asyncio, os
from app.services.central_google import _site_padrao
async def main():
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    os.makedirs("/tmp/bkp_lp_voto", exist_ok=True)
    atual = await s.ler("lp/demissao-por-voto.html")
    if atual:
        open("/tmp/bkp_lp_voto/demissao-por-voto.html", "w", encoding="utf-8").write(atual); print("backup feito")
    await sftp.garantir_diretorio(f"{raiz}/assets/images/lp")
    await sftp.upload(f"{raiz}/assets/images/lp/lp-demissao-voto.jpg", open("/tmp/lp-demissao-voto.jpg", "rb").read())
    await sftp.upload(f"{raiz}/lp/demissao-por-voto.html", open("/tmp/demissao-por-voto.html", "rb").read())
    await sftp.close(); print("lp publicada")
asyncio.run(main())
