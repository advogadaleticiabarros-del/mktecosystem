"""Transforma o painel "Presença no Google" numa lista de melhorias, da mais urgente para a menos.

Interface: `diagnosticar(painel, hoje)` devolve uma lista de recomendações:
`{chave, area, prioridade, titulo, motivo, acao, itens, link, aplicar}`.
- `chave` é estável entre coletas (é por ela que a usuária marca "feita" ou "ignorar");
- `aplicar` diz o que o Orbit faz sozinho a partir da recomendação ("editar_perfil",
  "responder_avaliacoes", "criar_post", "enviar_fotos") ou None se é tarefa manual.
Só lê o painel: nenhuma chamada externa, nenhuma escrita.
"""
import re
import unicodedata
from datetime import date, datetime, timedelta

from app.services.conformidade_oab import verificar_texto_oab

ORDEM = {"alta": 0, "media": 1, "baixa": 2}
NOMES_SECAO = {
    "perfil": "dados do Perfil", "atributos": "atributos do Perfil", "desempenho": "desempenho do Perfil",
    "palavras_chave": "palavras buscadas", "avaliacoes": "avaliações", "posts": "posts do Google",
    "midia": "fotos do Perfil", "verificacao": "verificação do Perfil", "botoes": "botões do Perfil",
    "analytics": "Google Analytics", "search_console": "Search Console", "site": "checagem do site",
}
LETRAS_PT = set("abcdefghijklmnopqrstuvwxyzáàâãéêíóôõúüç")


def _sem_acento(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


def _dias_desde(iso: str | None, hoje: date) -> int | None:
    if not iso:
        return None
    return (hoje - datetime.fromisoformat(iso.replace("Z", "+00:00")).date()).days


def palavra_suspeita(palavra: str) -> bool:
    """Erro de digitação provável: letra fora do português ou vogal acentuada dobrada ("assedíio")."""
    minuscula = palavra.lower()
    if any(c.isalpha() and c not in LETRAS_PT for c in minuscula):
        return True
    return any(a != b and _sem_acento(a) == _sem_acento(b) for a, b in zip(minuscula, minuscula[1:]))


def _rec(chave, area, prioridade, titulo, motivo, acao, *, itens=None, link=None, aplicar=None) -> dict:
    return {"chave": chave, "area": area, "prioridade": prioridade, "titulo": titulo, "motivo": motivo,
            "acao": acao, "itens": itens or [], "link": link, "aplicar": aplicar}


def _configuracao(erros: dict) -> list[dict]:
    recs = []
    desativadas = {s: e for s, e in erros.items() if e["tipo"] == "api_desativada"}
    for secao, erro in desativadas.items():
        recs.append(_rec(
            f"config-ativar-{secao}", "configuracao", "alta",
            f"Ativar a API de {NOMES_SECAO.get(secao, secao)} no Google Cloud",
            "Sem ela o Orbit não consegue ler essa parte.",
            "Abra o link, confira o projeto 462973861302 e clique em \"Ativar\". Os dados aparecem na próxima atualização.",
            link=erro.get("ativar_em"),
        ))
    if any(e["tipo"] == "reconectar" for e in erros.values()):
        secoes = [NOMES_SECAO.get(s, s) for s, e in erros.items() if e["tipo"] == "reconectar"]
        recs.append(_rec(
            "config-reconectar", "configuracao", "alta", "Reconectar o Google para liberar novas permissões",
            "A conexão atual não tem permissão para: " + ", ".join(secoes) + ".",
            "Visão Geral → Desconectar → Conectar, marcando todas as caixas de permissão.",
        ))
    for secao, erro in erros.items():
        if erro["tipo"] == "sem_acesso" and secao in ("analytics", "search_console"):
            recs.append(_rec(
                f"config-acesso-{secao}", "configuracao", "alta",
                f"Dar acesso ao {NOMES_SECAO[secao]} para a conta conectada",
                erro.get("mensagem", ""),
                "Adicione o e-mail da conta conectada como Leitor (Analytics) ou usuário (Search Console).",
            ))
    return recs


def _perfil(painel: dict) -> list[dict]:
    perfil = painel.get("perfil")
    if not perfil:
        return []
    recs = []
    site = perfil.get("site") or ""
    if site and "utm_" not in site:
        recs.append(_rec(
            "perfil-site-utm", "perfil", "media", "Rastrear as visitas que vêm do Perfil do Google",
            f"O link do site no Perfil ({site}) não tem marcação, então o Analytics mistura essas visitas com as do Google comum.",
            "Trocar o link do site no Perfil para a versão com marcação (utm).",
            itens=[f"https://{painel.get('dominio') or 'seusite.com.br'}/?utm_source=google&utm_medium=organic&utm_campaign=perfil-empresa"],
            aplicar="editar_perfil",
        ))
    descricao = perfil.get("descricao") or ""
    problemas = verificar_texto_oab(descricao)
    if problemas:
        recs.append(_rec(
            "perfil-descricao-oab", "perfil", "alta" if any(p["nivel"] == "bloqueia" for p in problemas) else "media",
            "Revisar a descrição do Perfil pelas regras da OAB",
            "Trechos que pedem atenção na descrição atual.",
            "Ajustar a descrição (o Orbit sugere um texto e você aprova antes de ir para o Google).",
            itens=[f"\"{p['trecho']}\": {p['motivo']}" for p in problemas], aplicar="editar_perfil",
        ))
    cidade = perfil.get("cidade") or ""
    if cidade and _sem_acento(cidade) not in _sem_acento(descricao):
        recs.append(_rec(
            "perfil-descricao-cidade", "perfil", "media", f"Citar {cidade} na descrição do Perfil",
            "A busca local usa a descrição para entender onde o escritório atende. A cidade não aparece nela.",
            f"Incluir {cidade} e a região atendida de forma natural na descrição.", aplicar="editar_perfil",
        ))
    if len(descricao) < 450:
        recs.append(_rec(
            "perfil-descricao-curta", "perfil", "baixa", "Aproveitar os 750 caracteres da descrição",
            f"A descrição tem {len(descricao)} caracteres.",
            "Completar com as áreas de atuação e como é o atendimento.", aplicar="editar_perfil",
        ))
    servicos = perfil.get("servicos") or []
    suspeitos = sorted({
        palavra for s in servicos for palavra in re.findall(r"\w+", f"{s['nome']} {s['descricao']}")
        if palavra_suspeita(palavra)
    })
    if suspeitos:
        recs.append(_rec(
            "perfil-servicos-digitacao", "perfil", "alta", "Corrigir erros de digitação nos serviços",
            "Erro de digitação no Perfil passa descuido para quem pesquisa e atrapalha a busca por esses termos.",
            "Corrigir as palavras abaixo.", itens=suspeitos, aplicar="editar_perfil",
        ))
    sem_descricao = [s["nome"] for s in servicos if not s.get("descricao")]
    if sem_descricao:
        recs.append(_rec(
            "perfil-servicos-sem-descricao", "perfil", "media", "Descrever os serviços que estão só com o nome",
            "Serviço com descrição ajuda o Google a mostrar o Perfil para buscas sobre aquele assunto.",
            "Escrever 1 ou 2 frases para cada um (o Orbit sugere).", itens=sem_descricao, aplicar="editar_perfil",
        ))
    return recs


def _avaliacoes(painel: dict) -> list[dict]:
    avaliacoes = painel.get("avaliacoes")
    if not avaliacoes:
        return []
    recs = []
    if avaliacoes["sem_resposta"]:
        recs.append(_rec(
            "avaliacoes-sem-resposta", "avaliacoes", "alta",
            f"Responder {avaliacoes['sem_resposta']} avaliação(ões) sem resposta",
            "Responder avaliações é um dos sinais que o Google usa no ranking local e mostra cuidado para quem lê.",
            "O Orbit escreve a resposta no tom da Dra. e você aprova.", aplicar="responder_avaliacoes",
        ))
    if avaliacoes["ultimos_30d"] == 0:
        recs.append(_rec(
            "avaliacoes-ritmo", "avaliacoes", "media", "Pedir avaliações a clientes satisfeitos",
            "Nenhuma avaliação nova nos últimos 30 dias. Avaliações recentes pesam no ranking local.",
            "Enviar o link de avaliação para clientes com caso encerrado (sem oferecer nada em troca).",
            link=(painel.get("perfil") or {}).get("link_avaliar"),
        ))
    if avaliacoes["media"] is not None and avaliacoes["media"] < 4.5:
        recs.append(_rec(
            "avaliacoes-media", "avaliacoes", "media", "Subir a nota média",
            f"A nota média está em {avaliacoes['media']}.",
            "Responder com cuidado as notas baixas e pedir avaliação a quem foi bem atendido.",
        ))
    return recs


def _conteudo(painel: dict, hoje: date) -> list[dict]:
    recs = []
    posts = painel.get("posts")
    if posts is not None:
        dias = _dias_desde(posts.get("ultimo_em"), hoje)
        if dias is None or dias > 7:
            recs.append(_rec(
                "posts-frequencia", "conteudo", "media", "Publicar no Perfil do Google toda semana",
                "Último post há " + (f"{dias} dias." if dias is not None else "muito tempo (nenhum post encontrado)."),
                "Agendar 1 post por semana pelo Orbit, ligado a um artigo do blog.", aplicar="criar_post",
            ))
    midia = painel.get("midia")
    if midia is not None:
        if midia["fotos"] < 15:
            recs.append(_rec(
                "fotos-poucas", "conteudo", "media", "Colocar mais fotos no Perfil",
                f"O Perfil tem {midia['fotos']} foto(s). Perfis com fotos variadas (fachada, sala, equipe) recebem mais cliques.",
                "Enviar fotos do escritório, da Dra. e da recepção pelo Orbit.", aplicar="enviar_fotos",
            ))
        dias = _dias_desde(midia.get("ultima_em"), hoje)
        if dias is not None and dias > 30:
            recs.append(_rec(
                "fotos-recentes", "conteudo", "baixa", "Renovar as fotos do Perfil",
                f"A foto mais recente é de {dias} dias atrás.", "Enviar 1 ou 2 fotos novas por mês.", aplicar="enviar_fotos",
            ))
    botoes = painel.get("botoes")
    if botoes is not None and not any(b["tipo"] in ("APPOINTMENT", "ONLINE_APPOINTMENT") for b in botoes):
        recs.append(_rec(
            "botoes-agendar", "perfil", "baixa", "Adicionar o botão \"Agendar\" no Perfil",
            "Sem esse botão, quem quer marcar horário precisa ligar ou procurar o site.",
            "Cadastrar o link de agendamento (WhatsApp ou página de contato).", aplicar="editar_perfil",
        ))
    return recs


def _desempenho(painel: dict) -> list[dict]:
    recs = []
    desempenho = painel.get("desempenho")
    if desempenho:
        atual = desempenho["totais_30d"]["buscas"] + desempenho["totais_30d"]["maps"]
        anterior = desempenho["totais_30d_anterior"]["buscas"] + desempenho["totais_30d_anterior"]["maps"]
        if anterior >= 30 and atual < anterior * 0.8:
            recs.append(_rec(
                "desempenho-queda", "busca", "alta", "As aparições do Perfil caíram",
                f"{atual} aparições nos últimos 30 dias contra {anterior} nos 30 anteriores ({round((atual / anterior - 1) * 100)}%).",
                "Conferir se algo mudou no Perfil (categoria, horário, endereço) e retomar posts e respostas.",
            ))
    palavras = painel.get("palavras_chave") or []
    titulo = (painel.get("perfil") or {}).get("titulo", "")
    marca = {p for p in re.findall(r"\w+", _sem_acento(titulo.split("|")[0])) if len(p) > 3}
    if palavras and marca:
        de_marca = [p for p in palavras if marca & set(re.findall(r"\w+", _sem_acento(p["termo"])))]
        if len(de_marca) / len(palavras) > 0.6:
            recs.append(_rec(
                "palavras-so-marca", "busca", "media", "Ser encontrada por assunto, não só pelo nome",
                f"{len(de_marca)} das {len(palavras)} buscas que levaram ao Perfil têm o nome da Dra. Quem ainda não a conhece não está chegando.",
                "Usar os termos dos assuntos (gestante, demissão, rescisão) nos serviços, na descrição e nos posts.",
                itens=[p["termo"] for p in palavras if p not in de_marca][:10], aplicar="editar_perfil",
            ))
    gsc = painel.get("search_console")
    if gsc:
        quase = [c for c in gsc["consultas"] if 4 <= c["posicao"] <= 20 and c["impressoes"] >= 10]
        quase.sort(key=lambda c: -c["impressoes"])
        if quase:
            recs.append(_rec(
                "gsc-quase-primeira-pagina", "busca", "alta", "Buscas em que o site está quase no topo",
                "O site aparece entre a 4ª e a 20ª posição nessas buscas. Um ajuste no conteúdo pode levar ao topo.",
                "Reforçar o artigo que responde cada busca (título, primeiro parágrafo, FAQ) ou escrever um artigo novo.",
                itens=[f"{c['termo']}: posição {c['posicao']}, {c['impressoes']} aparições" for c in quase[:8]],
            ))
        ctr_baixo = [p for p in gsc["paginas"] if p["impressoes"] >= 100 and p["ctr"] < 1]
        if ctr_baixo:
            recs.append(_rec(
                "gsc-ctr-baixo", "busca", "media", "Páginas que aparecem muito e recebem poucos cliques",
                "O título e a descrição dessas páginas não estão convencendo quem vê no Google.",
                "Reescrever o título e a descrição (meta description) de cada uma.",
                itens=[f"{p['pagina']}: {p['impressoes']} aparições, {p['ctr']}% de cliques" for p in ctr_baixo[:8]],
            ))
    return recs


def _site_e_ia(painel: dict) -> list[dict]:
    recs = []
    site = painel.get("site")
    if site:
        if site["paginas_sem_analytics"]:
            recs.append(_rec(
                "site-sem-analytics", "site", "alta", "Páginas sem o código do Google Analytics",
                "As visitas nessas páginas não são contadas em lugar nenhum.",
                "Colocar o código do Analytics nessas páginas.", itens=site["paginas_sem_analytics"],
            ))
        if site["paginas_sem_descricao"]:
            recs.append(_rec(
                "site-sem-descricao", "site", "media", "Páginas sem descrição para o Google",
                "Sem descrição (meta description), o Google e as IAs montam um resumo por conta própria.",
                "Escrever uma descrição de até 155 caracteres para cada uma.", itens=site["paginas_sem_descricao"],
            ))
        if site["robos_ia_bloqueados"]:
            recs.append(_rec(
                "site-robos-ia", "ia", "alta", "Robôs de IA bloqueados no robots.txt",
                "Esses assistentes não podem ler o site, então não citam a Dra.",
                "Liberar esses robôs no robots.txt.", itens=site["robos_ia_bloqueados"],
            ))
        if not site["llms_txt"]:
            recs.append(_rec(
                "site-llms-txt", "ia", "media", "Criar o arquivo llms.txt",
                "É um resumo do site feito para assistentes de IA lerem.", "Publicar /llms.txt com as áreas e os artigos principais.",
            ))
        schemas = set(site["home"]["schemas"])
        if not schemas & {"LegalService", "Attorney", "LocalBusiness", "ProfessionalService"}:
            recs.append(_rec(
                "site-schema", "ia", "media", "Identificar o escritório com dados estruturados",
                "A página inicial não diz em linguagem de máquina que é um escritório de advocacia (schema LegalService).",
                "Adicionar o bloco LegalService com nome, OAB, endereço, telefone e áreas.",
            ))
    analytics = painel.get("analytics")
    if analytics and analytics["ia"]["total_90d"] == 0:
        recs.append(_rec(
            "ia-sem-visitas", "ia", "media", "As IAs ainda não mandam visitas para o site",
            "Nenhuma visita vinda de ChatGPT, Gemini, Perplexity ou Copilot nos últimos 90 dias.",
            "Artigos com perguntas e respostas diretas, autoria com OAB visível e páginas por assunto aumentam as citações.",
        ))
    return recs


def diagnosticar(painel: dict, hoje: date | None = None) -> list[dict]:
    hoje = hoje or date.today()
    recs = (
        _configuracao(painel.get("erros", {}))
        + _perfil(painel)
        + _avaliacoes(painel)
        + _conteudo(painel, hoje)
        + _desempenho(painel)
        + _site_e_ia(painel)
    )
    return sorted(recs, key=lambda r: ORDEM[r["prioridade"]])
