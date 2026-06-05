import { useState } from "react";
import { login, register } from "./api/auth.js";
import { uploadDocument } from "./api/documents.js";
import { askQuestion } from "./api/query.js";

const TOKEN_KEY = "eka_access_token";

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || "");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [registerForm, setRegisterForm] = useState({
    email: "",
    password: "",
    organizationName: "",
  });
  const [loginForm, setLoginForm] = useState({
    email: "",
    password: "",
  });
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [queryQuestion, setQueryQuestion] = useState("");
  const [queryResult, setQueryResult] = useState(null);

  function saveToken(accessToken) {
    localStorage.setItem(TOKEN_KEY, accessToken);
    setToken(accessToken);
  }

  function clearToken() {
    localStorage.removeItem(TOKEN_KEY);
    setToken("");
  }

  async function handleRegister(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await register(registerForm);
      saveToken(data.access_token);
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
      saveToken(data.access_token);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload(e) {
    e.preventDefault();
    setError("");
    setUploadResult(null);

    if (!token) {
      setError("Login first to upload documents.");
      return;
    }
    if (!uploadFile) {
      setError("Choose a PDF file.");
      return;
    }

    setLoading(true);
    try {
      const data = await uploadDocument({ file: uploadFile, accessToken: token });
      setUploadResult(data);
      setUploadFile(null);
      e.target.reset();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleQuery(e) {
    e.preventDefault();
    setError("");
    setQueryResult(null);

    if (!token) {
      setError("Login first to ask questions.");
      return;
    }
    if (!queryQuestion.trim()) {
      setError("Enter a question.");
      return;
    }

    setLoading(true);
    try {
      const data = await askQuestion({ question: queryQuestion.trim(), accessToken: token });
      setQueryResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header>
        <h1>Enterprise Knowledge Assistant</h1>
        <p>Day 3 — Register, upload &amp; ask questions</p>
      </header>

      {error && <div className="alert error">{error}</div>}

      <div className="grid">
        <section className="card">
          <h2>Register</h2>
          <p className="hint">Creates a new organization and admin user.</p>
          <form onSubmit={handleRegister}>
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
            <label>
              Email
              <input
                type="email"
                required
                value={registerForm.email}
                onChange={(e) =>
                  setRegisterForm({ ...registerForm, email: e.target.value })
                }
              />
            </label>
            <label>
              Password (min 8)
              <input
                type="password"
                required
                minLength={8}
                value={registerForm.password}
                onChange={(e) =>
                  setRegisterForm({ ...registerForm, password: e.target.value })
                }
              />
            </label>
            <button type="submit" disabled={loading}>
              {loading ? "Working…" : "Register"}
            </button>
          </form>
        </section>

        <section className="card">
          <h2>Login</h2>
          <p className="hint">Sign in with an existing account.</p>
          <form onSubmit={handleLogin}>
            <label>
              Email
              <input
                type="email"
                required
                value={loginForm.email}
                onChange={(e) =>
                  setLoginForm({ ...loginForm, email: e.target.value })
                }
              />
            </label>
            <label>
              Password
              <input
                type="password"
                required
                value={loginForm.password}
                onChange={(e) =>
                  setLoginForm({ ...loginForm, password: e.target.value })
                }
              />
            </label>
            <button type="submit" disabled={loading}>
              {loading ? "Working…" : "Login"}
            </button>
          </form>
        </section>
      </div>

      <section className="card token-card">
        <h2>Upload PDF</h2>
        <p className="hint">Admin only. Login first — token is sent automatically.</p>
        <form onSubmit={handleUpload}>
          <label>
            PDF file
            <input
              type="file"
              accept="application/pdf,.pdf"
              required
              onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
            />
          </label>
          <button type="submit" disabled={loading || !token}>
            {loading ? "Uploading…" : "Upload"}
          </button>
        </form>
        {uploadResult && (
          <div className="alert success">
            <strong>{uploadResult.filename}</strong> — {uploadResult.status},{" "}
            {uploadResult.chunk_count} chunk(s)
            <pre className="upload-meta">{JSON.stringify(uploadResult, null, 2)}</pre>
          </div>
        )}
      </section>

      <section className="card token-card">
        <h2>Ask a question</h2>
        <p className="hint">Login and upload PDFs first — answers use your org&apos;s indexed documents.</p>
        <form onSubmit={handleQuery}>
          <label>
            Question
            <textarea
              required
              rows={3}
              value={queryQuestion}
              placeholder="e.g. How many PTO days do employees receive?"
              onChange={(e) => setQueryQuestion(e.target.value)}
            />
          </label>
          <button type="submit" disabled={loading || !token}>
            {loading ? "Searching…" : "Ask"}
          </button>
        </form>
        {queryResult && (
          <div className="alert success query-result">
            <p className="answer-text">{queryResult.answer}</p>
            {queryResult.citations?.length > 0 && (
              <div className="citations">
                <strong>Sources</strong>
                <ul>
                  {queryResult.citations.map((c) => (
                    <li key={c.chunk_id}>
                      {c.document}
                      {c.page != null && ` · p.${c.page}`}
                      {c.section && ` · ${c.section}`}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <pre className="upload-meta">{JSON.stringify(queryResult, null, 2)}</pre>
          </div>
        )}
      </section>

      <section className="card token-card">
        <div className="token-header">
          <h2>Access token</h2>
          {token && (
            <button type="button" className="secondary" onClick={clearToken}>
              Clear
            </button>
          )}
        </div>
        {token ? (
          <pre className="token">{token}</pre>
        ) : (
          <p className="hint">Register or login to receive a JWT.</p>
        )}
      </section>

      <footer>
        <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">
          API docs
        </a>
      </footer>
    </div>
  );
}
