import { useEffect, useRef, useState } from "react";
import { inviteUser } from "../api/auth.js";
import { uploadDocument } from "../api/documents.js";
import { askQuestion } from "../api/query.js";

const ACCESS_LEVELS = [
  { value: "public", label: "Public" },
  { value: "hr", label: "HR" },
  { value: "engineering", label: "Engineering" },
  { value: "finance", label: "Finance" },
  { value: "admin_only", label: "Admin only" },
];

const INVITE_ROLES = [
  { value: "employee", label: "Employee" },
  { value: "manager", label: "Manager" },
  { value: "admin", label: "Admin" },
];

function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`chat-message ${isUser ? "user" : "assistant"}`}>
      <div className="chat-message-inner">
        <span className="chat-role">{isUser ? "You" : "Assistant"}</span>
        <p className="chat-content">{message.content}</p>
        {!isUser && message.citations?.length > 0 && (
          <div className="chat-citations">
            <span className="chat-citations-label">Sources</span>
            <ul>
              {message.citations.map((c) => (
                <li key={c.chunk_id}>
                  {c.document}
                  {c.page != null && ` · p.${c.page}`}
                  {c.section && ` · ${c.section}`}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ChatPage({
  token,
  userRole,
  userEmail,
  onLogout,
  error,
  setError,
  loading,
  setLoading,
}) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [adminOpen, setAdminOpen] = useState(false);
  const [inviteForm, setInviteForm] = useState({ email: "", role: "employee" });
  const [inviteSuccess, setInviteSuccess] = useState(null);
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadAccessLevel, setUploadAccessLevel] = useState("public");
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const isAdmin = userRole === "admin";

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  function handleInputKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend(e);
    }
  }

  async function handleSend(e) {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setError("");
    setInput("");
    const userMessage = { id: crypto.randomUUID(), role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const data = await askQuestion({ question, accessToken: token });
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.answer,
          citations: data.citations ?? [],
        },
      ]);
    } catch (err) {
      setError(err.message);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
      textareaRef.current?.focus();
    }
  }

  async function handleInvite(e) {
    e.preventDefault();
    setError("");
    setInviteSuccess(null);
    setLoading(true);
    try {
      const data = await inviteUser({
        email: inviteForm.email,
        role: inviteForm.role,
        accessToken: token,
      });
      setInviteSuccess(data);
      setInviteForm({ email: "", role: "employee" });
      e.target.reset();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload(e) {
    e.preventDefault();
    setError("");
    setUploadSuccess(null);
    if (!uploadFile) {
      setError("Choose a PDF file.");
      return;
    }
    setLoading(true);
    try {
      const data = await uploadDocument({
        file: uploadFile,
        accessToken: token,
        accessLevel: uploadAccessLevel,
      });
      setUploadSuccess(data);
      setUploadFile(null);
      e.target.reset();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function copyInviteCode() {
    if (inviteSuccess?.token) {
      navigator.clipboard.writeText(inviteSuccess.token);
    }
  }

  return (
    <div className="chat-layout">
      <header className="chat-header">
        <div className="chat-header-left">
          <h1>Knowledge Assistant</h1>
          {userEmail && (
            <span className="user-badge">
              {userEmail}
              <span className="role-pill">{userRole}</span>
            </span>
          )}
        </div>
        <div className="chat-header-actions">
          {isAdmin && (
            <button
              type="button"
              className="secondary header-btn"
              onClick={() => setAdminOpen((open) => !open)}
            >
              {adminOpen ? "Close admin" : "Admin"}
            </button>
          )}
          <button type="button" className="secondary header-btn" onClick={onLogout}>
            Sign out
          </button>
        </div>
      </header>

      {error && <div className="alert error chat-banner">{error}</div>}

      {isAdmin && adminOpen && (
        <aside className="admin-panel card">
          <h2>Admin</h2>
          <div className="admin-grid">
            <section className="admin-section">
              <h3>Invite user</h3>
              <p className="hint">Share the invite code with the new team member.</p>
              <form onSubmit={handleInvite}>
                <label>
                  Email
                  <input
                    type="email"
                    required
                    value={inviteForm.email}
                    onChange={(e) => setInviteForm({ ...inviteForm, email: e.target.value })}
                  />
                </label>
                <label>
                  Role
                  <select
                    value={inviteForm.role}
                    onChange={(e) => setInviteForm({ ...inviteForm, role: e.target.value })}
                  >
                    {INVITE_ROLES.map((r) => (
                      <option key={r.value} value={r.value}>
                        {r.label}
                      </option>
                    ))}
                  </select>
                </label>
                <button type="submit" disabled={loading}>
                  {loading ? "Creating…" : "Create invite"}
                </button>
              </form>
              {inviteSuccess && (
                <div className="alert success admin-feedback">
                  <p>
                    Invite sent to <strong>{inviteSuccess.email}</strong>
                  </p>
                  <div className="invite-code-row">
                    <code className="invite-code">{inviteSuccess.token}</code>
                    <button type="button" className="secondary" onClick={copyInviteCode}>
                      Copy
                    </button>
                  </div>
                </div>
              )}
            </section>

            <section className="admin-section">
              <h3>Upload PDF</h3>
              <p className="hint">Documents are indexed for search by access level.</p>
              <form onSubmit={handleUpload}>
                <label>
                  Access level
                  <select
                    value={uploadAccessLevel}
                    onChange={(e) => setUploadAccessLevel(e.target.value)}
                  >
                    {ACCESS_LEVELS.map((level) => (
                      <option key={level.value} value={level.value}>
                        {level.label}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  PDF file
                  <input
                    type="file"
                    accept="application/pdf,.pdf"
                    required
                    onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                  />
                </label>
                <button type="submit" disabled={loading}>
                  {loading ? "Uploading…" : "Upload"}
                </button>
              </form>
              {uploadSuccess && (
                <div className="alert success admin-feedback">
                  <strong>{uploadSuccess.filename}</strong> indexed ({uploadSuccess.chunk_count}{" "}
                  chunks, {uploadSuccess.access_level})
                </div>
              )}
            </section>
          </div>
        </aside>
      )}

      <main className="chat-main">
        <div className="chat-messages">
          {messages.length === 0 && !loading && (
            <div className="chat-empty">
              <h2>How can I help you today?</h2>
              <p>Ask questions about your organization&apos;s uploaded documents.</p>
            </div>
          )}
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          {loading && messages.length > 0 && messages[messages.length - 1].role === "user" && (
            <div className="chat-message assistant">
              <div className="chat-message-inner">
                <span className="chat-role">Assistant</span>
                <p className="chat-content typing">Thinking…</p>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="chat-composer" onSubmit={handleSend}>
          <textarea
            ref={textareaRef}
            rows={1}
            placeholder="Ask a question…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleInputKeyDown}
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            Send
          </button>
        </form>
      </main>
    </div>
  );
}
