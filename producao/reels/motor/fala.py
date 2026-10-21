"""Fala limpa dos Reels premium (padrão de 21/10/2026, skill leticia-reels-premium).

Monta a fala do Reel a partir do bruto gravado pela Letícia, com as regras do manual:
- as pontas de cada trecho encostam na pausa real (silencedetect a -44 dB, >= 0,25 s): nunca corta palavra;
- pausas internas encurtadas para 0,18 s; aceleração de no máximo 5% (sem mudar o tom);
- fusão de 20 ms nas emendas (o áudio de cada pedaço avança 20 ms e cruza com o seguinte, sem perder sincronia);
- pontas alinhadas aos quadros de 30 fps (imagem e som não escorregam ao somar muitos pedaços);
- cada trecho é retranscrito isolado e comparado com o texto esperado (palavra comida, sobra, repetição, muleta);
- a fala montada é medida de novo: nenhuma pausa > 0,25 s.

Uso:
  py fala.py transcrever <bruto> [saida.json]   Whisper medium com palavras; imprime só duração e nº de palavras
  py fala.py montar <falas.py> [n ...]          falas.py define SRC, FALAS = {n: [(início, fim, "texto"), ...]},
                                                 e opcionalmente VEL (padrão 1.05), VIDEOS (padrão ./videos)
                                                 e VOCABULARIO (termos do tema, ajudam o Whisper)
Um trecho com "fixo" no 4º campo mantém as pontas escolhidas à mão (não encosta na pausa).
Saídas de `montar`, em VIDEOS: fala-rN.mp4, fala-rN.wav (16 kHz, para a energia da voz do motor),
fala-rN.emendas.json (tempos das emendas, para o punch-in) e fala-rN.transcricao.json (legenda do motor).
"""
import difflib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

BIN = Path(r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin")
FF, FFPROBE = BIN / "ffmpeg.exe", BIN / "ffprobe.exe"
FPS = 30
LIMIAR = "-44dB"
LIMIAR_FRACO = "-40dB"  # acha a pausa partida por estalo (ver pausas_com_estalo)
AUDIVEL = -38.0     # dB: abaixo disso, o que o corte tirou não é fala
PAUSA_MIN = 0.25    # pausa medida (e a maior aceita na fala montada)
MARGEM = 0.09       # silêncio mantido de cada lado de uma pausa encurtada (0,18 s no total)
FOLGA = 0.5         # distância máxima para encostar a ponta do trecho na pausa real
FUSAO = 0.02
VEL = 1.05
VEL_MAX = 1.05
MULETAS = {"ne", "entao", "tipo", "ahn", "hum", "hmm", "eh", "assim"}
ARTIGOS = {"o", "a", "os", "as", "um", "uma", "uns", "umas"}   # o Whisper troca um pelo outro; corte não gera troca
CURTO = 0.08        # silêncio curto aparado nas pontas de cada trecho
IMAGEM = f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps={FPS},setsar=1"


def ff(*args) -> None:
    subprocess.run([str(FF), "-v", "error", "-y", *map(str, args)], check=True)


def duracao(arq) -> float:
    return float(subprocess.run([str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                                capture_output=True, text=True, check=True).stdout)


# --------------------------------------------------------------------------- pausas
def ler_silencios(log: str, fim: float) -> list[tuple[float, float]]:
    """Silêncios do log do silencedetect; um silêncio aberto no fim do arquivo fecha em `fim`."""
    saida, ini = [], None
    for m in re.finditer(r"silence_(start|end): (-?[\d.]+)", log):
        if m.group(1) == "start":
            ini = max(0.0, float(m.group(2)))
        elif ini is not None:
            saida.append((ini, float(m.group(2))))
            ini = None
    if ini is not None:
        saida.append((ini, fim))
    return saida


def medir_silencios(arq, minimo: float = PAUSA_MIN, limiar: str = "") -> list[tuple[float, float]]:
    r = subprocess.run([str(FF), "-hide_banner", "-nostats", "-i", str(arq), "-vn", "-af", f"silencedetect=noise={limiar or LIMIAR}:d={minimo}",
                        "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return ler_silencios(r.stderr, duracao(arq))


def pausas_com_estalo(fracas, curtos, cobertura: float = 0.6) -> list[tuple[float, float]]:
    """Pausas partidas por um estalo ou respiro: medidas a LIMIAR_FRACO aparecem inteiras, e pelo menos `cobertura`
    delas é silêncio a LIMIAR. Na fala montada viram uma pausa só, então também são encurtadas. A consoante dentro
    da palavra (o "t" de "atestado") não passa: a -40 dB ela é fala, e o silêncio de verdade cobre pouco."""
    saida = []
    for s, e in fracas:
        mudo = sum(max(0.0, min(e, ce) - max(s, cs)) for cs, ce in curtos)
        if mudo >= cobertura * (e - s):
            saida.append((s, e))
    return saida


def unir(intervalos) -> list[tuple[float, float]]:
    """Une intervalos que se sobrepõem (a pausa com estalo engloba a pausa limpa dentro dela)."""
    saida = []
    for s, e in sorted(intervalos):
        if saida and s <= saida[-1][1]:
            saida[-1] = (saida[-1][0], max(saida[-1][1], e))
        else:
            saida.append((s, e))
    return saida


def retiradas(pedacos, borda: float = 0.06) -> list[tuple[float, float]]:
    """O que o corte tira de um trecho: o miolo de cada pausa encurtada e a borda logo fora de cada ponta."""
    saida = [(round(pedacos[0][0] - borda, 3), pedacos[0][0])]
    saida += [(b, a) for (_, b), (a, _) in zip(pedacos, pedacos[1:])]
    return saida + [(pedacos[-1][1], round(pedacos[-1][1] + borda, 3))]


def pico(arq, a: float, d: float) -> float:
    """Pico (dB) de [a, a+d] do arquivo; -inf se não houver som ali."""
    r = subprocess.run([str(FF), "-hide_banner", "-nostats", "-ss", f"{max(0.0, a):.3f}", "-t", f"{d:.3f}", "-i", str(arq), "-vn",
                        "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"max_volume: (-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else float("-inf")


def pausas_longas(sil, dur: float, limite: float = PAUSA_MIN) -> list[tuple[float, float]]:
    """Pausas maiores que `limite` no meio da fala (as das pontas não contam)."""
    return [(s, e) for s, e in sil if e - s > limite and s > 0.05 and e < dur - 0.05]


# --------------------------------------------------------------------------- cortes
def _encostar(a: float, b: float, sil) -> tuple[float, float]:
    """Os tempos do Whisper erram por alguns décimos: se a ponta cai em fala e há uma pausa real a até FOLGA s,
    a ponta vai para a pausa."""
    if not any(s <= a <= e for s, e in sil):
        antes = [e for s, e in sil if a - FOLGA <= e <= a]
        if antes:
            a = max(antes) - MARGEM
    if not any(s <= b <= e for s, e in sil):
        depois = [s for s, e in sil if b <= s <= b + FOLGA]
        if depois:
            b = min(depois) + MARGEM
    return a, b


def planejar(trecho, sil) -> list[tuple[float, float]]:
    """Pedaços (início, fim) do bruto para um trecho (início, fim, texto[, "fixo"]): pontas na pausa real e
    o miolo de cada pausa interna retirado (fica MARGEM de cada lado)."""
    a, b = trecho[0], trecho[1]
    if not (len(trecho) > 3 and trecho[3] == "fixo"):
        a, b = _encostar(a, b, sil)
    partes, ini = [], a
    for s, e in sil:
        if e <= a or s >= b:
            continue
        s, e = max(s, a), min(e, b)
        if s <= a + 0.01:          # silêncio no começo do trecho: começa onde a fala começa
            ini = max(ini, e - MARGEM)
            continue
        if e >= b - 0.01:          # silêncio no fim do trecho: termina onde a fala termina
            b = s + MARGEM
            break
        if e - s > 2 * MARGEM + 0.04:
            partes.append((ini, s + MARGEM))
            ini = e - MARGEM
    partes.append((ini, b))
    return [(round(x, 3), round(y, 3)) for x, y in partes if y - x > 0.05]


def aparar(pedacos, curtos) -> list[tuple[float, float]]:
    """Tira das pontas do trecho o silêncio curto (< PAUSA_MIN, fora do planejamento), deixando MARGEM: dois desses
    somados numa emenda dariam pausa longa."""
    (a, _), (_, b) = pedacos[0], pedacos[-1]
    for s, e in curtos:
        if s <= a < e:
            a = max(a, round(e - MARGEM, 3))
        if s < b <= e:
            b = min(b, round(s + MARGEM, 3))
    saida = list(pedacos)
    saida[0] = (a, saida[0][1])
    saida[-1] = (saida[-1][0], b)
    return saida


def _no_quadro(x: float) -> float:
    return round(round(x * FPS) / FPS, 4)


# --------------------------------------------------------------------------- texto
def _limpa(w: str) -> str:
    return re.sub(r"[^\w]", "", w)


def _norm(w: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", _limpa(w).lower()) if not unicodedata.combining(c))


def _parecida(x: str, y: str) -> bool:
    return (x in ARTIGOS and y in ARTIGOS) or difflib.SequenceMatcher(None, x, y).ratio() >= 0.6


def comparar(esperado: str, ouvido: str) -> list[str]:
    """Diferenças entre o texto esperado e o ouvido, tolerando pontuação, acento e grafia do Whisper."""
    E = [w for w in esperado.split() if _norm(w)]
    O = [w for w in ouvido.split() if _norm(w)]
    e, o = [_norm(w) for w in E], [_norm(w) for w in O]
    probs = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, e, o, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace" and i2 - i1 == j2 - j1 and all(_parecida(e[i1 + k], o[j1 + k]) for k in range(i2 - i1)):
            continue
        if tag == "delete":
            probs += [f"comida: '{_limpa(E[i])}'" for i in range(i1, i2)]
        elif tag == "insert":
            for j in range(j1, j2):
                if (j > 0 and o[j] == o[j - 1]) or (j + 1 < len(o) and o[j] == o[j + 1]):
                    probs.append(f"repetição: '{_limpa(O[j])}'")
                elif o[j] in MULETAS:
                    probs.append(f"muleta: '{_limpa(O[j])}'")
                else:
                    probs.append(f"sobra: '{_limpa(O[j])}'")
        else:
            probs.append(f"trocada: '{' '.join(map(_limpa, E[i1:i2]))}' -> '{' '.join(map(_limpa, O[j1:j2]))}'")
    return probs


# --------------------------------------------------------------------------- ouvido (Whisper)
class Whisper:
    """Adaptador do Whisper local; o modelo só carrega na primeira transcrição."""

    def __init__(self, modelo: str = "medium"):
        self.modelo, self._m = modelo, None

    def transcrever(self, arq, palavras: bool = False, prompt: str = "") -> dict:
        if self._m is None:
            os.environ["PATH"] = str(BIN) + os.pathsep + os.environ["PATH"]
            import whisper
            try:
                self._m = whisper.load_model(self.modelo)
            except (RuntimeError, MemoryError) as erro:  # o medium precisa de ~3 GB livres
                if "memory" not in str(erro).lower() and not isinstance(erro, MemoryError) or self.modelo == "small":
                    raise
            if self._m is None:  # fora do except: o modelo pela metade já foi solto junto com o erro
                import gc
                gc.collect()
                print(f"AVISO: sem memória para o Whisper {self.modelo}; usando o small (feche programas e rode de novo "
                      "para conferir com o medium)", flush=True)
                self.modelo = "small"
                self._m = whisper.load_model("small")
        return self._m.transcribe(str(arq), language="pt", word_timestamps=palavras, fp16=False, initial_prompt=prompt or None)


# --------------------------------------------------------------------------- montagem
def _cortar(src: Path, pedacos, destino: Path, vel: float) -> None:
    entradas, filtros = [], []
    for i, (a, b) in enumerate(pedacos):
        d = round(b - a, 4)
        cauda = FUSAO if i + 1 < len(pedacos) else 0.0   # o áudio avança e cruza com o pedaço seguinte
        entradas += ["-ss", f"{a:.4f}", "-t", f"{d + cauda + 0.1:.4f}", "-i", str(src)]
        filtros.append(f"[{i}:v]trim=duration={d},setpts=PTS-STARTPTS,{IMAGEM}[v{i}]")
        filtros.append(f"[{i}:a]atrim=duration={d + cauda:.4f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a{i}]")
    filtros.append("".join(f"[v{i}]" for i in range(len(pedacos))) + f"concat=n={len(pedacos)}:v=1:a=0[vc]")
    atual = "a0"
    for i in range(1, len(pedacos)):
        filtros.append(f"[{atual}][a{i}]acrossfade=d={FUSAO}:c1=tri:c2=tri[x{i}]")
        atual = f"x{i}"
    filtros.append(f"[{atual}]afade=t=in:d=0.01[ac]")
    if vel != 1.0:
        filtros += [f"[vc]setpts=PTS/{vel},fps={FPS}[v]", f"[ac]atempo={vel}[a]"]
    else:
        filtros += ["[vc]null[v]", "[ac]anull[a]"]
    ff(*entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", destino)


def montar(src, trechos, destino, ouvido, vel: float = VEL, vocabulario: str = "") -> list[str]:
    """Monta a fala dos `trechos` (início, fim, texto esperado[, "fixo"]) do bruto `src` em `destino` e devolve os
    problemas encontrados (lista vazia ou só "nota: ..." = fala ok). Grava ao lado: .wav, .emendas.json e
    .transcricao.json. Troca ou palavra comida num trecho em que o corte não tirou nada audível vira nota.
    `vocabulario` (termos do tema, ex. "limbo previdenciário, INSS") ajuda o Whisper nos trechos curtos."""
    if not 1.0 <= vel <= VEL_MAX:
        raise ValueError(f"aceleração {vel} fora do limite (1.0 a {VEL_MAX})")
    src, destino = Path(src), Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    curtos = medir_silencios(src, CURTO)
    fortes = [(s, e) for s, e in curtos if e - s >= PAUSA_MIN]
    estalos = pausas_com_estalo(medir_silencios(src, limiar=LIMIAR_FRACO), curtos)
    sil, bordas = unir(fortes + estalos), unir(curtos + estalos)
    planos = [(t, [(_no_quadro(a), _no_quadro(b)) for a, b in aparar(planejar(t, sil), bordas)]) for t in trechos]
    _cortar(src, [p for _, ps in planos for p in ps], destino, vel)
    wav = destino.with_suffix(".wav")
    ff("-i", destino, "-vn", "-ac", "1", "-ar", "16000", wav)

    t, emendas, faixas = 0.0, [], []
    for _, ps in planos:
        ini = t
        for a, b in ps:
            t += (b - a) / vel
            emendas.append(round(t, 3))
        faixas.append((ini, t))
    destino.with_suffix(".emendas.json").write_text(json.dumps(emendas[:-1]), encoding="utf-8")

    problemas = [f"pausa longa: {e - s:.2f}s em {s:.2f}s" for s, e in pausas_longas(medir_silencios(wav), duracao(wav))]
    completa = ouvido.transcrever(wav, palavras=True, prompt=vocabulario)
    destino.with_suffix(".transcricao.json").write_text(json.dumps(completa, ensure_ascii=False), encoding="utf-8")
    palavras = [w for s in completa["segments"] for w in s.get("words", [])]
    with tempfile.TemporaryDirectory() as tmp:
        for i, ((trecho, ps), (ini, fim)) in enumerate(zip(planos, faixas)):
            pedaco = Path(tmp) / f"t{i}.wav"
            ff("-ss", f"{ini:.3f}", "-t", f"{fim - ini:.3f}", "-i", wav, pedaco)
            if not comparar(trecho[2], ouvido.transcrever(pedaco, prompt=vocabulario)["text"]):
                continue
            # isolado, o Whisper chuta em trecho curto; só acusa o que também diverge na fala inteira (com contexto)
            contexto = " ".join(w["word"].strip() for w in palavras if ini - 0.05 <= w["start"] < fim - 0.03)
            probs = comparar(trecho[2], contexto)
            if not probs:
                continue
            nome = f"trecho {i + 1} ({trecho[0]:.2f}-{trecho[1]:.2f})"
            audivel = max(pico(src, a, b - a) for a, b in retiradas(ps)) > AUDIVEL
            for p in probs:
                if audivel or not p.startswith(("trocada", "comida")):
                    problemas.append(f"{nome}: {p}")
                else:
                    problemas.append(f"nota: {nome}: {p} (nada audível foi cortado: provável engano do Whisper)")
    return problemas


def transcrever(bruto, saida, ouvido) -> tuple[float, int]:
    r = ouvido.transcrever(bruto, palavras=True)
    Path(saida).write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    return duracao(bruto), sum(len(s.get("words", [])) for s in r["segments"])


def _carregar(caminho: Path):
    spec = importlib.util.spec_from_file_location("falas", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv) -> int:
    if len(argv) >= 2 and argv[0] == "transcrever":
        bruto = Path(argv[1])
        saida = Path(argv[2]) if len(argv) > 2 else Path.cwd() / f"transcricao-{bruto.stem}.json"
        dur, n = transcrever(bruto, saida, Whisper())
        print(f"{bruto.name}: {dur:.1f}s, {n} palavras -> {saida}")
        return 0
    if len(argv) >= 2 and argv[0] == "montar":
        caminho = Path(argv[1]).resolve()
        cfg = _carregar(caminho)
        videos = Path(getattr(cfg, "VIDEOS", caminho.parent / "videos"))
        ouvido, falhou = Whisper(), False
        for n in [int(x) for x in argv[2:]] or list(cfg.FALAS):
            destino = videos / f"fala-r{n}.mp4"
            probs = montar(cfg.SRC, cfg.FALAS[n], destino, ouvido, getattr(cfg, "VEL", VEL), getattr(cfg, "VOCABULARIO", ""))
            emendas = json.loads(destino.with_suffix(".emendas.json").read_text())
            bruto = sum(t[1] - t[0] for t in cfg.FALAS[n])
            print(f"r{n}: {len(cfg.FALAS[n])} trechos, {len(emendas)} emendas, bruto {bruto:.1f}s -> {duracao(destino):.1f}s")
            erros = [p for p in probs if not p.startswith("nota")]
            for p in probs:
                if p.startswith("nota"):
                    print(f"  {p}")
            print("  fala ok" if not erros else "\n".join(f"  {p}" for p in erros))
            falhou |= bool(erros)
        return 1 if falhou else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
