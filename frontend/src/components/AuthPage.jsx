import { useEffect, useState } from "react";
import { fetchDemoCredentials, login, register } from "../api/auth.js";
import DemoCredentialsHint from "./DemoCredentialsHint.jsx";

const ENV_DEMO_EMAIL = import.meta.env.VITE_DEMO_ADMIN_EMAIL?.trim() || "";
const ENV_DEMO_PASSWORD = import.meta.env.VITE_DEMO_ADMIN_PASSWORD || "";

export default function AuthPage({ onAuthenticated, loading, setLoading, error, setError }) {
  const [authTab, setAuthTab] = useState("signin");
  const [demoCredentials, setDemoCredentials] = useState(() =>
    ENV_DEMO_EMAIL && ENV_DEMO_PASSWORD
      ? { email: ENV_DEMO_EMAIL, password: ENV_DEMO_PASSWORD }
      : null,
  );
  const [registerMode, setRegisterMode] = useState("org");
  const [registerForm, setRegisterForm] = useState({
    email: "",
    password: "",
    organizationName: "",
    inviteToken: "",
  });
  const [loginForm, setLoginForm] = useState({ email: "", password: "" });

  useEffect(() => {
    if (demoCredentials) return undefined;

    let cancelled = false;
    fetchDemoCredentials()
      .then((data) => {
        if (!cancelled && data?.email && data?.password) {
          setDemoCredentials({ email: data.email, password: data.password });
        }
      })
      .catch(() => {});

    return () => {
      cancelled = true;
    };
  }, [demoCredentials]);

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
      onAuthenticated(data.access_token, data.refresh_token, registerForm.email);
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
      onAuthenticated(data.access_token, data.refresh_token, loginForm.email);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-layout">
      <section className="auth-showcase">
        <div className="auth-showcase-inner">
          <div className="brand-mark large">EK</div>
          <h1>Enterprise Knowledge Assistant</h1>
          <p>
            Your team&apos;s policies, handbooks, and docs — searchable in plain language with
            grounded answers and citations.
          </p>
          <ul className="auth-features">
            <li>Multi-tenant workspaces per organization</li>
            <li>Role-based access to sensitive documents</li>
            <li>Streaming answers with source links</li>
          </ul>
        </div>
      </section>

      <section className="auth-panel">
        <div className="auth-card">
          <div className="auth-card-header">
            <div>
              <h2>Welcome back</h2>
              <p className="auth-subtitle">Sign in or create an account to continue.</p>
            </div>
            {demoCredentials && authTab === "signin" && (
              <DemoCredentialsHint
                email={demoCredentials.email}
                password={demoCredentials.password}
                onUseDemo={() =>
                  setLoginForm({
                    email: demoCredentials.email,
                    password: demoCredentials.password,
                  })
                }
              />
            )}
          </div>

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

          {error && <div className="inline-alert error">{error}</div>}

          {authTab === "signin" ? (
            <form onSubmit={handleLogin} className="form-stack">
              <label>
                Email
                <input
                  type="email"
                  required
                  autoComplete="email"
                  placeholder="you@company.com"
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
              <button type="submit" disabled={loading} className="btn-primary btn-full">
                {loading ? "Signing in…" : "Sign in"}
              </button>
            </form>
          ) : (
            <form onSubmit={handleRegister} className="form-stack">
              <div className="segmented">
                <button
                  type="button"
                  className={registerMode === "org" ? "active" : ""}
                  onClick={() => setRegisterMode("org")}
                >
                  New organization
                </button>
                <button
                  type="button"
                  className={registerMode === "invite" ? "active" : ""}
                  onClick={() => setRegisterMode("invite")}
                >
                  Invite code
                </button>
              </div>
              {registerMode === "org" ? (
                <label>
                  Organization name
                  <input
                    required
                    placeholder="Acme Corporation"
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
                    placeholder="Paste invite code"
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
                Password
                <input
                  type="password"
                  required
                  minLength={8}
                  autoComplete="new-password"
                  placeholder="Minimum 8 characters"
                  value={registerForm.password}
                  onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
                />
              </label>
              <button type="submit" disabled={loading} className="btn-primary btn-full">
                {loading ? "Creating account…" : "Create account"}
              </button>
            </form>
          )}
        </div>
      </section>
    </div>
  );
}
