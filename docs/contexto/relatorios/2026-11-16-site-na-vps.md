# 16/11/2026: site advogadaleticiabarros.com.br para a VPS

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
- `docs/CONTEXTO_PROJETO.md` foi atualizado.

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
- **Não verificado:** acesso pela internet com o domínio, porque o DNS ainda aponta para a Hostinger, e o HTTPS,
  porque o certificado ainda não foi emitido.

## Decisões e porquês
- A troca foi preparada sem mexer no DNS, para que o site atual não saia do ar enquanto a VPS é testada.
- A pasta foi copiada fiel, com `lp-v3/` e as pastas de ferramentas que já estavam públicas na Hostinger. Depois,
  a pedido da Jessica, as quatro pastas de ferramentas foram bloqueadas no nginx; a `lp-v3/` continua no ar.
- A publicação na VPS vai continuar por SFTP, com um usuário preso na pasta. Assim o Orbit e os scripts mudam só
  as variáveis `BLOG_SFTP_*`, sem mexer no código. A alternativa descartada foi gravar direto na pasta, que
  exigiria mudar o código e deixaria os scripts do computador sem como publicar.

## Pendente (Jessica decide)
1. **DNS**, na conta Hostinger dona do domínio:
   - desligar a CDN da Hostinger para o site; hoje o `www` responde por `cdn.hstgr.net`, e foi esse o provável
     motivo do problema de DNS do Orbit;
   - criar o registro A `@` para `179.199.128.68`;
   - criar o registro A `www` para `179.199.128.68`, ou um CNAME para o domínio.
2. Depois que o DNS propagar, rodar na VPS
   `certbot --nginx -d advogadaleticiabarros.com.br -d www.advogadaleticiabarros.com.br`.
3. **Publicação**, na hora da troca: em `/home/orbit-src/deploy/vps/.env`, trocar as variáveis `BLOG_SFTP_*`
   pelos valores de `/root/segredos/site-leticia.env`, com `BLOG_SFTP_PATH=/domains/advogadaleticiabarros.com.br/public_html/blog/`.
   Depois, recriar o contêiner `api` e atualizar a skill `leticia-blog-artigo` e o `.env` local dos scripts.
4. Antes da troca, rodar de novo o `rsync` a partir da Hostinger, para pegar o que tiver sido publicado nesse meio
   tempo.
5. Só cancelar a hospedagem da Hostinger depois de uns dias com o site estável na VPS.

## Próxima sessão
Perguntar à Jessica se o DNS já foi trocado. Se ainda não, passar o item 1 acima.
- Se foi: refazer o download e o rsync com o mesmo procedimento deste relatório; rodar o certbot; testar com
  `curl -I https://advogadaleticiabarros.com.br`; aplicar o item 3 (publicação).
- Skills: `contexto-orbit`, `leticia-blog-artigo` (atualizar o host do SFTP nela).
