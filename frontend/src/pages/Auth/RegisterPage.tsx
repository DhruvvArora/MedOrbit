/**
 * MedOrbit — Register Page
 *
 * Full-name, email, password (with confirm), and role selection.
 * Auto-logs in after successful registration and redirects by role.
 */

import { useState, useEffect, type FormEvent } from "react";
import { useAuth } from "../../context/AuthContext";
import type { UserRole } from "../../types/auth";
import "../../styles/auth.css";

function navigateTo(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function RegisterPage() {
  const { register, isAuthenticated, user } = useAuth();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState<UserRole>("patient");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // If already authenticated, redirect via effect to avoid mid-render state collisions
  useEffect(() => {
    if (isAuthenticated && user) {
      const target = user.role === "doctor" ? "/doctor/dashboard" : "/patient/dashboard";
      navigateTo(target);
    }
  }, [isAuthenticated, user]);

  if (isAuthenticated && user) {
    return null; // prevent flash of form while redirecting
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    // Client-side validation
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await register(fullName, email, password, role);
      // Wait for React to naturally re-render with isAuthenticated=true
      // Instead of forcing navigation immediately here.
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed. Please try again.");
    } finally {
      if (!isAuthenticated) setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card auth-card--register">
        {/* Brand */}
        <div className="auth-brand" onClick={() => navigateTo("/")}>
          MedOrbit
        </div>

        <h1 className="auth-title">Create your account</h1>
        <p className="auth-subtitle">Join MedOrbit as a doctor or patient</p>

        {/* Error Alert */}
        {error && (
          <div className="auth-error" role="alert">
            <span className="auth-error-icon">⚠</span>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          {/* Role Toggle */}
          <div className="auth-role-toggle">
            <button
              type="button"
              className={`auth-role-btn ${role === "doctor" ? "auth-role-btn--active" : ""}`}
              onClick={() => setRole("doctor")}
            >
              <span className="auth-role-icon">🩺</span>
              I'm a Doctor
            </button>
            <button
              type="button"
              className={`auth-role-btn ${role === "patient" ? "auth-role-btn--active" : ""}`}
              onClick={() => setRole("patient")}
            >
              <span className="auth-role-icon">👤</span>
              I'm a Patient
            </button>
          </div>

          {/* Full Name */}
          <div className="auth-field">
            <label htmlFor="register-name">Full name</label>
            <input
              id="register-name"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder={role === "doctor" ? "Dr. Sarah Chen" : "Alex Johnson"}
              required
              maxLength={100}
              autoComplete="name"
              autoFocus
            />
          </div>

          {/* Email */}
          <div className="auth-field">
            <label htmlFor="register-email">Email address</label>
            <input
              id="register-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              autoComplete="email"
            />
          </div>

          {/* Password */}
          <div className="auth-field">
            <label htmlFor="register-password">Password</label>
            <div className="auth-password-wrap">
              <input
                id="register-password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 8 characters"
                required
                minLength={8}
                maxLength={128}
                autoComplete="new-password"
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
            <span className="auth-hint">Minimum 8 characters</span>
          </div>

          {/* Confirm Password */}
          <div className="auth-field">
            <label htmlFor="register-confirm">Confirm password</label>
            <input
              id="register-confirm"
              type={showPassword ? "text" : "password"}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Re-enter your password"
              required
              autoComplete="new-password"
            />
          </div>

          {/* Submit */}
          <button type="submit" className="auth-submit" disabled={loading}>
            {loading ? (
              <span className="auth-spinner" />
            ) : (
              "Create Account"
            )}
          </button>
        </form>

        {/* Login Link */}
        <p className="auth-switch">
          Already have an account?{" "}
          <a href="/login" onClick={(e) => { e.preventDefault(); navigateTo("/login"); }}>
            Sign in
          </a>
        </p>
      </div>
    </div>
  );
}
