import { useState } from "react";
import { inviteUser } from "../api/auth.js";
import { INVITE_ROLES } from "../constants.js";

export default function TeamPage({ error, setError, loading, setLoading }) {
  const [inviteForm, setInviteForm] = useState({ email: "", role: "employee" });
  const [inviteSuccess, setInviteSuccess] = useState(null);

  async function handleInvite(e) {
    e.preventDefault();
    setError("");
    setInviteSuccess(null);
    setLoading(true);
    try {
      const data = await inviteUser({
        email: inviteForm.email,
        role: inviteForm.role,
      });
      setInviteSuccess(data);
      setInviteForm({ email: "", role: "employee" });
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
    <div className="page-view">
      <header className="page-header">
        <div>
          <h1>Team</h1>
          <p>Invite colleagues to your organization workspace.</p>
        </div>
      </header>

      <div className="page-grid">
        <section className="panel">
          <h2>Invite a member</h2>
          <p className="panel-desc">
            Send an invite code so they can register and access documents based on their role.
          </p>
          <form className="form-stack" onSubmit={handleInvite}>
            <label>
              Email address
              <input
                type="email"
                required
                placeholder="colleague@company.com"
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
                {INVITE_ROLES.map((role) => (
                  <option key={role.value} value={role.value}>
                    {role.label}
                  </option>
                ))}
              </select>
            </label>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? "Creating invite…" : "Create invite"}
            </button>
          </form>
        </section>

        <section className="panel panel-muted">
          <h2>How invites work</h2>
          <ul className="feature-list">
            <li>Share the one-time invite code with your teammate.</li>
            <li>They sign up using <strong>Invite code</strong> on the registration screen.</li>
            <li>Roles control which documents they can search and which admin tools they see.</li>
          </ul>
        </section>
      </div>

      {inviteSuccess && (
        <div className="toast success">
          <div>
            <strong>Invite created for {inviteSuccess.email}</strong>
            <p>Share this code with them to complete registration.</p>
          </div>
          <div className="invite-code-row">
            <code>{inviteSuccess.token}</code>
            <button type="button" className="btn-secondary" onClick={copyInviteCode}>
              Copy code
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
