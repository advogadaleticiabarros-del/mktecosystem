"""Seed tenant 0 (Advogada Letícia Barros) with verified brand data.

Colors and fonts verified against the live CSS at
advogadaleticiabarros.com.br/css/pages.css?v=20260626 on 2026-07-14 — do not
copy values from squads/design-system/_memory in blogautomaticoleticia, which
describes a stale light theme.
"""
import asyncio
import os

from app.core.security import hash_password
from app.db import SessionLocal
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User

VOZ = {
    "principios": [
        "Foco no trabalhador/segurado — o conteúdo existe para proteger e "
        "informar quem mais precisa.",
        "Dois ângulos sempre: direitos (oportunidade) + sinceridade (riscos "
        "reais).",
        "Sem juridiquês. Linguagem humanizada, direta, segunda pessoa (você).",
        "Conformidade OAB: nunca prometer resultado, nunca garantir vitória, "
        "nunca comparar com outros advogados. Usar 'pode ter direito', 'a lei "
        "prevê', 'vamos avaliar'. Sempre convidar para consulta.",
    ],
    "proibicoes": [
        "travessão dramático (—)",
        "clichês de IA: 'a verdade é que', 'no fim das contas', 'chega de X, Y, Z'",
        "superlativo vazio",
        "lista automática de três",
    ],
    "estrutura_artigo": (
        "1200-1800 palavras: gancho, H2s com keyword, Perguntas frequentes, "
        "Leia também (links internos), 1 caso típico do escritório, 2 CTAs"
    ),
    "areas": ["Trabalhista", "Previdenciário", "Família", "Consumidor", "Direito da Gestante CLT"],
    "oab": "OAB/ES 39.948",
}

IDENTIDADE_VISUAL = {
    "cores": {
        "fundo_escuro": "#231E1A",
        "fundo_alt": "#2E2720",
        "fundo_card": "#352E26",
        "dourado": "#C9A962",
        "dourado_dark": "#B8943F",
        "dourado_light": "#D4BC7D",
        "areia": "#E8DED1",
        "areia_light": "#F2EBE0",
        "branco": "#FAF6F0",
        "cafe": "#3D2B1F",
        "whatsapp": "#25D366",
    },
    "fontes": {
        "titulo_grande": "Cormorant Garamond",
        "subtitulo": "Playfair Display",
        "corpo": "Inter",
    },
    "raios": {"sm": 8, "md": 12, "lg": 20, "xl": 30},
}

CTAS = {
    "whatsapp": "5527995151402",
    "blog_url": "https://advogadaleticiabarros.com.br/blog/",
}

REGRAS_COMPLIANCE = {
    "oab": True,
    "frases_proibidas": [
        "garanto que você vai ganhar",
        "sucesso certo",
        "melhor advogada da região",
    ],
    "frases_preferidas": [
        "pode ter direito",
        "a lei prevê",
        "vamos avaliar seu caso",
    ],
}

CANAIS = {"blog": True, "instagram": "@adv.leticiabarros2"}


async def seed_leticia() -> None:
    seed_password = os.environ.get("SEED_OWNER_PASSWORD")
    if not seed_password:
        raise SystemExit("Defina a variável de ambiente SEED_OWNER_PASSWORD antes de rodar o seed.")

    async with SessionLocal() as session:
        tenant = Tenant(
            nome="Advogada Letícia Barros",
            slug="leticia-barros",
            nicho="juridico",
        )
        session.add(tenant)
        await session.flush()

        config = TenantConfig(
            tenant_id=tenant.id,
            voz=VOZ,
            identidade_visual=IDENTIDADE_VISUAL,
            ctas=CTAS,
            regras_compliance=REGRAS_COMPLIANCE,
            canais=CANAIS,
        )
        session.add(config)

        user = User(
            tenant_id=tenant.id,
            email="leticia@advogadaleticiabarros.com.br",
            nome="Advogada Letícia Barros",
            hashed_password=hash_password(seed_password),
            role="owner",
        )
        session.add(user)
        await session.commit()
        print(f"Seeded tenant {tenant.slug} ({tenant.id})")


if __name__ == "__main__":
    asyncio.run(seed_leticia())
