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
    ("Lote 3 · novos, para aprovar (fim de ano, família e artigos mais vistos do blog)", [
        ("14-banheiro", "Recepcionista lavando banheiro", "O gerente manda a recepcionista lavar os banheiros antes de abrir; o contador mostra 300 pessoas por dia.", "Isso é função dela?", "Súmula 448, II, do TST · artigo mais visto do blog"),
        ("15-pensao", "Pensão atrasada", "Extrato de Pix da pensão: agosto pago, setembro a novembro em branco, e a mensagem “Esse mês não dá”.", "Atrasou. E agora?", "CPC, art. 528 · Súmula 309 do STJ · artigo entre os mais vistos"),
        ("16-guarda", "Guarda compartilhada", "As tarefas da semana com o filho vão sendo marcadas uma a uma: todas ficam com a mãe.", "Compartilhada?", "Código Civil, art. 1.583"),
        ("17-ferias-natal", "Natal e Ano-Novo com pais separados", "O pai avisa que vai levar o filho nas festas, e 24, 25, 31 e 1º ficam todos com ele.", "Pode levar assim?", "ECA, arts. 83 e 84"),
        ("18-decimo-terceiro", "13º salário", "As datas viram até 30/11 e 20/12, as duas parcelas caem e a segunda vem menor.", "Por que veio menor?", "Lei 4.749/1965"),
        ("19-temporario", "Temporário de fim de ano", "Chega a vaga temporária de Natal, e os direitos do temporário vão sendo marcados.", "Você recebe tudo isso?", "Lei 6.019/1974, art. 12"),
        ("20-pausa-banheiro", "Pausa para o banheiro", "O contador chega a 3 idas e o supervisor proíbe e ameaça expor o nome no quadro.", "Pode proibir?", "Constituição, arts. 1º, III, e 5º, X"),
        ("21-licenca-180", "Licença-maternidade: 120 ou 180?", "O grupo da família diz que o STF deu 180 dias para todas; o contador sobe a 180 e volta a 120.", "180 pra todas?", "ADI 7.495 · Lei 11.770/2008 · artigo entre os mais vistos"),
        ("22-fim-6x1", "Fim da escala 6x1", "A semana de 6 dias de trabalho vira 5 com 2 folgas a partir de 16/12/2026.", "Sua escala muda?", "EC 141/2026 · artigo entre os mais vistos"),
    ]),
    ("Lote 4 · temas do estilo Manchete, para aprovar", [
        ("23-gestante", "Gestante que não avisou", "O RH comunica a dispensa; 4 dias depois o exame dá positivo, com o carimbo “não avisou”.", "Tem estabilidade?", "ADCT, art. 10, II, b · Súmula 244, I, do TST"),
        ("24-assinou", "Gestante assinou o pedido de demissão", "O RH diz que é só formalidade, a assinatura é feita e aparece “sindicato: ninguém”.", "Isso vale?", "CLT, art. 500"),
        ("25-cabelo", "“Alisa o cabelo”", "A gerente pede cabelo “alinhado” e manda alisar; ela responde que o cabelo dela é assim.", "Ela pode exigir?", "Lei 9.029/1995, art. 1º"),
        ("26-amigo-secreto", "Amigo secreto obrigatório", "O grupo da firma avisa que quem não entrar terá desconto; o valor sobe até R$ 100.", "Pode descontar?", "CLT, art. 462"),
        ("27-preco", "Preço diferente no caixa", "Prateleira R$ 9,90, caixa R$ 12,90; a diferença aparece em ouro.", "Qual preço vale?", "Lei 10.962/2004, art. 5º"),
        ("28-estacionamento", "Furto no estacionamento", "A placa “não nos responsabilizamos”, a mensagem do carro arrombado e a placa riscada.", "A placa livra?", "Súmula 130 do STJ"),
        ("29-revista", "Revista íntima", "Na saída, mandam abrir a bolsa e levantar a blusa; o contador chega a 87 dias seguidos.", "Isso é rotina?", "CLT, art. 373-A, VI"),
        ("30-exame", "Falta para exame preventivo", "O chefe quer descontar o dia do exame; três dias do ano ficam dourados.", "Pode descontar?", "CLT, art. 473, XII"),
        ("31-story", "Story no dia do atestado", "Um story de praia corre na tela e o atestado de repouso aparece por cima.", "Vira prova?", "Prova digital"),
        ("32-avo", "Pensão: e a avó?", "O pai diz que não tem como pagar; o contador sobe a 8 meses sem pensão.", "E a avó?", "Súmula 596 do STJ · Código Civil, art. 1.698"),
        ("33-doar-sangue", "Folga para doar sangue", "Ela avisa que vai doar sangue e o gerente diz que vai ser falta; aparece “1 dia a cada 12 meses”.", "Mito ou realidade?", "CLT, art. 473, IV"),
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
<p class="intro">Dra. Letícia, estes são <strong>22 Reels curtos (22 segundos cada)</strong> no estilo do “23:47”. A ideia é publicar <strong>pelo menos 2 por semana</strong>. Não têm narração: só animação, textos e efeitos sonoros. Ative o som para ouvir. <strong>Nada foi publicado.</strong></p>
<div class="regras">
<div><b>Lote 3 (novo):</b> 9 Reels sobre fim de ano, família e os artigos mais vistos do blog. Os de família falam com a mãe que recebe a pensão pela criança. Os que têm artigo trazem o link no primeiro comentário.</div><div><b>Em todos:</b> o fechamento agora diz “Leia a legenda”, porque a explicação fica na legenda, e convida: “Quer ficar por dentro dos seus direitos? Clique em seguir e compartilhe com quem precisa saber disso.” A mesma frase entrou nas legendas.</div>
<div><b>O que precisamos da senhora:</b> aprovar, pedir ajuste ou descartar cada vídeo, principalmente os do lote 2. Pode comentar nesta página ou mandar mensagem citando o número do Reels.</div>
<div><b>Situações fictícias:</b> os comentários serão respondidos só em tese, sem análise de caso.</div>
</div>
{corpo}
<footer>Todas as legendas terminam com “Cada caso tem detalhes. Procure uma advogada de confiança.” e usam 5 hashtags. Efeitos sonoros com licença livre para uso comercial.</footer>
</main>'''
(AQUI / "aprovacao.html").write_text(PAGINA, encoding="utf-8")
print("ok", n)
