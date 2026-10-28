import asyncio
from app.services.central_google import _site_padrao
async def main():
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    if await s.ler("lp/assedio-eleitoral-es.html"):
        print("já existe no site: nada publicado"); await sftp.close(); return
    await sftp.upload(f"{raiz}/lp/assedio-eleitoral-es.html", open("/tmp/assedio-eleitoral-es.html", "rb").read())
    await sftp.close(); print("lp es publicada")
asyncio.run(main())
