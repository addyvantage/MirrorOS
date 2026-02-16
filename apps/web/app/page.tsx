"use client";

import Link from "next/link";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const howItWorks = [
  {
    title: "Ingest",
    body: "Import your exports from YouTube and Twitter with a clean, guided flow."
  },
  {
    title: "Graph",
    body: "MirrorOS builds your personal context graph to map intent, taste, and voice."
  },
  {
    title: "Receipts",
    body: "Trace every recommendation and generated reply back to source evidence."
  }
];

export default function LandingPage() {
  return (
    <div className="container pb-20 pt-16 md:pt-24">
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.55, ease: "easeOut" }}
        className="mx-auto max-w-4xl"
      >
        <p className="mb-3 text-xs font-medium tracking-[0.28em] text-cyan-200/80 uppercase">MirrorOS</p>
        <h1 className="text-balance text-4xl font-semibold leading-tight md:text-6xl">
          Your personal context layer: taste + voice + receipts.
        </h1>
        <p className="mt-5 max-w-2xl text-base text-muted-foreground md:text-lg">
          Bring your data in once, then reuse your context everywhere. Private by design and auditable by
          default.
        </p>

        <div className="mt-9 flex flex-wrap gap-3">
          <Button asChild size="lg">
            <Link href="/import/youtube">Import YouTube Takeout</Link>
          </Button>
          <Button asChild size="lg" variant="secondary">
            <Link href="/import/twitter">Import Twitter Export</Link>
          </Button>
        </div>
      </motion.section>

      <section className="mt-14 grid gap-5 md:mt-20 md:grid-cols-3">
        {howItWorks.map((item, idx) => (
          <motion.div
            key={item.title}
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.45 }}
            transition={{ duration: 0.35, ease: "easeOut", delay: idx * 0.08 }}
          >
            <Card className="h-full transition-all duration-300 hover:-translate-y-0.5 hover:border-cyan-200/25">
              <CardHeader>
                <CardTitle>{item.title}</CardTitle>
                <CardDescription>{item.body}</CardDescription>
              </CardHeader>
            </Card>
          </motion.div>
        ))}
      </section>

      <motion.section
        initial={{ opacity: 0, y: 18 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.4 }}
        transition={{ duration: 0.45, ease: "easeOut" }}
        className="mt-8 md:mt-10"
      >
        <Card className="border-cyan-200/20 bg-gradient-to-br from-cyan-400/10 via-white/[0.03] to-violet-400/10">
          <CardContent className="py-8">
            <h2 className="text-xl font-semibold md:text-2xl">Privacy-first foundation</h2>
            <p className="mt-2 text-muted-foreground">Local-first, read-only by default</p>
          </CardContent>
        </Card>
      </motion.section>

      <footer className="mt-14 border-t border-white/10 pt-6 text-sm text-muted-foreground">
        GitHub placeholder
      </footer>
    </div>
  );
}
