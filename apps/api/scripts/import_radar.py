"""Importa uma edição do Radar Jurídico (pesquisado/curado no ChatGPT) para o
Orbit como uma Pauta, pronta para entrar no fluxo normal de Planejamento →
Aprovação.

Não pesquisa nada sozinho — só leva o texto já pronto até a API. Rode uma vez
por pauta da semana (a manchete + até duas satélites):

    python scripts/import_radar.py radar-nr1.md \\
        --titulo "NR-1 e riscos psicossociais: o que muda após decisão do STF" \\
        --area Trabalhista --origem radar_juridico_manchete

    python scripts/import_radar.py radar-medida-protetiva.md \\
        --titulo "Medida protetiva não pode prejudicar a vítima" \\
        --area Família --origem radar_juridico_satelite

`--origem radar_juridico_manchete` é a pauta principal da semana: além do
artigo/carrossel/legenda/stories padrão, ela também gera a edição do Jornal
(a página semanal do site). `--origem radar_juridico_satelite` (default) gera
só o conjunto padrão, como qualquer outra pauta manual.

Variáveis de ambiente esperadas (mesmas do `.env` da API):
    ORBIT_API_URL       (default: http://localhost:8000)
    ORBIT_OWNER_EMAIL
    ORBIT_OWNER_PASSWORD
"""
import argparse
import os
import sys

import httpx


def _login(client: httpx.Client, email: str, password: str) -> str:
    resp = client.post("/auth/login", json={"email": email, "password": password})
    resp.raise_for_status()
    return resp.json()["access_token"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("arquivo", help="Caminho do .md/.txt com o texto do Radar (colado do ChatGPT)")
    parser.add_argument("--titulo", required=True, help="Título/manchete da pauta")
    parser.add_argument("--angulo", default="direitos", help="'direitos' ou 'sinceridade' (default: direitos)")
    parser.add_argument("--area", required=True, help="Área do direito (ex.: Trabalhista, Família)")
    parser.add_argument(
        "--origem",
        default="radar_juridico_satelite",
        choices=["radar_juridico_manchete", "radar_juridico_satelite"],
        help="manchete gera também a edição do Jornal; satelite gera só artigo/redes (default)",
    )
    args = parser.parse_args()

    with open(args.arquivo, "r", encoding="utf-8") as f:
        conteudo_bruto = f.read().strip()
    if not conteudo_bruto:
        print(f"Erro: {args.arquivo} está vazio.", file=sys.stderr)
        sys.exit(1)

    api_url = os.environ.get("ORBIT_API_URL", "http://localhost:8000")
    email = os.environ.get("ORBIT_OWNER_EMAIL")
    password = os.environ.get("ORBIT_OWNER_PASSWORD")
    if not email or not password:
        print("Erro: defina ORBIT_OWNER_EMAIL e ORBIT_OWNER_PASSWORD.", file=sys.stderr)
        sys.exit(1)

    with httpx.Client(base_url=api_url, timeout=30.0) as client:
        token = _login(client, email, password)
        resp = client.post(
            "/pautas",
            json={
                "titulo": args.titulo,
                "angulo": args.angulo,
                "area": args.area,
                "origem": args.origem,
                "conteudo_bruto": conteudo_bruto,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        resp.raise_for_status()
        pauta = resp.json()

    print(f"Pauta criada: {pauta['id']} — \"{pauta['titulo']}\" ({pauta['origem']})")
    print("Abra Planejamento → Aprovação no Orbit para gerar e revisar o conteúdo.")


if __name__ == "__main__":
    main()
