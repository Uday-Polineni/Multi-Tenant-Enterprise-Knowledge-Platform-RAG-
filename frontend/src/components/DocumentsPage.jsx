import { useCallback, useEffect, useRef, useState } from "react";
import {
  deleteDocument,
  getDocumentStatus,
  listDocuments,
  openDocumentPdf,
  updateDocumentAccessLevel,
  uploadDocument,
} from "../api/documents.js";
import { ACCESS_LEVELS } from "../constants.js";

function statusLabel(status) {
  if (status === "ready") return "Ready";
  if (status === "processing") return "Processing";
  if (status === "failed") return "Failed";
  return status;
}

function accessLevelLabel(value) {
  return ACCESS_LEVELS.find((level) => level.value === value)?.label ?? value;
}

export default function DocumentsPage({ userRole, setError, loading, setLoading }) {
  const readOnly = userRole !== "admin";
  const [documents, setDocuments] = useState([]);
  const [refreshing, setRefreshing] = useState(true);
  const [updatingId, setUpdatingId] = useState(null);
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadAccessLevel, setUploadAccessLevel] = useState("public");
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);
  const replaceInputRef = useRef(null);
  const replaceTargetRef = useRef(null);
  const replaceAccessLevelRef = useRef("public");

  const loadDocuments = useCallback(async () => {
    setRefreshing(true);
    try {
      const data = await listDocuments();
      setDocuments(data.items ?? []);
    } catch (err) {
      setError(err.message);
      setDocuments([]);
    } finally {
      setRefreshing(false);
    }
  }, [setError]);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  useEffect(() => {
    if (readOnly) return undefined;

    const processingIds = documents
      .filter((doc) => doc.status === "processing")
      .map((doc) => doc.id);
    if (processingIds.length === 0) return undefined;

    const intervalId = setInterval(async () => {
      try {
        const updates = await Promise.all(
          processingIds.map((id) => getDocumentStatus({ documentId: id }))
        );
        setDocuments((prev) =>
          prev.map((doc) => updates.find((item) => item.id === doc.id) ?? doc)
        );
      } catch {
        // ignore transient poll errors
      }
    }, 2000);

    return () => clearInterval(intervalId);
  }, [documents, readOnly]);

  async function handleUpload(file, accessLevel = uploadAccessLevel) {
    if (!file) {
      setError("Choose a PDF file.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const uploaded = await uploadDocument({
        file,
        accessLevel,
      });
      setDocuments((prev) => {
        const filtered = prev.filter(
          (doc) => doc.id !== uploaded.id && doc.filename !== uploaded.filename
        );
        return [uploaded, ...filtered];
      });
      setUploadFile(null);
      await loadDocuments();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleUploadSubmit(e) {
    e.preventDefault();
    await handleUpload(uploadFile);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      setUploadFile(file);
      handleUpload(file);
    }
  }

  function startUpdate(doc) {
    const select = document.querySelector(`select[data-doc-id="${doc.id}"]`);
    replaceAccessLevelRef.current = select?.value ?? doc.access_level;
    replaceTargetRef.current = doc;
    setUpdatingId(doc.id);
    replaceInputRef.current?.click();
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
    await handleUpload(file, replaceAccessLevelRef.current);
  }

  async function handleAccessLevelSave(doc) {
    const select = document.querySelector(`select[data-doc-id="${doc.id}"]`);
    const accessLevel = select?.value ?? doc.access_level;
    if (accessLevel === doc.access_level) return;

    setError("");
    setUpdatingId(doc.id);
    setLoading(true);
    try {
      const updated = await updateDocumentAccessLevel({
        documentId: doc.id,
        accessLevel,
      });
      setDocuments((prev) =>
        prev.map((item) => (item.id === updated.id ? updated : item))
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setUpdatingId(null);
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
      await deleteDocument({ documentId: doc.id });
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
      await openDocumentPdf({ documentId: doc.id });
    } catch (err) {
      setError(err.message);
    }
  }

  const readyCount = documents.filter((doc) => doc.status === "ready").length;

  return (
    <div className="page-view">
      <header className="page-header">
        <div>
          <h1>{readOnly ? "Library" : "Documents"}</h1>
          <p>
            {readOnly
              ? "PDFs you can ask questions about, based on your role."
              : "Upload and manage the PDFs your assistant searches."}
          </p>
        </div>
        <button
          type="button"
          className="btn-secondary"
          onClick={loadDocuments}
          disabled={refreshing || loading}
        >
          {refreshing ? "Refreshing…" : "Refresh"}
        </button>
      </header>

      <div className="stat-row">
        <div className="stat-card">
          <span className="stat-label">
            {readOnly ? "Available to you" : "Total documents"}
          </span>
          <strong className="stat-value">{documents.length}</strong>
        </div>
        {!readOnly && (
          <div className="stat-card">
            <span className="stat-label">Ready for search</span>
            <strong className="stat-value">{readyCount}</strong>
          </div>
        )}
      </div>

      {!readOnly && (
        <section
          className={`upload-zone${dragOver ? " drag-over" : ""}`}
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
        >
          <form className="upload-form" onSubmit={handleUploadSubmit}>
            <div className="upload-copy">
              <h2>Upload a PDF</h2>
              <p>Drag and drop a file here, or browse from your computer.</p>
            </div>
            <div className="upload-controls">
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
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf,.pdf"
                className="sr-only"
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
              />
              <button
                type="button"
                className="btn-secondary"
                onClick={() => fileInputRef.current?.click()}
              >
                Browse files
              </button>
              <button type="submit" className="btn-primary" disabled={loading || !uploadFile}>
                {loading ? "Uploading…" : "Upload PDF"}
              </button>
            </div>
            {uploadFile && <p className="upload-filename">Selected: {uploadFile.name}</p>}
          </form>
        </section>
      )}

      {!readOnly && (
        <input
          ref={replaceInputRef}
          type="file"
          accept="application/pdf,.pdf"
          className="sr-only"
          onChange={handleReplaceFile}
        />
      )}

      <section className="panel">
        <h2>{readOnly ? "Your knowledge base" : "Your library"}</h2>
        {refreshing && documents.length === 0 ? (
          <p className="panel-desc">Loading documents…</p>
        ) : documents.length === 0 ? (
          <div className="empty-state compact">
            <h3>{readOnly ? "No documents available" : "No documents yet"}</h3>
            <p>
              {readOnly
                ? "Nothing is indexed for your access level yet. Ask your admin if you expected files here."
                : "Upload your first PDF above to start asking questions."}
            </p>
          </div>
        ) : (
          <ul className="document-list">
            {documents.map((doc) => (
              <li key={doc.id} className="document-card">
                <button
                  type="button"
                  className="document-card-title"
                  onClick={() => handlePreview(doc)}
                  disabled={doc.status !== "ready"}
                >
                  {doc.filename}
                </button>
                <div className="document-card-meta">
                  {!readOnly && (
                    <span className={`status-pill status-${doc.status}`}>
                      {statusLabel(doc.status)}
                    </span>
                  )}
                  <span>{accessLevelLabel(doc.access_level)}</span>
                  <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                </div>
                {!readOnly && (
                  <div className="document-card-actions">
                    <select
                      key={`${doc.id}-${doc.access_level}`}
                      data-doc-id={doc.id}
                      defaultValue={doc.access_level}
                      disabled={loading}
                      aria-label={`Access level for ${doc.filename}`}
                    >
                      {ACCESS_LEVELS.map((level) => (
                        <option key={level.value} value={level.value}>
                          {level.label}
                        </option>
                      ))}
                    </select>
                    <button
                      type="button"
                      className="btn-secondary"
                      onClick={() => handleAccessLevelSave(doc)}
                      disabled={loading}
                    >
                      {loading && updatingId === doc.id ? "Saving…" : "Save level"}
                    </button>
                    <button
                      type="button"
                      className="btn-secondary"
                      onClick={() => startUpdate(doc)}
                      disabled={loading}
                    >
                      {loading && updatingId === doc.id ? "Replacing…" : "Replace"}
                    </button>
                    <button
                      type="button"
                      className="btn-danger"
                      onClick={() => handleDelete(doc)}
                      disabled={loading}
                    >
                      Delete
                    </button>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
