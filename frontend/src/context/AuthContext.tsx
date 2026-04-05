/**
 * MedOrbit — Auth Context Provider
 *
 * Manages global authentication state: user identity, JWT token,
 * login/register/logout actions, and initial token validation on load.
 *
 * MVP trade-off: JWT and user are stored in localStorage for persistence
 * across page refreshes. For production, this would move to httpOnly
 * cookies or a server-side session strategy.
 */

import { createContext, useContext, useCallback, useEffect, useState } from "react";
import type { AuthUser, UserRole } from "../types/auth";
import { authApi } from "../lib/api/auth";
import { setStoredToken } from "../lib/api/http";

/* ── Storage Keys ──────────────────────────────────────────── */

const TOKEN_KEY = "medorbit_access_token";
const USER_KEY = "medorbit_user";

/* ── Types ─────────────────────────────────────────────────── */

interface AuthState {
  user: AuthUser | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (fullName: string, email: string, password: string, role: UserRole) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

/* ── Helpers ───────────────────────────────────────────────── */

function getPersistedToken(): string | null {
  return localStorage.getItem(TOKEN_KEY) || null;
}

function getPersistedUser(): AuthUser | null {
  try {
    const raw = localStorage.getItem(USER_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    // Validate role is doctor or patient — if missing/invalid, treat as no user
    if (parsed && (parsed.role === "doctor" || parsed.role === "patient")) {
      return parsed as AuthUser;
    }
    return null;
  } catch {
    return null;
  }
}

function persistAuth(token: string, user: AuthUser) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  setStoredToken(token);
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  setStoredToken("");
}

/* ── Provider ──────────────────────────────────────────────── */

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /* ── Initial token validation on app load ─────────────── */
  useEffect(() => {
    const existingToken = getPersistedToken();

    if (!existingToken) {
      setIsLoading(false);
      return;
    }

    // Validate token by calling /auth/me
    authApi
      .getMe()
      .then((me) => {
        // Validate role
        if (me.role !== "doctor" && me.role !== "patient") {
          clearAuth();
          return;
        }
        setToken(existingToken);
        setUser(me);
        // Re-persist with fresh user data
        persistAuth(existingToken, me);
      })
      .catch(() => {
        // Token is invalid or expired — clear everything
        clearAuth();
        setToken(null);
        setUser(null);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  /* ── Login ────────────────────────────────────────────── */
  const login = useCallback(async (email: string, password: string) => {
    const response = await authApi.login({ email, password });

    // Validate role
    if (response.user.role !== "doctor" && response.user.role !== "patient") {
      throw new Error("Invalid account role");
    }

    persistAuth(response.access_token, response.user);
    setToken(response.access_token);
    setUser(response.user);
  }, []);

  /* ── Register + Auto-Login ────────────────────────────── */
  const register = useCallback(
    async (fullName: string, email: string, password: string, role: UserRole) => {
      // Step 1: Register
      await authApi.register({
        full_name: fullName,
        email,
        password,
        role,
      });

      // Step 2: Auto-login with same credentials
      await login(email, password);
    },
    [login],
  );

  /* ── Logout ───────────────────────────────────────────── */
  const logout = useCallback(() => {
    clearAuth();
    setToken(null);
    setUser(null);
    // Navigate to home
    window.history.pushState({}, "", "/");
    window.dispatchEvent(new PopStateEvent("popstate"));
  }, []);

  /* ── Listen for forced logout from 401 interceptor ──── */
  useEffect(() => {
    const handler = () => {
      clearAuth();
      setToken(null);
      setUser(null);
    };
    window.addEventListener("medorbit:force-logout", handler);
    return () => window.removeEventListener("medorbit:force-logout", handler);
  }, []);

  const value: AuthContextValue = {
    user,
    token,
    isLoading,
    isAuthenticated: !!user && !!token,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/* ── Hook ──────────────────────────────────────────────────── */

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
