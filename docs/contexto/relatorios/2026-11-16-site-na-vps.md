# 16/11/2026: site advogadaleticiabarros.com.br para a VPS (concluído)

## Pedido
"Preciso colocar o meu site hospedado dentro da minha VPS". Site escolhido: advogadaleticiabarros.com.br (Hostinger
compartilhada). A Jessica informou que o domínio não tem e-mail ("pode seguir").

## Feito
- O `public_html` inteiro foi baixado da Hostinger por SFTP, feito a partir do contêiner `vps-api-1`, que já tem as credenciais. São
  369 arquivos, 38 MB, tudo estático e sem PHP. A cópia bruta está em `/root/site_leticia_hostinger` na VPS `179.199.128.68`.
- Pasta do site na VPS: `/home/siteleticia/domains/advogadaleticiabarros.com.br/public_html`, a mesma estrutura da
  Hostinger. Primeiro a cópia foi para `/var/www/advogadaleticiabarros.com.br`; essa pasta foi removida depois da mudança.
- **Usuário SFTP `siteleticia`**, criado com autorização da Jessica ("o que for recomendado"):
  - só SFTP, preso em `/home/siteleticia` pela configuração `/etc/ssh/sshd_config.d/70-siteleticia-sftp.conf`;
  - a senha está em `/root/segredos/site-leticia.env`, que só o root lê; o valor fica `<REMOVIDO>` aqui;
  - a sessão abre em `/`, então os caminhos relativos `domains/advogadaleticiabarros.com.br/public_html/...` dos
    scripts continuam valendo.
- As pastas `agents/`, `mcps/`, `squads/` e `_expxagents/` foram tiradas do ar a pedido da Jessica: o nginx devolve
  404. Os arquivos continuam na pasta.
- A configuração do nginx é `deploy/vps/nginx-site-leticia.conf`, instalada como
  `/etc/nginx/sites-available/site-leticia` e ativada. Ela reproduz o `.htaccess`: os 2 redirecionamentos 301 do
  blog, o `/voto` 302, o bloqueio de arquivos ocultos menos `.well-known`, o gzip e o cache por tipo. Também manda
  `www` para o endereço sem www.
- **Publicação trocada para a VPS**, pedido da Jessica: "troque tudo que depende de lá".
  - Antes da troca, o site foi baixado de novo da Hostinger. Não havia conteúdo novo, só dono e permissões.
  - O `.env` do Orbit (`/home/orbit-src/deploy/vps/.env`) foi trocado: `BLOG_SFTP_*` agora apontam para a VPS
    (`siteleticia`, porta 22, `BLOG_SFTP_PATH=/domains/advogadaleticiabarros.com.br/public_html/blog/`).
  - O contêiner `api` foi recriado.
  - Backup do `.env` anterior: `/root/segredos/orbit-env-antes-site-vps-20261116.env`. As credenciais antigas da
    Hostinger ficaram em `/root/segredos/hostinger-sftp-antigo.env`.
  - Isso cobre tudo que publica no site, porque todos usam essas variáveis dentro do contêiner:
    - `blog_publisher.py`;
    - `central_google._site_padrao`;
    - `apps/api/scripts/*`;
    - `producao/**/publicar_*.py`.
  - O `.github/workflows/deploy-frontend.yml` e o `scripts/deploy_hostinger.py` são do painel antigo do Orbit, que
    está aposentado e só roda à mão; ficaram como estavam.
  - Também foram atualizados a skill `leticia-blog-artigo`, o `deploy/vps/.env.example` e o
    `docs/CONTEXTO_PROJETO.md`.

## Verificado
- `nginx -t` passou, e o reload foi feito sem afetar os sites do CRM e do Orbit.
- Testes com curl na VPS usando o cabeçalho `Host:` (resultados reais):
  - `/`, `/blog/`, `/bio/`, LP, `/sobre.html`, `robots.txt`, `sitemap.xml` e `llms.txt` respondem 200.
  - `/bio` responde 301 para `/bio/`.
  - Os redirecionamentos do `.htaccess` funcionam.
  - `/.git/config` e `/.htaccess` respondem 404.
  - O gzip e o Cache-Control estão ativos.
- O SFTP foi testado a partir do contêiner `vps-api-1`: gravou e apagou um arquivo de teste no `blog/`, a sessão
  abre em `/` e tentar rodar comandos dá erro, ou seja, o acesso a comandos está bloqueado.
- As quatro pastas respondem 404, e as páginas do site continuam respondendo 200.
- Depois da troca, o Orbit foi testado com o próprio código, dentro do contêiner:
  - leu `blog/index.html` (120 KB) e `sitemap.xml` (11 KB) da VPS;
  - gravou `blog/_teste_orbit.txt`, que o nginx serviu, e o arquivo foi apagado em seguida;
  - `_site_padrao()` aponta para `/domains/advogadaleticiabarros.com.br/public_html`;
  - o contêiner `api` está de pé.
- **No ar pela VPS desde 16/11/2026.** A Jessica trocou o DNS:
  - CDN da Hostinger desligada e retirada da ativação automática;
  - registros A `@` e `www` → `179.199.128.68`, TTL 300;
  - sem AAAA, CNAME ou ALIAS nesses nomes.
- Conferências depois da troca:
  - O Google e a Cloudflare respondem só o IPv4 da VPS, sem AAAA.
  - O servidor de DNS do domínio (`ns1.dns-parking.com`) confirma: só o IPv4.
- O `certbot --nginx` emitiu o certificado Let's Encrypt para o domínio e o `www`, válido até 14/02/2027. O
  `certbot.timer` está ativo e o `renew --dry-run` deu certo.
- Teste pela internet, a partir do PC da Jessica, forçando IPv4:
  - páginas, blog, `/bio/`, LP e sitemap respondem 200;
  - `/voto` responde 302, e o artigo antigo responde 301;
  - `.git`, `agents/`, `mcps/` e páginas inexistentes respondem 404;
  - http e www levam a https sem www;
  - o servidor que responde é o `nginx` da VPS.
- Observação: o provedor de internet do PC ainda tinha em cache o IPv6 antigo da Hostinger (servidor LiteSpeed,
  com o mesmo conteúdo). Esse cache deve expirar sozinho em algumas horas. Não é erro de configuração.

## Decisões e porquês
- A troca foi preparada sem mexer no DNS, para que o site atual não saia do ar enquanto a VPS é testada.
- A pasta foi copiada fiel, com `lp-v3/` e as pastas de ferramentas que já estavam públicas na Hostinger. Depois,
  a pedido da Jessica, as quatro pastas de ferramentas foram bloqueadas no nginx; a `lp-v3/` continua no ar.
- A publicação na VPS vai continuar por SFTP, com um usuário preso na pasta. Assim o Orbit e os scripts mudam só
  as variáveis `BLOG_SFTP_*`, sem mexer no código. A alternativa descartada foi gravar direto na pasta, que
  exigiria mudar o código e deixaria os scripts do computador sem como publicar.

## Pendente (Jessica decide)
1. ~~**DNS**~~, feito pela Jessica em 16/11/2026, na conta Hostinger dona do domínio:
   - desligar a CDN da Hostinger para o site; hoje o `www` responde por `cdn.hstgr.net`, e foi esse o provável
     motivo do problema de DNS do Orbit;
   - criar o registro A `@` para `179.199.128.68`;
   - criar o registro A `www` para `179.199.128.68`, ou um CNAME para o domínio.
2. ~~Certificado HTTPS~~: emitido em 16/11/2026, com renovação automática.
3. ~~Publicação~~: feita em 16/11/2026, ver Feito. Para voltar à Hostinger, restaurar o backup do `.env` e rodar `docker compose up -d api`.
4. A Hostinger não recebe mais publicações. Não é preciso copiar de novo de lá.
5. Só cancelar a hospedagem da Hostinger depois de uns dias com o site estável na VPS.

## Próxima sessão
A migração está concluída. Daqui a uns dias, confirmar com a Jessica se está tudo estável e se ela quer cancelar
a hospedagem compartilhada da Hostinger. O domínio continua na Hostinger e deve ser mantido lá.
- Para publicar, use a skill `leticia-blog-artigo`; ela já aponta para a VPS.
- A configuração final do nginx, já com o HTTPS do certbot, está em `deploy/vps/nginx-site-leticia.conf`.
