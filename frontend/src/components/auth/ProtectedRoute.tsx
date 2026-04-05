/**
 * MedOrbit — Protected Route Component
 *
 * Wraps route sections that require authentication and/or a specific role.
 * Handles three cases:
 *   1. Still loading auth state → show loading spinner
 *   2. Not authenticated → redirect to /login
 *   3. Wrong role → redirect to correct dashboard
 */

import { useAuth } from "../../context/AuthContext";
import { LoadingState } from "../shared/LoadingState";
import type { UserRole } from "../../types/auth";
import { useEffect } from "react";

interface Props {
  requiredRole: UserRole;
  children: React.ReactNode;
}

function navigateTo(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function ProtectedRoute({ requiredRole, children }: Props) {
  const { isAuthenticated, isLoading, user } = useAuth();

  useEffect(() => {
    if (isLoading) return;

    if (!isAuthenticated || !user) {
      navigateTo("/login");
      return;
    }

    if (user.role !== requiredRole) {
      // Wrong role → redirect to their correct dashboard
      const correctPath =
        user.role === "doctor" ? "/doctor/dashboard" : "/patient/dashboard";
      navigateTo(correctPath);
    }
  }, [isLoading, isAuthenticated, user, requiredRole]);

  // While loading auth state, show spinner
  if (isLoading) {
    return <LoadingState label="Verifying authentication..." />;
  }

  // Not authenticated or wrong role — render nothing while redirect fires
  if (!isAuthenticated || !user || user.role !== requiredRole) {
    return null;
  }

  return <>{children}</>;
}
