"use client";

// Auditoria do perfil @adv.leticiabarros2 (09/10/2026), feita com a skill instagram-marketing
// (ig-profile-optimizer) sobre os dados da Graph API e filtrada pelas regras da OAB.
// Fonte: docs/AUDITORIA_PERFIL_INSTAGRAM.md.

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Check, ChevronLeft, Copy } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type Situacao = "ok" | "melhorar" | "refazer" | "conferir";

const PLACAR: { parte: string; situacao: Situacao; motivo: string }[] = [
  { parte: "Foto de perfil", situacao: "conferir", motivo: "Rosto grande, fundo limpo e contraste alto; a foto aparece pequena." },
  { parte: "Campo NOME (o que a busca do Instagram encontra)", situacao: "refazer", motivo: "Hoje: “Advogada | Direito Trabalhista, Direito das Gravidas e Famílias”. Não tem o seu nome, é longo e “Gravidas” está sem acento." },
  { parte: "@ do perfil", situacao: "ok", motivo: "adv.leticiabarros2 funciona; não vale trocar agora." },
  { parte: "Bio", situacao: "refazer", motivo: "“📲 Fale comigo” é oferta direta (vetada pela OAB) e a bio não diz o que você publica nem para quem." },
  { parte: "Link", situacao: "melhorar", motivo: "Leva à página inicial; para crescer, leve ao conteúdo (blog ou série)." },
  { parte: "Categoria", situacao: "conferir", motivo: "Usar “Advogado(a)”." },
  { parte: "Destaques", situacao: "conferir", motivo: "4 a 6, na ordem da próxima pergunta de quem chega (proposta abaixo)." },
  { parte: "Grade (9 primeiros posts)", situacao: "ok", motivo: "Identidade café e dourado consistente desde outubro." },
  { parte: "Posts fixados (até 3)", situacao: "refazer", motivo: "Usar as melhores provas (proposta abaixo)." },
];

const COR: Record<Situacao, string> = {
  ok: "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300",
  melhorar: "bg-amber-500/15 text-amber-700 dark:text-amber-300",
  refazer: "bg-red-500/15 text-red-700 dark:text-red-300",
  conferir: "bg-sky-500/15 text-sky-700 dark:text-sky-300",
};
const ROTULO: Record<Situacao, string> = { ok: "Ok", melhorar: "Melhorar", refazer: "Refazer", conferir: "Conferir no app" };

const NOME = "Letícia Barros | Advogada Trabalhista";
const BIO_A = "A advogada da gestante trabalhadora.\nDireito do Trabalho e de Família sem juridiquês.\nVitória/ES · OAB/ES 39.948\n👇 Artigos no blog";
const BIO_B = "Seus direitos no trabalho, na gravidez e na família, explicados sem juridiquês.\nVitória/ES · OAB/ES 39.948\n👇 Artigos no blog";

function Copiavel({ titulo, texto }: { titulo: string; texto: string }) {
  const [copiado, setCopiado] = useState(false);
  return (
    <div className="rounded-lg border border-border bg-background p-4">
      <div className="mb-2 flex items-center justify-between gap-2">
        <p className="text-xs font-semibold uppercase tracking-wide text-primary">{titulo}</p>
        <Button
          size="sm"
          variant="outline"
          onClick={async () => {
            await navigator.clipboard.writeText(texto);
            setCopiado(true);
            setTimeout(() => setCopiado(false), 1800);
          }}
        >
          {copiado ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
          {copiado ? "Copiado" : "Copiar"}
        </Button>
      </div>
      <p className="whitespace-pre-line text-sm">{texto}</p>
      <p className="mt-2 text-xs text-muted-foreground">{texto.length} caracteres</p>
    </div>
  );
}

export default function AuditoriaPerfilPage() {
  const router = useRouter();
  return (
    <AppShell
      title="Auditoria do perfil"
      description="@adv.leticiabarros2 · 09/10/2026 · 415 seguidores, 443 seguindo, 298 posts"
      headerActions={
        <Button variant="outline" size="sm" onClick={() => router.push("/crescimento")}>
          <ChevronLeft className="h-4 w-4" /> Voltar ao crescimento
        </Button>
      }
    >
      <div className="mx-auto max-w-4xl space-y-6">
        <Card className="p-5">
          <h2 className="font-display text-base font-semibold">Placar das 9 partes do perfil</h2>
          <p className="text-sm text-muted-foreground">É no topo do perfil que a visita decide seguir. Meta: média de 30 seguidores por mês.</p>
          <div className="mt-2 divide-y divide-border">
            {PLACAR.map((l) => (
              <div key={l.parte} className="flex flex-col gap-1 py-3 sm:flex-row sm:items-start sm:gap-4">
                <span className={cn("w-fit shrink-0 rounded-full px-2.5 py-0.5 text-xs font-semibold", COR[l.situacao])}>{ROTULO[l.situacao]}</span>
                <div>
                  <p className="text-sm font-medium">{l.parte}</p>
                  <p className="text-sm text-muted-foreground">{l.motivo}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-5">
          <h2 className="font-display text-base font-semibold">O que trocar no Instagram (pronto para copiar)</h2>
          <div className="grid gap-4">
            <Copiavel titulo="Campo NOME (recomendado)" texto={NOME} />
            <Copiavel titulo="Bio · opção A (posicionamento gestante)" texto={BIO_A} />
            <Copiavel titulo="Bio · opção B (mais ampla)" texto={BIO_B} />
          </div>
          <p className="text-sm text-muted-foreground">
            Link: o blog (advogadaleticiabarros.com.br/blog) ou uma página com o blog e a série da gestante. Evitar página com oferta de consulta.
          </p>
        </Card>

        <Card className="p-5">
          <h2 className="font-display text-base font-semibold">Destaques</h2>
          <div className="flex flex-wrap gap-2">
            {["Comece aqui", "Gestante", "Trabalho", "Família", "Na TV", "Dúvidas"].map((d) => (
              <span key={d} className="rounded-full border border-primary/40 bg-primary/5 px-3 py-1 text-sm">{d}</span>
            ))}
          </div>
          <p className="text-sm text-muted-foreground">Capas no padrão café e dourado, nomes curtos, nessa ordem.</p>
        </Card>

        <Card className="p-5">
          <h2 className="font-display text-base font-semibold">Posts fixados</h2>
          <ol className="list-decimal space-y-2 pl-5 text-sm">
            <li><b>Vídeo da TV Tribuna</b> sobre a licença-maternidade adotiva (25/09): o melhor desempenho recente (45 curtidas, 9 comentários) e prova de autoridade.</li>
            <li><b>Reel 1/3 da série da gestante</b>, quando for publicado: diz para quem é o perfil.</li>
            <li><b>Carrossel da pensão de R$ 300</b> (10/10), ou o post de família que mais for salvo.</li>
          </ol>
          <p className="text-sm text-muted-foreground">Extra: seguir mais contas do que tem seguidores (443 × 415) passa um sinal fraco; reduzir aos poucos, sem pressa.</p>
        </Card>

        <Card className="p-5">
          <h2 className="font-display text-base font-semibold">Teste do cabeçalho</h2>
          <p className="text-sm text-muted-foreground">
            Lendo só a foto, o nome, a bio, o link e a primeira linha da grade, uma gestante de Vitória entende em 3 segundos que ali estão os
            direitos dela, explicados por uma advogada real (nome + OAB)? Com as mudanças acima, sim.
          </p>
          <p className="text-sm text-muted-foreground">
            Já aplicado no Orbit: toda legenda gerada segue as regras da skill (gancho nos 125 caracteres antes do “mais”, um único convite de
            salvar ou enviar, 3 a 5 hashtags de nicho + área + local, nada inventado e sem marcas de texto de IA).
          </p>
        </Card>
      </div>
    </AppShell>
  );
}
