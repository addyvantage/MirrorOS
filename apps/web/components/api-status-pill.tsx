"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { getApiBaseUrl, getHealth } from "@/lib/api-client";

export function ApiStatusPill() {
  const [status, setStatus] = useState<"checking" | "connected" | "offline">("checking");
  const apiBaseUrl = getApiBaseUrl() || "Not configured";

  useEffect(() => {
    let isDisposed = false;
    let activeController: AbortController | null = null;

    const checkHealth = async () => {
      activeController?.abort();
      const controller = new AbortController();
      activeController = controller;

      setStatus("checking");
      const ok = await getHealth(controller.signal);
      if (!isDisposed) {
        setStatus(ok ? "connected" : "offline");
      }
    };

    checkHealth();
    const intervalId = window.setInterval(checkHealth, 10_000);

    return () => {
      isDisposed = true;
      activeController?.abort();
      window.clearInterval(intervalId);
    };
  }, []);

  const connected = status === "connected";
  const label =
    status === "checking" ? "Checking" : status === "connected" ? "API Connected" : "Offline";

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2, duration: 0.35, ease: "easeOut" }}
    >
      <Badge
        title={`API base: ${apiBaseUrl}`}
        className={
          connected
            ? "border-cyan-300/30 bg-cyan-300/10 text-cyan-200"
            : "border-white/15 bg-white/5 text-muted-foreground"
        }
      >
        <span
          className={`mr-2 inline-block size-1.5 rounded-full ${
            connected ? "bg-cyan-300 animate-pulse-glow" : "bg-zinc-500"
          }`}
        />
        {label}
        <span className="ml-2 text-[10px] uppercase opacity-80" title={`API base: ${apiBaseUrl}`}>
          API base
        </span>
      </Badge>
    </motion.div>
  );
}
