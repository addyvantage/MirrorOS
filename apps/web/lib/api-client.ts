export type HealthResponse = Record<string, unknown>;

export type IngestResponse = {
  ok: boolean;
  connector_id: string;
  ingestion_run_id: string;
  ingested_events: number;
  warnings: string[];
  errors: string[];
  notes?: string;
};

export type RecommendationReceipt = {
  event_id: string;
  title: string;
  timestamp: string;
  connector_id: string;
};

export type RecentRecommendation = {
  title: string;
  creator: string;
  url: string;
  score: number;
  receipts: RecommendationReceipt[];
};

export type RecentRecommendationsResponse = {
  recommendations: RecentRecommendation[];
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

function normalizedApiBaseUrl(): string {
  return API_BASE_URL.replace(/\/$/, "");
}

export function getApiBaseUrl(): string {
  return normalizedApiBaseUrl();
}

export async function getHealth(signal?: AbortSignal): Promise<boolean> {
  const baseUrl = normalizedApiBaseUrl();
  if (!baseUrl) return false;

  try {
    const response = await fetch(`${baseUrl}/health`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
      signal
    });

    if (!response.ok) return false;

    const contentType = response.headers.get("content-type") ?? "";
    if (contentType.includes("application/json")) {
      await response.json();
    } else {
      await response.text();
    }

    return true;
  } catch {
    return false;
  }
}

async function ingest(
  connector: "youtube" | "twitter",
  path: string,
  signal?: AbortSignal
): Promise<IngestResponse> {
  const baseUrl = normalizedApiBaseUrl();
  if (!baseUrl) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not configured");
  }

  const response = await fetch(`${baseUrl}/ingest/${connector}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    body: JSON.stringify({ path }),
    signal
  });

  if (!response.ok) {
    throw new Error(`Ingest request failed (${response.status})`);
  }

  return (await response.json()) as IngestResponse;
}

export function ingestYoutube(path: string, signal?: AbortSignal): Promise<IngestResponse> {
  return ingest("youtube", path, signal);
}

export function ingestTwitter(path: string, signal?: AbortSignal): Promise<IngestResponse> {
  return ingest("twitter", path, signal);
}

export async function getRecentRecommendations(
  signal?: AbortSignal
): Promise<RecentRecommendationsResponse> {
  const baseUrl = normalizedApiBaseUrl();
  if (!baseUrl) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not configured");
  }

  const response = await fetch(`${baseUrl}/recommend/recent`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    signal
  });

  if (!response.ok) {
    throw new Error(`Recommendation request failed (${response.status})`);
  }

  return (await response.json()) as RecentRecommendationsResponse;
}
