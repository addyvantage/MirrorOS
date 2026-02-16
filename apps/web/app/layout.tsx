import type { Metadata } from "next";
import { Manrope } from "next/font/google";

import { TopNav } from "@/components/top-nav";
import "./globals.css";

const manrope = Manrope({
  subsets: ["latin"],
  variable: "--font-manrope"
});

export const metadata: Metadata = {
  title: "MirrorOS",
  description: "Personal context platform"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${manrope.variable} font-sans`}>
        <div className="relative isolate min-h-screen overflow-hidden">
          <div className="pointer-events-none absolute inset-x-0 top-[-25rem] mx-auto h-[38rem] w-[38rem] rounded-full bg-gradient-to-br from-cyan-400/18 via-cyan-300/5 to-violet-500/18 blur-3xl" />
          <TopNav />
          <main className="relative z-10">{children}</main>
        </div>
      </body>
    </html>
  );
}
