# Migrar o Orbit para a VPS (Hostinger, `srv1921337.hstgr.cloud`)

Guia passo a passo pra sair do Railway e rodar o Orbit na mesma VPS onde já
está o CRM jurídico (`/home/crma`, porta 3001, Node + MySQL local), sem tocar
nesse serviço. O Orbit sobe em containers Docker isolados (Postgres próprio,
nada de MySQL) e o painel web é servido como arquivo estático pelo nginx que
já roda na máquina — igual ao blog, só que local em vez de por SFTP.

Domínios: `orbit.advogadaleticiabarros.com.br` (painel) e
`api.orbit.advogadaleticiabarros.com.br` (API). Portas já ocupadas na VPS
(não usar): 80/443 (nginx), 22 (ssh), 3001 (CRM), 3306/33060 (MySQL local). A
API do Orbit fica em `127.0.0.1:8010`, só acessível via nginx.

## 0. DNS

No painel de DNS do domínio (Hostinger → Domínios → `advogadaleticiabarros.com.br`
→ Gerenciador de DNS), crie dois registros A apontando para `179.199.128.68`:

- `orbit` → 179.199.128.68
- `api.orbit` → 179.199.128.68

Propagação pode levar alguns minutos a poucas horas.

## 1. Instalar Docker na VPS

```bash
apt update
apt install -y docker.io docker-compose-plugin
systemctl enable --now docker
```

## 2. Trazer o código pra VPS

```bash
cd /home
git clone <url-do-repo-mktecosystem> orbit-src
cd orbit-src
```

(Repo privado: gere um token de acesso pessoal no GitHub ou use uma deploy
key só de leitura — não coloque credenciais direto na URL do `git clone`.)

## 3. Configurar variáveis de ambiente

```bash
cd deploy/vps
cp .env.example .env
nano .env
```

Preencha com os mesmos valores que já estão nas Variables do serviço
`orbit-api` no Railway (JWT_SECRET, GEMINI_API_KEY, RESEND_API_KEY,
GROQ_API_KEY, TAVILY_API_KEY, ENCRYPTION_KEY, META_*, GOOGLE_*,
BLOG_SFTP_PASSWORD) — copie exatamente os mesmos valores, não gere novos
(principalmente `ENCRYPTION_KEY` e `JWT_SECRET`: trocar invalida sessões e
qualquer dado que dependa deles). Escolha uma senha nova só para
`POSTGRES_PASSWORD` (não existia antes) e repita o mesmo valor dentro de
`DATABASE_URL`.

## 4. Migrar os dados do Postgres do Railway

Pegue a `DATABASE_URL` pública do Postgres no Railway (aba Variables do
serviço Postgres, aponta pra fora do Railway, não a interna `postgres.railway.internal`).

Na sua máquina local (ou na VPS, se tiver `pg_dump`/`pg_restore` de uma versão
compatível com Postgres 16):

```bash
pg_dump "postgresql://usuario:senha@host-publico-railway:porta/railway" -Fc -f orbit.dump
```

Suba só o banco primeiro (ainda sem a API, pra restaurar num banco vazio):

```bash
cd deploy/vps
docker compose up -d db
# espere alguns segundos o Postgres inicializar
docker cp orbit.dump orbit-vps-db-1:/tmp/orbit.dump
docker compose exec db pg_restore -U orbit -d orbit --no-owner /tmp/orbit.dump
```

(Nome do container pode variar — confira com `docker compose ps`.)

## 5. Subir a API

```bash
cd deploy/vps
docker compose up -d --build
docker compose logs -f api   # confirma "alembic upgrade head" sem erro e uvicorn no ar
```

Teste local antes de expor: `curl http://127.0.0.1:8010/health` deve
responder `{"status":"ok"}`.

## 6. Buildar e publicar o painel web (estático)

A VPS já tem Node (é o runtime do CRM), então dá pra buildar direto nela:

```bash
cd /home/orbit-src/apps/web
echo "NEXT_PUBLIC_API_URL=https://api.orbit.advogadaleticiabarros.com.br" > .env.local
npm install
npm run build
mkdir -p /var/www/orbit-web
cp -r out/* /var/www/orbit-web/
```

## 7. Configurar o nginx

```bash
cp /home/orbit-src/deploy/vps/nginx-orbit-web.conf /etc/nginx/sites-available/orbit-web
cp /home/orbit-src/deploy/vps/nginx-orbit-api.conf /etc/nginx/sites-available/orbit-api
ln -s /etc/nginx/sites-available/orbit-web /etc/nginx/sites-enabled/orbit-web
ln -s /etc/nginx/sites-available/orbit-api /etc/nginx/sites-enabled/orbit-api
nginx -t && systemctl reload nginx
certbot --nginx -d orbit.advogadaleticiabarros.com.br -d api.orbit.advogadaleticiabarros.com.br
```

(Se `certbot` não estiver instalado: `apt install -y certbot python3-certbot-nginx`.)

## 8. Validar tudo antes de desligar o Railway

- `https://api.orbit.advogadaleticiabarros.com.br/health` → `{"status":"ok"}`
- `https://orbit.advogadaleticiabarros.com.br` abre a tela de login, login
  funciona com as credenciais existentes (prova que o banco migrado está
  certo)
- Gerar/aprovar um conteúdo de teste, conferir que o agendamento automático
  aparece no Calendário
- Rodar o CLI `import_radar.py` uma vez apontando `ORBIT_API_URL` pra
  `https://api.orbit.advogadaleticiabarros.com.br`

## 9. Trocar as referências que hoje apontam pro Railway

Estes arquivos têm a URL do Railway hardcoded (formulários de captação) e
precisam apontar pra API nova antes do cutover final:

- `apps/api/app/templates/blog_artigo.html`
- `apps/api/app/templates/jornal.html`
- `lp/guia-gestante-clt.html`
- `lp/guia-direitos-gestante-trabalhadora.html`

Troque `https://orbit-api-production-0029.up.railway.app` por
`https://api.orbit.advogadaleticiabarros.com.br` nos quatro, faça commit, e
publique de novo o blog (o publicador do Orbit já reenvia `blog_artigo.html`
a cada novo artigo — os artigos já publicados no ar não têm o form corrigido
retroativamente, só os próximos; se quiser corrigir os já publicados, é reenviar
manualmente por SFTP). Os dois `lp/*.html` são publicados manualmente — reenvie
por SFTP depois de editar.

Também atualize `CORS_ORIGINS` no `.env` da VPS se algum outro domínio novo
precisar chamar a API.

## 10. Desligar o Railway

Só depois do item 8 validado por pelo menos alguns dias:

```bash
railway down --service orbit-api
railway down --service orbit-web
```

Ou apague os serviços direto no painel do Railway.

## Manutenção

- Atualizar código: `cd /home/orbit-src && git pull && cd deploy/vps &&
  docker compose up -d --build`
- Ver logs: `docker compose logs -f api`
- Backup do Postgres: `docker compose exec db pg_dump -U orbit orbit -Fc -f /tmp/backup.dump`
  (depois `docker cp` pra fora do container)
