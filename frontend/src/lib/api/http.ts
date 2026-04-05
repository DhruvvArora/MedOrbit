/**
 * MedOrbit — HTTP Client
 *
 * Central fetch wrapper that attaches JWT auth headers and handles
 * common error scenarios including token expiry.
 *
 * MVP trade-off: Token stored in localStorage for simplicity.
 * Production would use httpOnly cookies or a more secure strategy.
 */

const API_BASE = (import.meta as ImportMeta & { env: Record<string, string> }).env
  .VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

export function getStoredToken() {
  return localStorage.getItem("medorbit_access_token") || "";
}

export function setStoredToken(token: string) {
  localStorage.setItem("medorbit_access_token", token);
}

/**
 * Paths that should NOT trigger a forced logout on 401.
 * These are auth-related endpoints where a 401 is an expected
 * "wrong credentials" response, not an expired token.
 */
const AUTH_PATHS = ["/auth/login", "/auth/register", "/auth/me"];

function isAuthPath(path: string): boolean {
  return AUTH_PATHS.some((p) => path.startsWith(p));
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers || {});
  headers.set("Content-Type", "application/json");

  const token = getStoredToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    // Handle 401 on non-auth paths — token is expired/invalid
    // Dispatch a custom event so AuthContext can clear state centrally.
    // This avoids importing React state into a plain utility module
    // and prevents redirect loops on /auth/* endpoints.
    if (response.status === 401 && !isAuthPath(path)) {
      window.dispatchEvent(new CustomEvent("medorbit:force-logout"));
      // Navigate to login — but only if not already there
      if (window.location.pathname !== "/login") {
        window.history.pushState({}, "", "/login");
        window.dispatchEvent(new PopStateEvent("popstate"));
      }
    }

    let message = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      message = body.detail || body.message || message;
    } catch {
      // keep fallback message
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
