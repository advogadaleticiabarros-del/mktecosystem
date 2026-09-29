import type { Metadata, Viewport } from "next";
import "./editorial.css";

export const metadata: Metadata = {
  title: "Orbit Editorial",
  manifest: "/editorial-manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "Editorial",
  },
  icons: {
    apple: "/editorial-icon.png",
  },
};

export const viewport: Viewport = {
  themeColor: "#231e1a",
  viewportFit: "cover",
};

export default function EditorialLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="editorial-root" data-theme="dourado">
      {children}
    </div>
  );
}
