/**
 * MedOrbit — Auth API Client
 *
 * Wraps the three auth endpoints: register, login, and getMe.
 * Uses the shared apiFetch which automatically attaches the stored JWT.
 */

import { apiFetch } from "./http";
import type { AuthUser, LoginRequest, RegisterRequest, TokenResponse } from "../../types/auth";

export const authApi = {
  /**
   * Register a new doctor or patient account.
   * Returns the created user (without token — call login after).
   */
  register: (data: RegisterRequest) =>
    apiFetch<AuthUser>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  /**
   * Authenticate with email + password.
   * Returns JWT access token and user profile.
   */
  login: (data: LoginRequest) =>
    apiFetch<TokenResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  /**
   * Get the currently authenticated user's profile.
   * Requires a valid Bearer token in localStorage.
   */
  getMe: () => apiFetch<AuthUser>("/auth/me"),
};