import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

CARROSSEIS = {
    "17-08-gestante-aviso-previo": [
        "3 situações em que a gravidez muda tudo no contrato (mesmo sem ninguém saber ainda)",
        "Durante o aviso prévio, a estabilidade vale mesmo com o contrato \"no fim\"",
        "Depois de assinar a rescisão, se a gravidez já existia, o direito continua",
        "Em contrato temporário ou de experiência, a proteção também pode alcançar você",
        "Entenda na íntegra clicando no link da bio — artigo publicado em nosso blog.",
    ],
    "18-08-familia-pensao-ex-conjuge": [
        "Pensão para genitor(a): quando existe e por quanto tempo dura",
        "A regra: pensão entre genitores é exceção, não é automática",
        "Quando costuma existir: casamentos longos, com dependência financeira real",
        "O prazo: geralmente temporário, para reorganização de vida",
        "Como pedir",
    ],
    "19-08-gestante-descoberta-apos-rescisao": [
        "Assinou e só depois descobriu a gravidez? O que ainda pode ser feito",
        "O que decide o direito é a data da concepção, não a data da descoberta",
        "A empresa não precisa saber da gravidez no momento da demissão para a proteção existir",
        "O documento assinado não é definitivo se a gravidez já existia antes",
        "O que fazer agora\n\nEntenda na íntegra clicando no link da bio — artigo publicado em nosso blog.",
    ],
    "20-08-familia-guarda-compartilhada": [
        "Guarda compartilhada: o mito da divisão 50/50 que ninguém te explica",
        "Guarda compartilhada é sobre decisão conjunta, não sobre dividir dias",
        "O tempo de convivência é definido pelo que é melhor para a criança, não por uma fórmula matemática",
        "A Justiça já pacificou: não existe obrigação de tempo igual",
        "O que isso muda na prática",
    ],
    "21-08-gestante-distrato-sem-saber": [
        "Fez um distrato grávida sem saber? Isso pode ser revisto",
        "Distrato é acordo de saída amigável, mas não apaga a estabilidade da gestante",
        "O que decide é a data da concepção, não quando o acordo foi assinado",
        "Nem você nem a empresa precisavam saber da gravidez no momento",
        "Como reverter\n\nEntenda na íntegra clicando no link da bio — artigo publicado em nosso blog.",
    ],
    "22-08-familia-pensao-provisoria-fds": [
        "O que ninguém te conta sobre pedir pensão pela primeira vez",
        "Não precisa esperar o divórcio terminar para pedir pensão provisória",
        "O valor é calculado pelo binômio necessidade da criança x possibilidade de quem paga",
        "Pensão provisória pode ser fixada logo no início do processo, sem esperar meses",
        "Documentos que ajudam a comprovar a necessidade",
    ],
    "24-08-familia-pensao-atrasada": [
        "Pensão atrasada: o que você pode fazer além de esperar",
        "Atraso de pensão é dívida, e existe caminho legal de cobrança",
        "A partir de 3 parcelas em atraso, a Justiça pode determinar prisão civil do devedor",
        "Você não precisa esperar \"boa vontade\", existe execução judicial",
        "Como iniciar a cobrança",
    ],
    "25-08-gestante-ambiente-insalubre": [
        "Trabalha em ambiente insalubre e está grávida? Veja o que muda",
        "A empresa é obrigada a afastar a gestante de atividades insalubres",
        "O afastamento pode ser para função compatível ou, sem alternativa, com pagamento garantido",
        "Isso vale mesmo que o ambiente insalubre já fizesse parte do seu trabalho antes de engravidar",
        "O que fazer se a empresa não afastar\n\nEntenda na íntegra clicando no link da bio — artigo publicado em nosso blog.",
    ],
    "26-08-familia-revisao-pensao": [
        "Pensão de valor fixado há anos: como pedir a revisão para cima",
        "As necessidades da criança mudam, o valor da pensão também pode mudar",
        "Não é preciso esperar boa vontade do genitor para pedir reajuste",
        "A Justiça avalia o binômio necessidade x possibilidade para decidir o novo valor",
        "Como dar entrada no pedido",
    ],
    "27-08-gestante-tst-contrato-temporario": [
        "TST mudou a regra: contratada só por alguns meses e grávida também tem estabilidade agora",
        "Antes: contrato temporário terminava no prazo e a empresa dizia \"não houve demissão\"",
        "Agora: o TST decidiu que essa barreira não existe mais, a proteção da gestante vale mesmo assim",
        "Vale desde 10/10/2023 e não é preciso a empresa saber da gravidez no momento",
        "Contrato temporário x contrato de experiência (são diferentes)\n\nEntenda na íntegra clicando no link da bio — artigo publicado em nosso blog.",
    ],
    "28-08-familia-guarda-unilateral": [
        "5 coisas que toda mãe separada precisa saber sobre pensão e guarda",
        "Visita e pensão são direitos separados, um não justifica o outro",
        "Ausência prolongada do outro genitor pode justificar guarda unilateral",
        "Guarda compartilhada não impede pedir revisão se a realidade mudou",
        "Quando buscar ajuda jurídica",
    ],
    "30-08-gestante-sinais-pressao-fds": [
        "3 sinais de que a empresa está tentando te empurrar pra pedir demissão grávida",
        "Mudança repentina de função ou de local de trabalho sem explicação",
        "Pressão constante, comentários sobre \"render menos\" ou \"dar trabalho\"",
        "Isolamento da equipe, exclusão de reuniões ou decisões",
        "Por que nunca pedir demissão nessa situação",
    ],
    "31-08-gestante-volta-licenca": [
        "Volta ao trabalho após a licença-maternidade: o que a empresa é obrigada a garantir",
        "Direito à mesma função ou função equivalente ao retornar",
        "Condições de trabalho não podem piorar por causa da licença",
        "A estabilidade pode continuar valendo mesmo após o retorno, dependendo da data do parto",
        "O que fazer se mudaram seu cargo sem sua concordância\n\nEntenda na íntegra clicando no link da bio — artigo publicado em nosso blog.",
    ],
}

# Regra fixa: o último slide (CTA "Procure uma advogada") sempre usa uma
# foto da própria Letícia, nunca do banco genérico de tema.
BANCO_ADVOGADA = Path(r"C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\Advogada")
FOTO_ADVOGADA_PADRAO = BANCO_ADVOGADA / "Gemini_Generated_Image_rrg4ylrrg4ylrrg4.png"

async def main():
    out_root = Path(__file__).parent / "_saida_carrosseis_calendario_agosto"
    out_root.mkdir(exist_ok=True)
    for nome, slides in CARROSSEIS.items():
        out_dir = out_root / nome
        out_dir.mkdir(exist_ok=True)
        for i, texto in enumerate(slides):
            caminho = out_dir / f"slide-{i + 1}.png"
            final = i == len(slides) - 1
            await renderizar_slide(
                texto=texto,
                indice=i,
                total=len(slides),
                identidade_visual=IDENTIDADE,
                caminho_saida=str(caminho),
                foto_path=str(FOTO_ADVOGADA_PADRAO) if final else None,
                foto_posicao="center top" if final else "center",
            )
            print(f"{nome} slide {i + 1} -> {caminho}")

if __name__ == "__main__":
    asyncio.run(main())
