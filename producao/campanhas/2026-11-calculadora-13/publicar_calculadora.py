"""Publica a LP da calculadora do 13º (09/11/2026; v2 clara no mesmo dia). Roda dentro do container da API, com os arquivos em
/tmp/calc13/. Se já existir versão no ar, guarda cópia em /tmp/bkp_calc13_v1/ antes de trocar."""
import asyncio, os
from app.services.central_google import _site_padrao
ARQUIVOS = ["lp/calculadora-13-salario.html", "lp/js/calculo-13.js"]
async def main():
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    os.makedirs("/tmp/bkp_calc13_v1", exist_ok=True)
    await sftp.garantir_diretorio(f"{raiz}/lp/js")
    for arq in ARQUIVOS:
        atual = await s.ler(arq)
        if atual:
            open(f"/tmp/bkp_calc13_v1/{os.path.basename(arq)}", "w", encoding="utf-8").write(atual); print("backup", arq)
        await sftp.upload(f"{raiz}/{arq}", open(f"/tmp/calc13/{arq}", "rb").read()); print("publicado", arq)
    await sftp.close()
asyncio.run(main())
