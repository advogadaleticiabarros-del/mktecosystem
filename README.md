# Marketing OS

Plataforma multi-tenant de marketing com IA. v1: módulo de conteúdo para o tenant
Advogada Letícia Barros — pesquisa de temas, geração de conteúdo, revisão e
aprovação. Sem publicação automática.

Design completo: `docs/superpowers/specs/2026-07-14-marketing-os-v1-design.md`

## Rodando localmente

### API

    cd apps/api
    pip install -e ".[dev]"
    cp .env.example .env   # preencher GEMINI_API_KEY e DATABASE_URL
    alembic upgrade head
    python -m app.seed.seed_leticia
    uvicorn app.main:app --reload

### Web

    cd apps/web
    npm install
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    npm run dev

## Testes

    cd apps/api && python -m pytest -v

## Deploy

- API + Postgres: Railway (`railway.json` + `apps/api/Procfile`).
- Web: Vercel, root directory `apps/web`, env var `NEXT_PUBLIC_API_URL` pointing
  to the Railway API URL.

Variáveis de ambiente necessárias em produção: `DATABASE_URL`, `JWT_SECRET`,
`GEMINI_API_KEY`.
