const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type ApiMethod = "GET" | "POST" | "PUT" | "PATCH";

export async function apiRequest<T>(path: string, method: ApiMethod = "GET", body?: unknown, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail ?? "Error inesperado de backend");
  }

  return response.json() as Promise<T>;
}
