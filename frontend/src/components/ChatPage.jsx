import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import { listRecentQueries } from "../api/analytics.js";
import { inviteUser } from "../api/auth.js";
import { getDocumentStatus, openDocumentPdf, uploadDocument } from "../api/documents.js";
import { askQuestionStream } from "../api/query.js";
import {
  buildSourceMap,
  citationLinkLabel,
  citationLinkTitle,
  firstSourceIndex,
  splitAnswerParagraphs,
  stripSourceRefs,
} from "../utils/citations.js";

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

function AssistantAnswer({ content, citations, accessToken, onCitationError }) {
  const sourceMap = buildSourceMap(citations);
  const paragraphs = splitAnswerParagraphs(content);

  async function handleCitationClick(citation) {
    if (!citation?.document_id || !accessToken) return;
    try {
      await openDocumentPdf({
        documentId: citation.document_id,
        page: citation.page,
        accessToken,
      });
    } catch (err) {
      onCitationError?.(err.message);
    }
  }

  if (paragraphs.length === 0) {
    return null;
  }

  return (
    <div className="chat-content chat-markdown chat-answer-paragraphs">
      {paragraphs.map((paragraph, index) => {
        const sourceIndex = firstSourceIndex(paragraph);
        const citation = sourceIndex != null ? sourceMap.get(sourceIndex) : null;
        const cleanText = stripSourceRefs(paragraph);

        return (
          <p key={index} className="answer-paragraph">
            <span className="answer-paragraph-text">
              <ReactMarkdown
                rehypePlugins={[rehypeSanitize]}
                components={{
                  p: ({ children }) => <span>{children}</span>,
                }}
              >
                {cleanText}
              </ReactMarkdown>
            </span>
            {citation && (
              <>
                {" "}
                <button
                  type="button"
                  className="citation-inline"
                  onClick={() => handleCitationClick(citation)}
                  title={citationLinkTitle(citation)}
                >
                  {citationLinkLabel(citation)}
                </button>
              </>
            )}
          </p>
        );
      })}
    </div>
  );
}

function ChatMessage({ message, accessToken, onCitationError }) {
  const isUser = message.role === "user";

  return (
    <div className={`chat-message ${isUser ? "user" : "assistant"}`}>
      <div className="chat-message-inner">
        <span className="chat-role">{isUser ? "You" : "Assistant"}</span>
        {isUser ? (
          <p className="chat-content">{message.content}</p>
        ) : message.streaming && !message.content ? (
          <p className="chat-content typing">Generating answer…</p>
        ) : (
          <AssistantAnswer
            content={message.content}
            citations={message.citations}
            accessToken={accessToken}
            onCitationError={onCitationError}
          />
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
  onOpenDocuments,
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
  const [queryLogs, setQueryLogs] = useState([]);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const isAdmin = userRole === "admin";
  const canViewAnalytics = userRole === "admin" || userRole === "manager";

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (!adminOpen || !canViewAnalytics) return;
    listRecentQueries({ accessToken: token, limit: 10 })
      .then((data) => setQueryLogs(data.items ?? []))
      .catch(() => setQueryLogs([]));
  }, [adminOpen, canViewAnalytics, token, messages.length]);

  useEffect(() => {
    if (!uploadSuccess?.id || uploadSuccess.status !== "processing") return;

    const documentId = uploadSuccess.id;
    const intervalId = setInterval(async () => {
      try {
        const doc = await getDocumentStatus({ documentId, accessToken: token });
        if (doc.status !== "processing") {
          setUploadSuccess(doc);
        }
      } catch {
        // ignore transient poll errors
      }
    }, 2000);

    return () => clearInterval(intervalId);
  }, [uploadSuccess?.id, uploadSuccess?.status, token]);

  function uploadStatusMessage(doc) {
    if (doc.status === "processing") {
      return "We're preparing your document for search…";
    }
    if (doc.status === "ready") {
      return "Your document is ready — you can ask questions about it now.";
    }
    if (doc.status === "failed") {
      return "We couldn't prepare this document. Please try uploading again.";
    }
    return doc.status;
  }

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
    const assistantId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      {
        id: assistantId,
        role: "assistant",
        content: "",
        citations: [],
        streaming: true,
      },
    ]);

    try {
      await askQuestionStream({
        question,
        accessToken: token,
        onCitations: () => {
          // Citations arrive in onDone with source_index for inline links
        },
        onToken: (text) => {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId ? { ...m, content: m.content + text } : m
            )
          );
        },
        onDone: (payload) => {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? {
                    ...m,
                    content: payload.answer ?? m.content,
                    citations: payload.citations ?? m.citations,
                    streaming: false,
                  }
                : m
            )
          );
        },
      });
    } catch (err) {
      const errorMessage = err.message || "Something went wrong. Please try again.";
      setError(errorMessage);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? {
                ...m,
                content: errorMessage,
                streaming: false,
              }
            : m
        )
      );
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
          {(isAdmin || canViewAnalytics) && (
            <button
              type="button"
              className="secondary header-btn"
              onClick={() => setAdminOpen((open) => !open)}
            >
              {adminOpen ? "Close" : isAdmin ? "Admin" : "Analytics"}
            </button>
          )}
          <button type="button" className="secondary header-btn" onClick={onLogout}>
            Sign out
          </button>
        </div>
      </header>

      {error && <div className="alert error chat-banner">{error}</div>}

      {(isAdmin || canViewAnalytics) && adminOpen && (
        <aside className="admin-panel card">
          <div className="admin-panel-head">
            <h2>{isAdmin ? "Admin" : "Analytics"}</h2>
            {isAdmin && (
              <button
                type="button"
                className="secondary header-btn"
                onClick={() => {
                  setAdminOpen(false);
                  onOpenDocuments?.();
                }}
              >
                Documents
              </button>
            )}
          </div>
          <div className="admin-grid">
            {isAdmin && (
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
            )}

            {isAdmin && (
            <section className="admin-section">
              <h3>Upload PDF</h3>
              <p className="hint">
                Prototype limits: up to 15 pages per PDF and 15 documents per organization.
                Documents are indexed for search by access level.
              </p>
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
                <div
                  className={
                    uploadSuccess.status === "failed"
                      ? "alert error admin-feedback"
                      : `alert success admin-feedback${
                          uploadSuccess.status === "processing" ? " upload-status-processing" : ""
                        }`
                  }
                >
                  <strong>{uploadSuccess.filename}</strong>
                  <p className="upload-status-text">{uploadStatusMessage(uploadSuccess)}</p>
                  {uploadSuccess.status === "ready" && (
                    <p className="upload-status-meta">
                      {uploadSuccess.chunk_count} section(s) indexed · {uploadSuccess.access_level}{" "}
                      access
                    </p>
                  )}
                </div>
              )}
            </section>
            )}

            {canViewAnalytics && (
              <section className="admin-section admin-section-wide">
                <h3>Recent queries</h3>
                <p className="hint">Logged after each question (latency + chunks used).</p>
                {queryLogs.length === 0 ? (
                  <p className="hint">No queries logged yet.</p>
                ) : (
                  <ul className="query-log-list">
                    {queryLogs.map((log) => (
                      <li key={log.id}>
                        <strong>{log.question}</strong>
                        <span className="query-log-meta">
                          {log.latency_ms} ms · {log.retrieved_chunk_ids?.length ?? 0} chunks
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </section>
            )}
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
            <ChatMessage
              key={msg.id}
              message={msg}
              accessToken={token}
              onCitationError={setError}
            />
          ))}
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
