"""Rerenderiza só o fechamento (outro) de cada Reel e recodifica com o áudio já pronto."""
import asyncio, os, sys
import serie
async def main():
    for n in (1, 2, 3):
        cfg, _ = serie.montar_cfg(n)
        fala = cfg["semLegenda"][0][0]
        os.environ["DESDE_QUADRO"] = str(int(fala * serie.FPS) - 2)
        pasta = await serie.renderizar(n, cfg)
        a = serie.AQUI / f"audio_r{n}"
        print(serie.codificar(n, pasta, cfg["total"], a / "com_musica.wav", a / "sem_musica.wav"), flush=True)
asyncio.run(main())
