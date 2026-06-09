import { useEffect, useMemo, useState } from "react";
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";
import AppShell from "./components/AppShell.jsx";
import AnalyticsPage from "./components/AnalyticsPage.jsx";
import AuthPage from "./components/AuthPage.jsx";
import ChatPage from "./components/ChatPage.jsx";
import DocumentsPage from "./components/DocumentsPage.jsx";
import TeamPage from "./components/TeamPage.jsx";
import {
  EMAIL_KEY,
  getStoredAccessToken,
  getStoredRefreshToken,
  isAccessTokenExpired,
  logoutSession,
  refreshSession,
  saveSession,
  setSessionHandlers,
} from "./api/session.js";
import { parseJwtPayload } from "./utils/jwt.js";

function RequireRole({ allowed, role, children }) {
  if (!allowed.includes(role)) {
    return <Navigate to="/chat" replace />;
  }
  return children;
}

function AppRoutes({
  token,
  setToken,
  error,
  setError,
  loading,
  setLoading,
  chatMessages,
  setChatMessages,
  chatInput,
  setChatInput,
}) {
  const navigate = useNavigate();

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
    setSessionHandlers({
      onTokensUpdated: ({ accessToken }) => {
        if (accessToken) setToken(accessToken);
      },
      onSessionLost: () => {
        setToken("");
        setChatMessages([]);
        setChatInput("");
        navigate("/login", { replace: true });
      },
    });
  }, [navigate, setToken, setChatMessages, setChatInput]);

  useEffect(() => {
    if (token && !session) {
      logoutSession();
      setToken("");
      navigate("/login", { replace: true });
    }
  }, [token, session, setToken, navigate]);

  const userEmail = token ? localStorage.getItem(EMAIL_KEY) || "" : "";

  function handleAuthenticated(accessToken, refreshToken, email) {
    saveSession({ accessToken, refreshToken, email });
    setToken(accessToken);
    setError("");
    setChatMessages([]);
    setChatInput("");
    navigate("/chat", { replace: true });
  }

  async function handleLogout() {
    await logoutSession();
    setToken("");
    setError("");
    setChatMessages([]);
    setChatInput("");
    navigate("/login", { replace: true });
  }

  if (!token || !session) {
    return (
      <Routes>
        <Route
          path="/login"
          element={
            <AuthPage
              onAuthenticated={handleAuthenticated}
              loading={loading}
              setLoading={setLoading}
              error={error}
              setError={setError}
            />
          }
        />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  const sharedProps = {
    userRole: session.role,
    userEmail,
    error,
    setError,
    loading,
    setLoading,
  };

  return (
    <>
      {error && (
        <div className="global-banner error" role="alert">
          <span>{error}</span>
          <button
            type="button"
            className="banner-dismiss"
            onClick={() => setError("")}
            aria-label="Dismiss"
          >
            ×
          </button>
        </div>
      )}
      <Routes>
        <Route path="/login" element={<Navigate to="/chat" replace />} />
        <Route
          element={
            <AppShell
              userEmail={userEmail}
              userRole={session.role}
              onLogout={handleLogout}
            />
          }
        >
          <Route index element={<Navigate to="/chat" replace />} />
          <Route
            path="/chat"
            element={
              <ChatPage
                {...sharedProps}
                messages={chatMessages}
                setMessages={setChatMessages}
                input={chatInput}
                setInput={setChatInput}
              />
            }
          />
          <Route
            path="/documents"
            element={<DocumentsPage {...sharedProps} />}
          />
          <Route
            path="/team"
            element={
              <RequireRole allowed={["admin"]} role={session.role}>
                <TeamPage {...sharedProps} />
              </RequireRole>
            }
          />
          <Route
            path="/analytics"
            element={
              <RequireRole allowed={["admin", "manager"]} role={session.role}>
                <AnalyticsPage />
              </RequireRole>
            }
          />
          <Route path="*" element={<Navigate to="/chat" replace />} />
        </Route>
      </Routes>
    </>
  );
}

export default function App() {
  const [token, setToken] = useState(() => getStoredAccessToken());
  const [bootstrapping, setBootstrapping] = useState(true);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function bootstrap() {
      const refresh = getStoredRefreshToken();
      const access = getStoredAccessToken();
      if (!refresh) {
        if (!cancelled) setBootstrapping(false);
        return;
      }
      try {
        if (!access || isAccessTokenExpired(access)) {
          const newAccess = await refreshSession();
          if (!cancelled) setToken(newAccess);
        } else if (!cancelled) {
          setToken(access);
        }
      } catch {
        if (!cancelled) setToken("");
      } finally {
        if (!cancelled) setBootstrapping(false);
      }
    }

    bootstrap();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!getStoredRefreshToken()) return undefined;

    const intervalMs = 8 * 60 * 1000;
    const id = window.setInterval(() => {
      refreshSession().catch(() => {
        setToken("");
      });
    }, intervalMs);

    return () => window.clearInterval(id);
  }, [token]);

  if (bootstrapping) {
    return (
      <div className="auth-layout">
        <div className="auth-card" style={{ margin: "auto" }}>
          <p>Loading session…</p>
        </div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <AppRoutes
        token={token}
        setToken={setToken}
        error={error}
        setError={setError}
        loading={loading}
        setLoading={setLoading}
        chatMessages={chatMessages}
        setChatMessages={setChatMessages}
        chatInput={chatInput}
        setChatInput={setChatInput}
      />
    </BrowserRouter>
  );
}
