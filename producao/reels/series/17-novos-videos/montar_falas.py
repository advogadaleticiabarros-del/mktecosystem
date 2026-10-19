"""Monta a fala de cada Reels da série 17 (18/10/2026) a partir das gravações em Desktop/novo video (a pasta "ja usou"
não é usada). Cortes entre palavras (Whisper medium); ("PAUSA", s) insere s segundos sem fala para um cartão de
explicação sobre vídeo do banco. 1080x1920, 30 fps. Sem correção de cor (tom de pele fiel no bruto).
Fatos conferidos (18/10/2026):
- R1 multa do 477: CLT art. 477, §§ 6º e 8º (pagamento das verbas e entrega dos documentos em até 10 dias do fim do
  contrato; atraso = multa de um salário), vale também no pedido de demissão. Tomada "video correto para usar" NÃO
  usada: diz "10 dias úteis" (são corridos) e que "o contrato não está extinto".
- R2 conselhos: treinamento obrigatório é tempo à disposição (CLT art. 4º); domingo sem folga compensatória é pago em
  dobro (Lei 605/1949, art. 9º; Súmula 146 do TST). Prints e mensagens são meio de prova (CPC art. 369). A frase
  "favorzinho vira tarefa... e você vira reclamante" ficou de fora (pode soar como estímulo ao litígio, vetado pela
  OAB, Provimento 205/2021, art. 2º, VIII).
- R3 hora extra: adicional mínimo de 50% (CF art. 7º, XVI); domingo e feriado não compensados em dobro (Súmula 146).
- R4 banco de horas: acordo individual escrito com compensação em até 6 meses (CLT art. 59, § 5º) ou por convenção/
  acordo coletivo em até 1 ano (art. 59, § 2º); sem isso, a empresa paga as horas extras.
  CORTADO: "hora extra não paga tem que virar banco de horas" (errado: depende de acordo).
- R5 prova: testemunha e documentos/prints (CPC art. 369; CLT art. 818). Cortados: "esse é um pedido para a gente
  fazer... procurar" (soa como oferta de serviço), a abertura sobre o movimento de audiências e "tá mexendo a câmera".
"""
import subprocess
from pathlib import Path

FF = r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
N = Path(r"C:\Users\prosy\Desktop\novo video")
RESC = N / "novo video da semana - atraso documentação ou valor das verbas rescisorias em caso de pedido de demissao .MOV"
HE = N / "2" / "IMG_5219.MOV"
J = lambda nome: N / "3" / f"20260123_{nome}.mp4"  # noqa: E731
AQUI = Path(__file__).resolve().parent
VIDEOS = AQUI.parent / "work" / "videos"

FALAS = {
    1: [(RESC, 15.86, 42.80), (RESC, 43.62, 46.68)],
    2: [(J("140438"), 2.22, 7.02), ("PAUSA", 3.2), (J("140229"), 0.0, 3.78), ("PAUSA", 3.0), (J("142214"), 0.90, 6.36)],
    3: [(HE, 18.62, 30.24), (HE, 98.24, 123.52)],
    4: [(HE, 65.78, 69.92), (HE, 89.36, 97.98), (HE, 47.40, 64.52)],
    5: [(HE, 123.46, 149.66), (HE, 150.08, 153.66), (HE, 156.06, 176.42), (HE, 176.78, 180.98)],
}
IMAGEM = "scale=1080:1920:flags=lanczos,fps=30,setsar=1"


def montar(n: int, trechos) -> Path:
    VIDEOS.mkdir(parents=True, exist_ok=True)
    destino = VIDEOS / f"fala-r{n}.mp4"
    entradas, filtros, rotulos = [], [], ""
    for i, t in enumerate(trechos):
        if t[0] == "PAUSA":
            d = t[1]
            entradas += ["-f", "lavfi", "-t", str(d), "-i", "color=c=0x231E1A:s=1080x1920:r=30",
                         "-f", "lavfi", "-t", str(d), "-i", "anullsrc=r=48000:cl=stereo"]
        else:
            arq, ini, fim = t
            d = round(fim - ini, 3)
            entradas += ["-ss", str(ini), "-t", str(d), "-i", str(arq)]
    # índices das entradas
    k = 0
    for i, t in enumerate(trechos):
        if t[0] == "PAUSA":
            filtros.append(f"[{k}:v]setsar=1,setpts=PTS-STARTPTS[v{i}]")
            filtros.append(f"[{k + 1}:a]asetpts=PTS-STARTPTS[a{i}]")
            k += 2
        else:
            d = round(t[2] - t[1], 3)
            filtros.append(f"[{k}:v]{IMAGEM},setpts=PTS-STARTPTS[v{i}]")
            filtros.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.03,"
                           f"afade=t=out:st={d - 0.05}:d=0.05,asetpts=PTS-STARTPTS[a{i}]")
            k += 1
        rotulos += f"[v{i}][a{i}]"
    filtros.append(f"{rotulos}concat=n={len(trechos)}:v=1:a=1[v][a]")
    subprocess.run([FF, "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    str(destino)], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(destino), "-vn", "-ac", "1", "-ar", "16000", str(AQUI / f"fala-r{n}.wav")],
                   check=True)
    return destino


if __name__ == "__main__":
    import sys
    for n in [int(a) for a in sys.argv[1:]] or FALAS:
        print("ok", montar(n, FALAS[n]))
