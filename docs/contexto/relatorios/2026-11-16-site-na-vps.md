# 16/11/2026: site advogadaleticiabarros.com.br para a VPS

## Pedido
"Preciso colocar o meu site hospedado dentro da minha VPS". Site escolhido: advogadaleticiabarros.com.br (Hostinger
compartilhada). A Jessica informou que o domínio não tem e-mail ("pode seguir").

## Feito
- O `public_html` inteiro foi baixado da Hostinger por SFTP, feito a partir do contêiner `vps-api-1`, que já tem as credenciais. São
  369 arquivos, 38 MB, tudo estático e sem PHP. A cópia bruta está em `/root/site_leticia_hostinger` na VPS `179.199.128.68`.
- Os arquivos foram copiados para `/var/www/advogadaleticiabarros.com.br` (dono `www-data`).
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
- **Não verificado:** acesso pela internet com o domínio, porque o DNS ainda aponta para a Hostinger, e o HTTPS,
  porque o certificado ainda não foi emitido.

## Decisões e porquês
- A troca foi preparada sem mexer no DNS, para que o site atual não saia do ar enquanto a VPS é testada.
- A pasta foi copiada fiel, com `agents/`, `mcps/`, `squads/`, `_expxagents/` e `lp-v3/`, que já estavam
  públicas na Hostinger. Vale a Jessica decidir se essas pastas devem sair do ar.
- Foi tentado criar o usuário SFTP `siteleticia`, só SFTP, preso na pasta e com senha, para os scripts e o Orbit
  publicarem na VPS trocando apenas as variáveis `BLOG_SFTP_*`. A verificação de segurança barrou o comando,
  porque ele abre um acesso novo ao servidor. Isso fica para a Jessica autorizar.

## Pendente (Jessica decide)
1. **DNS**, na conta Hostinger dona do domínio:
   - desligar a CDN da Hostinger para o site; hoje o `www` responde por `cdn.hstgr.net`, e foi esse o provável
     motivo do problema de DNS do Orbit;
   - criar o registro A `@` para `179.199.128.68`;
   - criar o registro A `www` para `179.199.128.68`, ou um CNAME para o domínio.
2. Depois que o DNS propagar, rodar na VPS
   `certbot --nginx -d advogadaleticiabarros.com.br -d www.advogadaleticiabarros.com.br`.
3. **Publicação:** até a troca, o Orbit e os scripts continuam publicando na Hostinger. Na hora da troca, é preciso
   escolher uma de duas opções:
   - (a) autorizar o usuário SFTP `siteleticia` na VPS e trocar as variáveis `BLOG_SFTP_*` em
     `/home/orbit-src/deploy/vps/.env`, com `BLOG_SFTP_PATH=/domains/advogadaleticiabarros.com.br/public_html/blog/`;
   - (b) montar `/var/www/advogadaleticiabarros.com.br` no contêiner `api` e publicar sem SFTP, o que exige mudar o
     código.
4. Antes da troca, rodar de novo o `rsync` a partir da Hostinger, para pegar o que tiver sido publicado nesse meio
   tempo.
5. Só cancelar a hospedagem da Hostinger depois de uns dias com o site estável na VPS.

## Próxima sessão
Perguntar à Jessica se o DNS já foi trocado. Se ainda não, passar o item 1 acima.
- Se foi: refazer o download e o rsync com o mesmo procedimento deste relatório; rodar o certbot; testar com
  `curl -I https://advogadaleticiabarros.com.br`; aplicar a opção de publicação escolhida.
- Skills: `contexto-orbit`, `leticia-blog-artigo` (atualizar o host do SFTP nela).
