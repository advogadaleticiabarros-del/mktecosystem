"""Diagramas explicativos para a tela dividida (26/10/2026, referência dos Reels de explicação que a Jessica mandou).

Cada função devolve a lista de elementos (o JSON que o engine.html anima) de um diagrama inteiro, desenhado na área do
painel (y de TOPO a BASE, coordenadas do quadro cheio, antes do encolhimento da área segura). Os tempos (`at`) vêm do
roteiro, presos às palavras da fala, então o diagrama se monta junto com a explicação.
Identidade: café e dourado, títulos em EB Garamond com itálico dourado, rótulos em Inter caixa-alta.
Uso no roteiro: {"a": ..., "painel": PAINEL, "bg": rosto_baixo(...), "els": titulo(...) + calendario(...)}.
"""
from motor import pilula, centro, carimbo, traco, texto

PAINEL = 1000          # altura do painel (px do quadro cheio)
TOPO, BASE = 175, 900  # faixa útil dentro do painel
OURO, CREME, CAFE = "#C9A962", "#FAF6F0", "#231E1A"

_ROT = "font-size:26px;font-weight:800;letter-spacing:3px;text-transform:uppercase"


def _el(html, at, top, left, w, anim="sobe", **kw):
    return {"html": html, "at": at, "anim": anim, "style": {"top": f"{top}px", "left": f"{left}px", "width": f"{w}px"}, **kw}


def titulo(linha1, at, enfase="", top=TOPO):
    """Título do painel: linha em Inter forte + linha em serifa itálica dourada (como na referência)."""
    els = [{"html": linha1, "at": at, "anim": "sobe",
            "style": {"top": f"{top}px", "left": "60px", "right": "60px", "textAlign": "center", "fontSize": "58px",
                      "fontWeight": "800", "color": CREME, "letterSpacing": "-1px"}}]
    if enfase:
        els.append(texto(f"<em>{enfase}</em>", at + .12, top + 70, size=62, left=60, right=60, align="center"))
    return els


# --------------------------------------------------------------------------- símbolo recorrente
_PECAS = [  # arcos do mostrador que acendem ao longo da série (convocação, resposta, pagamento, depósito)
    "M150 30 A120 120 0 0 1 270 150", "M270 150 A120 120 0 0 1 150 270",
    "M150 270 A120 120 0 0 1 30 150", "M30 150 A120 120 0 0 1 150 30"]


def relogio(at, cx, cy, acesas=0, rotulo="", size=300):
    """Relógio dourado do "contrato por hora": desenha o mostrador e acende `acesas` peças (0 a 4).
    Volta em vários momentos com mais peças acesas: é o fio visual da série."""
    base =('<circle class="desenha" cx="150" cy="150" r="120" stroke-opacity=".35"/>'
            '<path class="desenha" d="M150 150 L150 75"/><path class="desenha" d="M150 150 L205 180"/>')
    acesos = "".join(f'<path class="desenha" d="{p}" stroke-width="16" stroke="#F4E6BC"/>' for p in _PECAS[:acesas])
    d = traco(base + acesos, at, cy - size // 2, cx - size // 2, 300, 300, dur=1.0, stagger=.12)
    d["html"] = d["html"].replace('width="300" height="300"', f'width="{size}" height="{size}"')  # o viewBox escala o desenho
    els = [d]
    if rotulo:
        els.append(pilula(rotulo, at + .5, cy + size // 2 + 30, left=0, style=centro(520)))
    return els


# --------------------------------------------------------------------------- calendário (convocação e resposta)
def calendario(at, at_resposta, at_silencio=None, top=330):
    """Semana com a convocação 3 dias antes do trabalho e o prazo de 1 dia útil para responder (CLT 452-A, §§1º-2º)."""
    dias = ["SEG", "TER", "QUA", "QUI", "SEX"]
    w, gap, left0 = 150, 22, 540 - (5 * 150 + 4 * 22) // 2
    els = []
    for i, dia in enumerate(dias):
        destaque = {0: ("Chamado", OURO), 3: ("Trabalho", "#F4E6BC")}.get(i)
        borda = f"3px solid {destaque[1]}" if destaque else "1.5px solid rgba(201,169,98,.45)"
        fundo = "rgba(201,169,98,.16)" if destaque else "rgba(36,29,24,.7)"
        html = (f'<div style="height:170px;border-radius:20px;border:{borda};background:{fundo};display:flex;flex-direction:column;'
                f'align-items:center;justify-content:center;box-shadow:0 18px 40px rgba(0,0,0,.45)">'
                f'<div style="{_ROT};color:#E8DED1">{dia}</div>'
                f'<div class="cg" style="font-size:72px;font-weight:700;color:{CREME};line-height:1">{i + 10}</div></div>')
        els.append(_el(html, at + i * .08, top, left0 + i * (w + gap), w, anim="pop"))
        if destaque:
            els.append(_el(f'<div style="{_ROT};color:{destaque[1]};text-align:center">{destaque[0]}</div>',
                           at + .5 + (i == 3) * .2, top + 190, left0 + i * (w + gap) - 30, w + 60))
    # seta de 3 dias entre a convocação e o trabalho
    x0, x1 = left0 + w // 2, left0 + 3 * (w + gap) + w // 2
    els.append(traco(f'<path class="desenha" d="M10 70 C{(x1 - x0) // 3} 0 {2 * (x1 - x0) // 3} 0 {x1 - x0 - 10} 70"/>'
                     f'<path class="desenha" d="M{x1 - x0 - 40} 50 L{x1 - x0 - 10} 72 L{x1 - x0 + 2} 38"/>',
                     at + .7, top - 95, x0, x1 - x0 + 20, 90, dur=.8))
    els.append(pilula("3 dias de antecedência", at + .9, top - 150, left=0, style=centro(560)))
    els.append(_el(f'<div class="cartao" style="padding:26px 34px;text-align:center"><div class="cg" style="font-size:54px;font-weight:700;color:{CREME}">'
                   f'<em>1 dia útil</em> para responder</div></div>', at_resposta, top + 270, 150, 780))
    if at_silencio is not None:
        els.append(_el(f'<div style="{_ROT};color:#E8DED1;text-align:center">Se não responder, conta como recusa</div>',
                       at_silencio, top + 420, 90, 900))
    return els


# --------------------------------------------------------------------------- pagamento do período
def contracheque(ats, top=300):
    """Recibo que se monta linha a linha (CLT 452-A, §6º). `ats` = tempos de cada linha:
    [valor da hora, 13º, férias + 1/3, total]."""
    linhas = [("Valor das horas", "acertado"), ("13º proporcional", "✓"), ("Férias + ⅓", "✓")]
    els = [_el(f'<div class="papel" style="height:520px;padding:34px 44px"><div style="{_ROT};color:#8E6E2E">Recibo do período</div>'
               f'<div style="height:2px;background:#E5DCCB;margin:18px 0 0"></div></div>', ats[0] - .25, top, 170, 740, anim="pop")]
    for i, (rot, val) in enumerate(linhas):
        els.append(_el(f'<div style="display:flex;justify-content:space-between;font-size:40px;font-weight:700;color:#2B231C">'
                       f'<span>{rot}</span><span style="color:#8E6E2E">{val}</span></div>', ats[i], top + 110 + i * 92, 214, 652, anim="desliza", dx=-60))
    els.append(_el(f'<div style="height:3px;background:{OURO};margin-bottom:18px"></div>'
                   f'<div class="cg" style="font-size:50px;font-weight:700;color:#2B231C;text-align:center">'
                   f'Tudo junto, <span style="font-style:italic;color:#8E6E2E">no fim do período</span></div>',
                   ats[3], top + 390, 214, 652))
    return els


def fgts_deposito(at, top=850):
    """FGTS não vem no pagamento: é depositado (CLT 452-A, §8º)."""
    return [pilula("FGTS: depositado na conta, todo mês", at, top, left=0, style=centro(720))]


def dezembro(at, at_risco, top=330):
    """Dezembro sem o 13º de uma vez: ele já veio aos poucos."""
    els = [_el(f'<div class="cartao" style="padding:40px 30px;text-align:center"><div style="{_ROT};color:{OURO}">Dezembro</div>'
               f'<div class="cg" style="font-size:96px;font-weight:700;color:{CREME};margin-top:10px">13º salário</div></div>',
               at, top, 190, 700, anim="pop"),
           {"tipo": "risco", "at": at_risco, "largura": 560, "html": "",
            "style": {"top": f"{top + 175}px", "left": "260px", "height": "8px", "width": "0px", "background": "#E9D398",
                      "borderRadius": "4px", "boxShadow": "0 0 18px rgba(201,169,98,.8)"}}]
    els.append(texto("Ele já veio <em>aos poucos</em>", (at + at_risco) / 2, top + 330, size=64, align="center"))  # cedo o bastante para ler
    return els


# --------------------------------------------------------------------------- comparação
def comparacao(at, at_inter, top=300):
    """CLT comum x intermitente, lado a lado. Coluna da direita entra em `at_inter`."""
    def col(titulo_, itens, x, t0, cor):
        html = (f'<div class="cartao" style="padding:30px 30px;height:430px"><div style="{_ROT};color:{cor};text-align:center">{titulo_}</div>'
                + "".join(f'<div style="font-size:36px;font-weight:700;color:{CREME};margin-top:26px">{i}</div>' for i in itens) + '</div>')
        return _el(html, t0, top, x, 410, anim="pop")
    return [col("Contrato comum", ["✓ Aviso prévio", "✓ 13º no fim do ano", "✓ Férias", "✓ Rescisão"], 110, at, OURO),
            col("Intermitente", ["• Pago a cada período", "• Sem horas garantidas", "• Só quando chamado"], 560, at_inter, "#E9D398")]


# --------------------------------------------------------------------------- pergunta do público
def balao(txt, at, top=380, autor="seguidora"):
    """Pergunta em balão de comentário (estilo Instagram), com a nossa paleta."""
    html = (f'<div class="papel" style="padding:26px 32px;border-radius:28px;display:flex;gap:22px;align-items:flex-start">'
            f'<div style="flex:none;width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#C9A962,#8E6E2E)"></div>'
            f'<div><div style="font-size:26px;font-weight:800;color:#8E6E2E">{autor}</div>'
            f'<div style="font-size:42px;font-weight:700;color:#2B231C;line-height:1.2;margin-top:6px">{txt}</div></div></div>')
    return [_el(html, at, top, 120, 840, anim="pop")]


# --------------------------------------------------------------------------- todos os dias
def meses(ats, at_selo, top=300):
    """Três linhas de 22 dias úteis que se preenchem (1, 2, 3 meses) e o selo de vínculo comum."""
    els = []
    for m, t0 in enumerate(ats):
        quad = "".join('<i style="display:inline-block;width:26px;height:26px;margin:0 5px 0 0;border-radius:6px;'
                       'background:linear-gradient(180deg,#F4E6BC,#C9A962)"></i>' for _ in range(22))
        els.append(_el(f'<div style="{_ROT};color:#E8DED1;margin-bottom:12px">{m + 1}º mês</div><div>{quad}</div>',
                       t0, top + m * 120, 150, 800, anim="desliza", dx=-80))
    els.append(carimbo("Contrato comum", at_selo, top + 400, 230, rot=-6, size=70))
    return els


# --------------------------------------------------------------------------- papel x prática
def papel_pratica(at, at_pratica, top=300):
    """Balança: no papel, intermitente; na prática, funcionário de todo dia."""
    return [traco('<path class="desenha" d="M300 20 L300 360 M200 360 L400 360 M60 120 L540 60"/>'
                  '<path class="desenha" d="M60 120 L20 230 L120 230 Z M540 60 L500 170 L600 170 Z"/>', at, top, 240, 620, 380, dur=1.0),
            _el(f'<div style="{_ROT};color:#E8DED1;text-align:center">No papel</div>', at + .4, top + 250, 150, 300),
            _el(f'<div style="{_ROT};color:{OURO};text-align:center">Na prática</div>', at_pratica, top + 190, 640, 300)]
