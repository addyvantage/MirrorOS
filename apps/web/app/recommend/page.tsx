"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { RecentRecommendation, getRecentRecommendations } from "@/lib/api-client";

type ExpandedReceipts = Record<string, boolean>;

function recommendationKey(recommendation: RecentRecommendation): string {
  return `${recommendation.creator}:${recommendation.url}`;
}

export default function RecommendPage() {
  const [recommendations, setRecommendations] = useState<RecentRecommendation[]>([]);
  const [expandedReceipts, setExpandedReceipts] = useState<ExpandedReceipts>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    const loadRecommendations = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await getRecentRecommendations(controller.signal);
        setRecommendations(response.recommendations);
      } catch (loadError) {
        if (controller.signal.aborted) return;
        const message =
          loadError instanceof Error ? loadError.message : "Failed to load recommendations";
        setError(message);
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    };

    void loadRecommendations();
    return () => controller.abort();
  }, []);

  const toggleReceipts = (key: string) => {
    setExpandedReceipts((current) => ({ ...current, [key]: !current[key] }));
  };

  return (
    <section className="container py-14 md:py-20">
      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease: "easeOut" }}
        className="space-y-6"
      >
        <Card>
          <CardHeader>
            <CardTitle className="text-3xl md:text-4xl">Recommendations</CardTitle>
            <CardDescription className="max-w-2xl text-base leading-relaxed text-muted-foreground/90">
              Recent creator recommendations grounded in your context graph with receipts for
              traceability.
            </CardDescription>
          </CardHeader>
        </Card>

        {isLoading ? (
          <Card>
            <CardContent className="pt-6 text-sm text-muted-foreground">
              Loading recommendations...
            </CardContent>
          </Card>
        ) : null}

        {error ? (
          <Card>
            <CardContent className="pt-6 text-sm text-rose-200">
              Failed to load recommendations: {error}
            </CardContent>
          </Card>
        ) : null}

        {!isLoading && !error && recommendations.length === 0 ? (
          <Card>
            <CardContent className="pt-6 text-sm text-muted-foreground">
              No recent recommendations found.
            </CardContent>
          </Card>
        ) : null}

        {!isLoading && !error
          ? recommendations.map((recommendation) => {
              const key = recommendationKey(recommendation);
              const isExpanded = expandedReceipts[key] ?? false;

              return (
                <Card key={key}>
                  <CardHeader>
                    <CardTitle className="text-2xl">{recommendation.title}</CardTitle>
                    <CardDescription className="text-sm text-muted-foreground/90">
                      Creator: {recommendation.creator}
                    </CardDescription>
                    <CardDescription className="text-sm text-muted-foreground/90">
                      Score: {recommendation.score.toFixed(2)}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-cyan-100">
                      {recommendation.url ? recommendation.url : "No canonical URL available"}
                    </p>
                    <Button variant="secondary" size="sm" onClick={() => toggleReceipts(key)}>
                      {isExpanded ? "Hide Receipts" : "Show Receipts"}
                    </Button>
                    {isExpanded ? (
                      <ul className="space-y-3 text-sm text-muted-foreground">
                        {recommendation.receipts.map((receipt) => (
                          <li key={receipt.event_id} className="rounded-xl border border-white/10 p-3">
                            <p className="text-foreground">{receipt.title}</p>
                            <p>timestamp: {receipt.timestamp}</p>
                            <p>connector_id: {receipt.connector_id}</p>
                          </li>
                        ))}
                      </ul>
                    ) : null}
                  </CardContent>
                </Card>
              );
            })
          : null}
      </motion.div>
    </section>
  );
}
