/**
 * MedOrbit — Login Page
 *
 * Email + password login form. On success, stores JWT and
 * redirects to the user's role-specific dashboard.
 */

import { useState, type FormEvent } from "react";
import { useAuth } from "../../context/AuthContext";
import "../../styles/auth.css";

function navigateTo(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function LoginPage() {
  const { login, isAuthenticated, user } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // If already authenticated, redirect
  if (isAuthenticated && user) {
    const target = user.role === "doctor" ? "/doctor/dashboard" : "/patient/dashboard";
    navigateTo(target);
    return null;
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(email, password);
      // AuthContext now has the user — read role from it
      // We need to get the user from the login response
      // The login function sets the user in context, but we can't
      // read it synchronously here. Instead, we'll use the stored user.
      const stored = localStorage.getItem("medorbit_user");
      if (stored) {
        const parsed = JSON.parse(stored);
        const target = parsed.role === "doctor" ? "/doctor/dashboard" : "/patient/dashboard";
        navigateTo(target);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        {/* Brand */}
        <div className="auth-brand" onClick={() => navigateTo("/")}>
          MedOrbit
        </div>

        <h1 className="auth-title">Welcome back</h1>
        <p className="auth-subtitle">Sign in to access your dashboard</p>

        {/* Error Alert */}
        {error && (
          <div className="auth-error" role="alert">
            <span className="auth-error-icon">⚠</span>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          {/* Email */}
          <div className="auth-field">
            <label htmlFor="login-email">Email address</label>
            <input
              id="login-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              autoComplete="email"
              autoFocus
            />
          </div>

          {/* Password */}
          <div className="auth-field">
            <label htmlFor="login-password">Password</label>
            <div className="auth-password-wrap">
              <input
                id="login-password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                autoComplete="current-password"
              />
              <button
                type="button"
                className="auth-password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex={-1}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          {/* Submit */}
          <button type="submit" className="auth-submit" disabled={loading}>
            {loading ? (
              <span className="auth-spinner" />
            ) : (
              "Sign In"
            )}
          </button>
        </form>

        {/* Register Link */}
        <p className="auth-switch">
          Don't have an account?{" "}
          <a href="/register" onClick={(e) => { e.preventDefault(); navigateTo("/register"); }}>
            Create one
          </a>
        </p>

        {/* Demo Hint */}
        <div className="auth-demo-hint">
          <details>
            <summary>Demo accounts</summary>
            <div className="auth-demo-accounts">
              <div>
                <strong>Doctor:</strong> doctor@medorbit.demo / doctor123
              </div>
              <div>
                <strong>Patient:</strong> patient@medorbit.demo / patient123
              </div>
            </div>
          </details>
        </div>
      </div>
    </div>
  );
}
