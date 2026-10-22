# 22/10/2026 — LinkedIn no Orbit, manual do aplicativo e capa nova

## Manual (privado, conta atual do Claude)
"Conexão do LinkedIn": https://claude.ai/artifact/BHjcEyPjap1ezi8KX9ztsE. Tem 4 partes:
1. página da empresa;
2. aplicativo em linkedin.com/developers (Share on LinkedIn + Sign In with OpenID Connect, verificação com a
   página, redirect `https://api.orbit.advogadaleticiabarros.com.br/integracoes/linkedin/callback`);
3. chaves em Configurações (Client ID + Client Secret separados por espaço);
4. conectar na Visão Geral.

Guia do perfil ajustado ao perfil existente: https://claude.ai/artifact/Qp1tMEFgfBJ1Z58NQX3v9u.

## Integração (commit ff52284, no ar; migração e3f5a7b9c1d2 aplicada com backup do banco antes)
- `integrations/social/linkedin_api.py`:
  - OAuth (`openid profile w_member_social`), `/v2/userinfo` e `/rest/posts` com card do artigo;
  - capa pela API `/rest/images` (initializeUpload + PUT);
  - escape "little text" (os reservados cortariam o post) e hashtags como `{hashtag|\#|tag}`;
  - `LinkedIn-Version` começa 2 meses atrás e recua um mês quando a versão não existe (426 / NONEXISTENT_VERSION).
- `services/linkedin.py`:
  - `abrir` (conexão vencida = aviso);
  - `dados_do_artigo` (título, descrição e capa lidos do site por SFTP);
  - `publicar_post` / `publicar_prontos` (espera o artigo ir ao ar; conexão vencida mantém o post agendado);
  - `aviso_conexao` (melhoria a partir de 7 dias do vencimento; o token dura 60 dias, sem refresh);
  - `sugerir_post` (voz da Dra. para o LinkedIn, com nova tentativa se ferir a OAB).
- Rotas:
  - `/integracoes/linkedin/iniciar|callback`, `DELETE /integracoes/linkedin`;
  - `/linkedin` (situação), `/linkedin/posts` (CRUD, publicar-agora, sugerir);
  - job a cada 5 min no `job_envios`;
  - chave "LinkedIn" em `chaves_api` (validada: só `invalid_client` recusa).
- Tela: card "LinkedIn" na Visão Geral (Conectar / Reconectar / Desconectar / Abrir fila), página `/linkedin`
  (novo post com IA e checagem da OAB, link do artigo, agenda, fila) e item no menu.
- Testes: `test_linkedin_api.py` (6) e `test_linkedin_rotas.py` (4). Suíte com 323 passando.
- **Falta (Jessica e Dra.):** criar a página da empresa e o aplicativo, colar as chaves e conectar. Nenhum post foi
  publicado no LinkedIn ainda.

## Perfil do LinkedIn (prints da Jessica)
- A Dra. já tem perfil: linkedin.com/in/leticia-barros-996699158.
- Experiência cadastrada: "Advogada · Letícia Barros Advocacia e Consultoria Jurídica · 2021 – o momento". **Pedi
  para conferir a data de início:** antes da inscrição na OAB (aprovada no 37º Exame), não pode constar "Advogada".
  Sugeri também ligar a experiência à página da empresa e usar "Híbrido".
- No campo "LinkedIn Page" do aplicativo, apareceu uma página "Letícia Barros" que pode não ser dela. Orientei a não
  escolher antes de conferir em "Eu" › "Gerenciar".

## Capa nova (caderno de marca: `Downloads/Caderno_de_Marca_-_Letícia_Barros.pdf`)
- `producao/linkedin/capa-linkedin-leticia-barros.png` (1584×396) e `@2x`. Fonte HTML: `capa-linkedin.html`.
  Cópia em `C:\Users\prosy\Downloads\capa-linkedin-leticia-barros.png`.
- Fundo marrom terra (#4d2a1f), selo oficial LB com balança (`logo/logo-sem-fundo.png`), Playfair Display +
  Raleway, assinatura principal do caderno e "OAB/ES 39.948 · Vitória/ES · site". O lado esquerdo fica livre para a
  foto de perfil.
- A capa atual (LB preto com colunas laranja) está fora do caderno.
- **Ponto de atenção:** o caderno posiciona a marca como "exclusivamente gestantes CLT", enquanto o guia do
  LinkedIn mira também empresas e RH (pilar "Empresa em dia" do plano até 31/12). A capa usa "Gestantes CLT", como
  no caderno.
