import "./globals.css";
import { Chakra_Petch, Inter, JetBrains_Mono } from "next/font/google";
import { cn } from "@/lib/utils";
import { ThemeProvider } from "@/components/theme-provider";

const chakraPetch = Chakra_Petch({
  subsets: ["latin"],
  variable: "--font-display",
  weight: ["500", "600", "700"],
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  weight: ["400", "500", "600"],
});

export const metadata = {
  title: "Orbit — The Marketing Operating System",
};

const THEME_SCRIPT = `
(function () {
  try {
    var temasValidos = ["dourado", "esmeralda", "azul", "violeta"];
    var tema = localStorage.getItem("orbit-theme");
    if (temasValidos.indexOf(tema) === -1) tema = "dourado";
    document.documentElement.setAttribute("data-theme", tema);
  } catch (e) {}
})();
`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="pt-BR"
      data-theme="dourado"
      suppressHydrationWarning
      className={cn("font-sans", chakraPetch.variable, inter.variable, jetbrainsMono.variable)}
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: THEME_SCRIPT }} />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
