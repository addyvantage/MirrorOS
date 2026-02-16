import Link from "next/link";

import { ApiStatusPill } from "@/components/api-status-pill";

export function TopNav() {
  return (
    <header className="sticky top-0 z-20 border-b border-white/10 bg-black/20 backdrop-blur-xl">
      <div className="container flex h-16 items-center justify-between">
        <Link
          href="/"
          className="text-sm font-semibold tracking-[0.18em] text-foreground/90 uppercase"
        >
          MirrorOS
        </Link>

        <div className="flex items-center gap-6">
          <nav className="hidden items-center gap-5 text-sm text-muted-foreground sm:flex">
            <Link href="#" className="transition-colors hover:text-foreground">
              Docs
            </Link>
            <Link href="#" className="transition-colors hover:text-foreground">
              Roadmap
            </Link>
            <Link href="#" className="transition-colors hover:text-foreground">
              GitHub
            </Link>
          </nav>
          <ApiStatusPill />
        </div>
      </div>
    </header>
  );
}
