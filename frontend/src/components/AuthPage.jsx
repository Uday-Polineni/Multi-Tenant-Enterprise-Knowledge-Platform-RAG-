import { useState } from "react";
import { login, register } from "../api/auth.js";

export default function AuthPage({ onAuthenticated, loading, setLoading, error, setError }) {
  const [authTab, setAuthTab] = useState("signin");
  const [registerMode, setRegisterMode] = useState("org");
  const [registerForm, setRegisterForm] = useState({
    email: "",
    password: "",
    organizationName: "",
    inviteToken: "",
  });
  const [loginForm, setLoginForm] = useState({
    email: "",
    password: "",
  });

  async function handleRegister(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await register({
        email: registerForm.email,
        password: registerForm.password,
        organizationName: registerMode === "org" ? registerForm.organizationName : undefined,
        inviteToken: registerMode === "invite" ? registerForm.inviteToken : undefined,
      });
      onAuthenticated(data.access_token, registerForm.email);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleLogin(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await login(loginForm);
      onAuthenticated(data.access_token, loginForm.email);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-hero">
        <h1>Enterprise Knowledge Assistant</h1>
        <p>Sign in to search your organization&apos;s documents with AI.</p>
      </div>

      <div className="auth-card card">
        <div className="auth-tabs" role="tablist">
          <button
            type="button"
            role="tab"
            className={authTab === "signin" ? "auth-tab active" : "auth-tab"}
            aria-selected={authTab === "signin"}
            onClick={() => {
              setAuthTab("signin");
              setError("");
            }}
          >
            Sign in
          </button>
          <button
            type="button"
            role="tab"
            className={authTab === "signup" ? "auth-tab active" : "auth-tab"}
            aria-selected={authTab === "signup"}
            onClick={() => {
              setAuthTab("signup");
              setError("");
            }}
          >
            Sign up
          </button>
        </div>

        {error && <div className="alert error auth-alert">{error}</div>}

        {authTab === "signin" ? (
          <form onSubmit={handleLogin} className="auth-form">
            <label>
              Email
              <input
                type="email"
                required
                autoComplete="email"
                value={loginForm.email}
                onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
              />
            </label>
            <label>
              Password
              <input
                type="password"
                required
                autoComplete="current-password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
              />
            </label>
            <button type="submit" disabled={loading} className="auth-submit">
              {loading ? "Signing in…" : "Sign in"}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegister} className="auth-form">
            <div className="register-modes">
              <label className="radio-inline">
                <input
                  type="radio"
                  name="registerMode"
                  checked={registerMode === "org"}
                  onChange={() => setRegisterMode("org")}
                />
                New organization
              </label>
              <label className="radio-inline">
                <input
                  type="radio"
                  name="registerMode"
                  checked={registerMode === "invite"}
                  onChange={() => setRegisterMode("invite")}
                />
                Invite code
              </label>
            </div>
            {registerMode === "org" ? (
              <label>
                Organization name
                <input
                  required
                  value={registerForm.organizationName}
                  onChange={(e) =>
                    setRegisterForm({ ...registerForm, organizationName: e.target.value })
                  }
                />
              </label>
            ) : (
              <label>
                Invite code
                <input
                  required
                  value={registerForm.inviteToken}
                  onChange={(e) =>
                    setRegisterForm({ ...registerForm, inviteToken: e.target.value })
                  }
                />
              </label>
            )}
            <label>
              Email
              <input
                type="email"
                required
                autoComplete="email"
                value={registerForm.email}
                onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
              />
            </label>
            <label>
              Password (min 8 characters)
              <input
                type="password"
                required
                minLength={8}
                autoComplete="new-password"
                value={registerForm.password}
                onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
              />
            </label>
            <button type="submit" disabled={loading} className="auth-submit">
              {loading ? "Creating account…" : "Create account"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
