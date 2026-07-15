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
    export SEED_OWNER_PASSWORD=<escolha-uma-senha>   # Windows (PowerShell): $env:SEED_OWNER_PASSWORD="<escolha-uma-senha>"
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

**API + Postgres:** Railway (`railway.json` + `apps/api/Procfile`).
O `DATABASE_URL` que o Railway gera automaticamente para o serviço Postgres vem
como `postgresql://...` — o app precisa do driver assíncrono, então defina
manualmente na aba Variables do serviço da API:

    DATABASE_URL=postgresql+asyncpg://${{Postgres.PGUSER}}:${{Postgres.PGPASSWORD}}@${{Postgres.PGHOST}}:${{Postgres.PGPORT}}/${{Postgres.PGDATABASE}}

**Web — hospedagem compartilhada (Hostinger ou similar, sem Node.js):**
`apps/web/next.config.mjs` está configurado com `output: "export"`, então
`npm run build` gera um diretório `apps/web/out/` com HTML/CSS/JS 100% estáticos
— sem servidor Node necessário. Fluxo:

    cd apps/web
    echo "NEXT_PUBLIC_API_URL=https://sua-api.up.railway.app" > .env.local
    npm run build

O env var precisa estar definido *antes* do build (fica embutido nos arquivos
gerados, não é lido em tempo de execução). Envie o conteúdo de `apps/web/out/`
por SFTP para a pasta pública do domínio/subdomínio escolhido — mesmo fluxo já
usado para publicar o blog da Letícia.

**Web — alternativa com Node.js (Vercel ou similar):** o mesmo build também
funciona em uma plataforma que rode Node.js normalmente; root directory
`apps/web`, env var `NEXT_PUBLIC_API_URL` apontando para a URL da API no Railway.

Variáveis de ambiente necessárias em produção: `DATABASE_URL`, `JWT_SECRET`,
`GEMINI_API_KEY`, `CORS_ORIGINS` (lista separada por vírgula com a origem real
do frontend, ex.: `https://app.advogadaleticiabarros.com.br`). `ENVIRONMENT`
deve ser `production` — sem isso, a API recusa subir se `JWT_SECRET` ainda
estiver no valor padrão de desenvolvimento. `SEED_OWNER_PASSWORD` é necessária
apenas ao rodar o seed (`app.seed.seed_leticia`), não em runtime.
