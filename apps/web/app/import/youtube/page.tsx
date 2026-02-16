"use client";

import { FormEvent, useState } from "react";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { IngestResponse, ingestYoutube } from "@/lib/api-client";

export default function YouTubeImportPage() {
  const [path, setPath] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<IngestResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setResult(null);
    setError(null);

    try {
      const response = await ingestYoutube(path);
      setResult(response);
    } catch (submitError) {
      const message = submitError instanceof Error ? submitError.message : "Failed to ingest";
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="container py-14 md:py-20">
      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease: "easeOut" }}
      >
        <Card className="max-w-3xl">
          <CardHeader>
            <CardTitle className="text-3xl md:text-4xl">Import YouTube Takeout</CardTitle>
            <CardDescription className="max-w-xl text-base leading-relaxed text-muted-foreground/90">
              Enter a local file path and trigger ingestion into MirrorOS.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={onSubmit} className="space-y-4">
              <label className="block text-sm font-medium text-foreground/90" htmlFor="youtube-path">
                Local path
              </label>
              <input
                id="youtube-path"
                value={path}
                onChange={(event) => setPath(event.target.value)}
                placeholder="/path/to/youtube-export"
                className="w-full rounded-xl border border-white/15 bg-black/30 px-4 py-3 text-sm text-foreground outline-none transition focus:border-cyan-300/50"
                required
              />
              <Button type="submit" disabled={isSubmitting || !path.trim()}>
                {isSubmitting ? "Ingesting..." : "Ingest"}
              </Button>
            </form>

            {result ? (
              <div className="mt-5 rounded-xl border border-cyan-300/30 bg-cyan-300/10 p-4 text-sm text-cyan-100">
                <p className="font-semibold">Ingestion started</p>
                <p>Connector: {result.connector_id}</p>
                <p>Run ID: {result.ingestion_run_id}</p>
                <p>Ingested events: {result.ingested_events}</p>
                {result.warnings.length ? (
                  <div className="mt-3">
                    <p className="font-semibold">Warnings</p>
                    <ul className="mt-1 list-disc pl-5">
                      {result.warnings.map((warning) => (
                        <li key={warning}>{warning}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
                {result.errors.length ? (
                  <div className="mt-3">
                    <p className="font-semibold">Errors</p>
                    <ul className="mt-1 list-disc pl-5">
                      {result.errors.map((errorItem) => (
                        <li key={errorItem}>{errorItem}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
              </div>
            ) : null}

            {error ? (
              <div className="mt-5 rounded-xl border border-rose-300/35 bg-rose-300/10 p-4 text-sm text-rose-100">
                <p className="font-semibold">Ingestion failed</p>
                <p>{error}</p>
              </div>
            ) : null}
          </CardContent>
        </Card>
      </motion.div>
    </section>
  );
}
