import { useEffect, useMemo, useState } from "react";
import AuthPage from "./components/AuthPage.jsx";
import ChatPage from "./components/ChatPage.jsx";
import DocumentsPage from "./components/DocumentsPage.jsx";
import { parseJwtPayload } from "./utils/jwt.js";

const TOKEN_KEY = "eka_access_token";
const EMAIL_KEY = "eka_user_email";

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || "");
  const [view, setView] = useState("chat");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const session = useMemo(() => {
    if (!token) return null;
    const payload = parseJwtPayload(token);
    if (!payload?.role) return null;
    return {
      role: payload.role,
      userId: payload.sub,
    };
  }, [token]);

  useEffect(() => {
    if (token && !session) {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(EMAIL_KEY);
      setToken("");
    }
  }, [token, session]);

  const userEmail = token ? localStorage.getItem(EMAIL_KEY) || "" : "";

  function handleAuthenticated(accessToken, email) {
    localStorage.setItem(TOKEN_KEY, accessToken);
    if (email) localStorage.setItem(EMAIL_KEY, email);
    setToken(accessToken);
    setError("");
  }

  function handleLogout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(EMAIL_KEY);
    setToken("");
    setView("chat");
    setError("");
  }

  if (!token || !session) {
    return (
      <AuthPage
        onAuthenticated={handleAuthenticated}
        loading={loading}
        setLoading={setLoading}
        error={error}
        setError={setError}
      />
    );
  }

  if (view === "documents" && session.role === "admin") {
    return (
      <DocumentsPage
        token={token}
        userRole={session.role}
        userEmail={userEmail}
        onBack={() => setView("chat")}
        onLogout={handleLogout}
        error={error}
        setError={setError}
        loading={loading}
        setLoading={setLoading}
      />
    );
  }

  return (
    <ChatPage
      token={token}
      userRole={session.role}
      userEmail={userEmail}
      onLogout={handleLogout}
      onOpenDocuments={() => setView("documents")}
      error={error}
      setError={setError}
      loading={loading}
      setLoading={setLoading}
    />
  );
}
