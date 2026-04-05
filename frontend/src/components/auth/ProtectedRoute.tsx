import { useAuth } from "../../context/AuthContext";
import { LoadingState } from "../shared/LoadingState";
import type { UserRole } from "../../types/auth";
import { useEffect } from "react";

interface Props {
  requiredRole?: UserRole;
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

    if (requiredRole && user.role !== requiredRole) {
      const correctPath =
        user.role === "doctor" ? "/doctor/dashboard" : "/patient/dashboard";
      navigateTo(correctPath);
    }
  }, [isLoading, isAuthenticated, user, requiredRole]);

  if (isLoading) {
    return <LoadingState label="Verifying authentication..." />;
  }

  if (!isAuthenticated || !user) {
    return null;
  }

  if (requiredRole && user.role !== requiredRole) {
    return null;
  }

  return <>{children}</>;
}