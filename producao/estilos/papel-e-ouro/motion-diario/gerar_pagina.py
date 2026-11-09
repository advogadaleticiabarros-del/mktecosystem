"""Gera aprovacao.html (página publicada para a Dra. aprovar). Uso: python gerar_pagina.py"""
import html
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LOTES = [
    ("Lote 1 · já aprovado, com o fechamento novo", [
        ("01-atestado", "Atestado recusado", "Conversa no WhatsApp: o gerente diz que atestado do posto não vale e que vai descontar os 2 dias.", "Pode descontar?", "Lei 605/1949"),
        ("02-holerite", "Holerite sem hora extra", "O contador sobe até 46 horas a mais e o recibo sai com hora extra R$ 0,00.", "Cadê as 46 horas?", "Constituição, art. 7º, XVI"),
        ("03-ponto", "Ponto britânico", "A folha de ponto marca 08:00 às 17:00 todo dia, e o horário real aparece escrito em ouro.", "Ponto igual vale?", "Súmula 338, III, do TST"),
        ("04-demissao", "“Pede demissão”", "O chefe sugere o pedido de demissão, e os direitos perdidos são riscados um a um.", "Melhor pra quem?", "CLT, art. 484-A"),
        ("05-ferias", "Vender as férias", "O calendário de 30 dias fica dourado e depois volta a só 10 dias.", "Pode vender tudo?", "CLT, art. 143"),
        ("06-almoco", "Almoço de 20 minutos", "O cronômetro chega a 20 minutos, o chefe chama de volta e a barra mostra os 40 que faltaram.", "Isso é normal?", "CLT, art. 71"),
        ("07-experiencia", "Experiência além de 90 dias", "O contador chega ao dia 90 e o RH quer estender a experiência por mais 30 dias.", "Pode?", "CLT, arts. 445 e 451"),
    ]),
    ("Lote 2 · novos, para aprovar", [
        ("08-por-fora", "Salário por fora", "O holerite mostra R$ 1.800 e chega um Pix de R$ 1.200 “por fora”; os direitos são calculados só sobre R$ 1.800.", "Quem perde com isso?", "CLT, art. 457"),
        ("09-sem-carteira", "Sem carteira na experiência", "O contador chega ao dia 45, o RH diz que assina a carteira depois, e a carteira digital mostra “nenhum” contrato.", "Pode?", "CLT, art. 29"),
        ("10-salario-atrasado", "Salário atrasado", "A data passa do 5º dia útil, o banco avisa saldo R$ 0,00 a cada dia e o atraso aumenta.", "Até quando esperar?", "CLT, arts. 459 e 483"),
        ("11-fgts", "FGTS não depositado", "O extrato do FGTS aparece mês a mês, e os meses sem depósito são marcados em ouro.", "Cadê o depósito?", "Lei 8.036/1990, art. 15"),
        ("12-sem-folga", "Sem folga", "Duas semanas de calendário são marcadas como trabalhadas, com os domingos em ouro.", "Quando é a folga?", "Lei 605/1949, CLT art. 67, Súmula 146 do TST"),
        ("13-aviso-previo", "Aviso prévio no horário normal", "O RH manda cumprir o aviso no horário normal; o relógio volta para 15:00 e aparecem as duas opções da lei.", "Horário normal?", "CLT, art. 488"),
    ]),
]


def card(n, k, t, d, q, lei):
    leg = json.loads((AQUI / k / "legenda.json").read_text(encoding="utf-8"))["legenda"]
    return f'''<article class="ep"><div class="vid"><video src="videos/{k}-v2.mp4" controls playsinline preload="metadata"></video></div>
<div class="txt"><p class="dia">Reels {n} · {html.escape(lei)}</p><h2>{html.escape(t)}</h2><p>{html.escape(d)}</p>
<p class="q">Pergunta na tela: <mark>{html.escape(q)}</mark></p>
<details><summary>Ver a legenda do post</summary><pre>{html.escape(leg)}</pre></details></div></article>'''


corpo = ""
n = 0
for titulo, eps in LOTES:
    corpo += f'<h3 class="lote">{html.escape(titulo)}</h3>'
    for e in eps:
        n += 1
        corpo += card(n, *e)

PAGINA = f'''<title>Reels motion · aprovação</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;1,400&family=Inter:wght@400;500;600&display=swap">
<style>
/* Coluna única de leitura; cada Reels ao lado do seu texto, empilha no celular */
:root{{--bg:#1E1814;--card:#2A231E;--fg:#EFE6D9;--mute:#B8AC9C;--ouro:#D8B566;--linha:#4A3F35;
--display:'EB Garamond',Georgia,serif;--body:Inter,system-ui,sans-serif;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:400 16px/1.6 var(--body)}}
main{{max-width:940px;margin:0 auto;padding-block:48px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.fio{{height:3px;background:linear-gradient(112deg,#a57a2c,#f9efc2 27%,#a67c2e 56%,#fcf4cc 80%,#bb923f)}}
h1{{font:500 clamp(40px,7vw,64px)/1.05 var(--display);text-wrap:balance;margin:24px 0 12px}}
.intro{{max-width:65ch;color:var(--mute)}}.intro strong{{color:var(--fg)}}
.regras{{display:grid;gap:8px;margin:24px 0 24px;padding:20px 24px;border:1px solid var(--linha);border-radius:12px}}
.regras b{{color:var(--ouro);font-weight:600}}
.lote{{font:500 30px/1.2 var(--display);color:var(--ouro);margin:40px 0 0}}
.ep{{display:grid;grid-template-columns:270px 1fr;gap:32px;padding-block:36px;border-top:1px solid var(--linha)}}
.vid video{{width:100%;aspect-ratio:9/16;background:#000;border-radius:10px;display:block}}
.txt{{min-width:0;display:flex;flex-direction:column;gap:12px}}
.dia{{font:600 12px var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--ouro);margin:0}}
h2{{font:500 36px/1.1 var(--display);margin:0;text-wrap:balance}}
.txt p{{margin:0}}
mark{{background:linear-gradient(112deg,#c9a14e,#f9efc2 34%,#d8b566 52%,#cfa85a);color:#1E1814;font:italic 400 22px var(--display);padding:0 8px}}
details{{background:var(--card);border-radius:10px;padding:12px 16px}}
summary{{cursor:pointer;font-weight:500}}summary:focus-visible{{outline:2px solid var(--ouro)}}
pre{{white-space:pre-wrap;font:400 14px/1.55 var(--body);color:var(--mute);margin:12px 0 0}}
footer{{border-top:1px solid var(--linha);padding-top:24px;color:var(--mute);font-size:14px}}
@media (max-width:640px){{.ep{{grid-template-columns:1fr}}.vid{{max-width:300px}}}}
</style>
<main><div class="fio"></div>
<h1>Reels motion · aprovação</h1>
<p class="intro">Dra. Letícia, estes são <strong>13 Reels curtos (22 segundos cada)</strong> no estilo do “23:47”. A ideia é publicar <strong>pelo menos 2 por semana</strong>. Não têm narração: só animação, textos e efeitos sonoros. Ative o som para ouvir. <strong>Nada foi publicado.</strong></p>
<div class="regras">
<div><b>Novo em todos:</b> o fechamento agora diz “Leia a legenda”, porque a explicação fica na legenda, e convida: “Quer ficar por dentro dos seus direitos? Clique em seguir e compartilhe com quem precisa saber disso.” A mesma frase entrou nas legendas.</div>
<div><b>O que precisamos da senhora:</b> aprovar, pedir ajuste ou descartar cada vídeo, principalmente os do lote 2. Pode comentar nesta página ou mandar mensagem citando o número do Reels.</div>
<div><b>Situações fictícias:</b> os comentários serão respondidos só em tese, sem análise de caso.</div>
</div>
{corpo}
<footer>Todas as legendas terminam com “Cada caso tem detalhes. Procure uma advogada de confiança.” e usam 5 hashtags. Efeitos sonoros com licença livre para uso comercial.</footer>
</main>'''
(AQUI / "aprovacao.html").write_text(PAGINA, encoding="utf-8")
print("ok", n)
