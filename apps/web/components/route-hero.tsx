"use client";

import { motion } from "framer-motion";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

type RouteHeroProps = {
  title: string;
  description: string;
};

export function RouteHero({ title, description }: RouteHeroProps) {
  return (
    <section className="container py-14 md:py-20">
      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease: "easeOut" }}
      >
        <Card className="max-w-3xl">
          <CardHeader>
            <CardTitle className="text-3xl md:text-4xl">{title}</CardTitle>
            <CardDescription className="max-w-xl text-base leading-relaxed text-muted-foreground/90">
              {description}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Placeholder workflow screen for this route.
            </p>
          </CardContent>
        </Card>
      </motion.div>
    </section>
  );
}
