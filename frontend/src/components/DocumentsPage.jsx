import { useCallback, useEffect, useRef, useState } from "react";
import {
  deleteDocument,
  getDocumentStatus,
  listDocuments,
  openDocumentPdf,
  uploadDocument,
} from "../api/documents.js";

const ACCESS_LEVELS = [
  { value: "public", label: "Public" },
  { value: "hr", label: "HR" },
  { value: "engineering", label: "Engineering" },
  { value: "finance", label: "Finance" },
  { value: "admin_only", label: "Admin only" },
];

function statusLabel(status) {
  if (status === "ready") return "Ready";
  if (status === "processing") return "Processing";
  if (status === "failed") return "Failed";
  return status;
}

export default function DocumentsPage({
  token,
  userEmail,
  userRole,
  onBack,
  onLogout,
  error,
  setError,
  loading,
  setLoading,
}) {
  const [documents, setDocuments] = useState([]);
  const [refreshing, setRefreshing] = useState(true);
  const [updatingId, setUpdatingId] = useState(null);
  const fileInputRef = useRef(null);
  const replaceTargetRef = useRef(null);
  const replaceAccessLevelRef = useRef("public");

  const loadDocuments = useCallback(async () => {
    setRefreshing(true);
    try {
      const data = await listDocuments({ accessToken: token });
      setDocuments(data.items ?? []);
    } catch (err) {
      setError(err.message);
      setDocuments([]);
    } finally {
      setRefreshing(false);
    }
  }, [token, setError]);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  useEffect(() => {
    const processingIds = documents
      .filter((doc) => doc.status === "processing")
      .map((doc) => doc.id);
    if (processingIds.length === 0) return;

    const intervalId = setInterval(async () => {
      try {
        const updates = await Promise.all(
          processingIds.map((id) => getDocumentStatus({ documentId: id, accessToken: token }))
        );
        setDocuments((prev) =>
          prev.map((doc) => {
            const updated = updates.find((item) => item.id === doc.id);
            return updated ?? doc;
          })
        );
      } catch {
        // ignore transient poll errors
      }
    }, 2000);

    return () => clearInterval(intervalId);
  }, [documents, token]);

  function startUpdate(doc) {
    const select = document.querySelector(`select[data-doc-id="${doc.id}"]`);
    replaceAccessLevelRef.current = select?.value ?? doc.access_level;
    replaceTargetRef.current = doc;
    setUpdatingId(doc.id);
    fileInputRef.current?.click();
  }

  async function handleReplaceFile(e) {
    const file = e.target.files?.[0];
    const target = replaceTargetRef.current;
    e.target.value = "";
    setUpdatingId(null);
    replaceTargetRef.current = null;

    if (!file || !target) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are allowed.");
      return;
    }

    setError("");
    setLoading(true);
    try {
      const updated = await uploadDocument({
        file,
        accessToken: token,
        accessLevel: replaceAccessLevelRef.current,
      });
      setDocuments((prev) => {
        const withoutStale = prev.filter(
          (doc) => doc.id !== target.id && doc.filename !== updated.filename
        );
        return [updated, ...withoutStale];
      });
      await loadDocuments();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(doc) {
    const confirmed = window.confirm(
      `Delete "${doc.filename}"? This removes the PDF and all indexed search data.`
    );
    if (!confirmed) return;

    setError("");
    setLoading(true);
    try {
      await deleteDocument({ documentId: doc.id, accessToken: token });
      setDocuments((prev) => prev.filter((item) => item.id !== doc.id));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handlePreview(doc) {
    if (doc.status !== "ready") return;
    try {
      await openDocumentPdf({ documentId: doc.id, accessToken: token });
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="chat-layout">
      <header className="chat-header">
        <div className="chat-header-left">
          <h1>Documents</h1>
          {userEmail && (
            <span className="user-badge">
              {userEmail}
              <span className="role-pill">{userRole}</span>
            </span>
          )}
        </div>
        <div className="chat-header-actions">
          <button type="button" className="secondary header-btn" onClick={onBack}>
            Back to chat
          </button>
          <button type="button" className="secondary header-btn" onClick={onLogout}>
            Sign out
          </button>
        </div>
      </header>

      {error && <div className="alert error chat-banner">{error}</div>}

      <main className="documents-main page">
        <div className="documents-toolbar">
          <p className="hint">
            Prototype limits: 15 pages per PDF, 15 documents per organization (
            {documents.length}/15). Replace by uploading a new PDF. Delete removes the file and
            its search index.
          </p>
          <button
            type="button"
            className="secondary"
            onClick={loadDocuments}
            disabled={refreshing || loading}
          >
            {refreshing ? "Refreshing…" : "Refresh"}
          </button>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf,.pdf"
          className="sr-only"
          onChange={handleReplaceFile}
        />

        {refreshing && documents.length === 0 ? (
          <p className="hint">Loading documents…</p>
        ) : documents.length === 0 ? (
          <div className="card documents-empty">
            <h2>No documents yet</h2>
            <p className="hint">Upload a PDF from the Admin panel on the chat page.</p>
          </div>
        ) : (
          <ul className="document-list">
            {documents.map((doc) => (
              <li key={doc.id} className="document-row card">
                <div className="document-row-main">
                  <button
                    type="button"
                    className="document-filename"
                    onClick={() => handlePreview(doc)}
                    disabled={doc.status !== "ready"}
                    title={doc.status === "ready" ? "Open PDF" : "Not ready yet"}
                  >
                    {doc.filename}
                  </button>
                  <div className="document-meta">
                    <span className={`status-pill status-${doc.status}`}>
                      {statusLabel(doc.status)}
                    </span>
                    <span>{doc.access_level} access</span>
                    <span>{doc.chunk_count} chunk(s)</span>
                    <span>{new Date(doc.created_at).toLocaleString()}</span>
                  </div>
                </div>
                <div className="document-actions">
                  <label className="document-update-level">
                    <span className="sr-only">Access level for replacement upload</span>
                    <select
                      data-doc-id={doc.id}
                      defaultValue={doc.access_level}
                      disabled={loading}
                    >
                      {ACCESS_LEVELS.map((level) => (
                        <option key={level.value} value={level.value}>
                          {level.label}
                        </option>
                      ))}
                    </select>
                  </label>
                  <button
                    type="button"
                    className="secondary"
                    onClick={() => startUpdate(doc)}
                    disabled={loading}
                  >
                    {loading && updatingId === doc.id ? "Updating…" : "Update"}
                  </button>
                  <button
                    type="button"
                    className="danger-btn"
                    onClick={() => handleDelete(doc)}
                    disabled={loading}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
