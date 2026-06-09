import { useEffect, useState } from "react";
import { listRecentQueries } from "../api/analytics.js";

function formatLatency(ms) {
  if (ms == null) return "—";
  if (ms < 1000) return `${ms} ms`;
  return `${(ms / 1000).toFixed(1)} s`;
}

export default function AnalyticsPage() {
  const [queryLogs, setQueryLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    listRecentQueries({ limit: 25 })
      .then((data) => setQueryLogs(data.items ?? []))
      .catch(() => setQueryLogs([]))
      .finally(() => setLoading(false));
  }, []);

  const avgLatency =
    queryLogs.length > 0
      ? Math.round(
          queryLogs.reduce((sum, log) => sum + (log.latency_ms || 0), 0) / queryLogs.length
        )
      : 0;

  return (
    <div className="page-view">
      <header className="page-header">
        <div>
          <h1>Analytics</h1>
          <p>Recent assistant activity across your organization.</p>
        </div>
      </header>

      <div className="stat-row">
        <div className="stat-card">
          <span className="stat-label">Queries logged</span>
          <strong className="stat-value">{queryLogs.length}</strong>
        </div>
        <div className="stat-card">
          <span className="stat-label">Avg. response time</span>
          <strong className="stat-value">{formatLatency(avgLatency)}</strong>
        </div>
      </div>

      <section className="panel">
        <h2>Recent questions</h2>
        {loading ? (
          <p className="panel-desc">Loading activity…</p>
        ) : queryLogs.length === 0 ? (
          <div className="empty-state compact">
            <h3>No activity yet</h3>
            <p>Questions will appear here once your team starts using the assistant.</p>
          </div>
        ) : (
          <ul className="activity-list">
            {queryLogs.map((log) => (
              <li key={log.id} className="activity-item">
                <div className="activity-question">{log.question}</div>
                <div className="activity-meta">
                  <span>{formatLatency(log.latency_ms)}</span>
                  <span>{log.retrieved_chunk_ids?.length ?? 0} sources</span>
                  <span>{new Date(log.created_at).toLocaleString()}</span>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
