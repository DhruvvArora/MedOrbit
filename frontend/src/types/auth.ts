/**
 * MedOrbit — Auth Type Definitions
 *
 * Shared types for authentication state, API payloads, and user identity.
 */

export type UserRole = "doctor" | "patient";

export interface AuthUser {
  id: string;
  full_name: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}
