import { NavLink, Outlet } from "react-router-dom";

function NavIcon({ name }) {
  const paths = {
    chat: (
      <path
        d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"
        stroke="currentColor"
        strokeWidth="1.75"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    ),
    documents: (
      <>
        <path
          d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
          stroke="currentColor"
          strokeWidth="1.75"
          fill="none"
        />
        <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" stroke="currentColor" strokeWidth="1.75" fill="none" />
      </>
    ),
    team: (
      <>
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="1.75" fill="none" />
        <circle cx="9" cy="7" r="4" stroke="currentColor" strokeWidth="1.75" fill="none" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" stroke="currentColor" strokeWidth="1.75" fill="none" />
      </>
    ),
    analytics: (
      <>
        <path d="M18 20V10M12 20V4M6 20v-6" stroke="currentColor" strokeWidth="1.75" fill="none" strokeLinecap="round" />
      </>
    ),
  };

  return (
    <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">
      {paths[name]}
    </svg>
  );
}

export default function AppShell({ userEmail, userRole, onLogout }) {
  const isAdmin = userRole === "admin";
  const canViewAnalytics = userRole === "admin" || userRole === "manager";

  const navItems = [
    { to: "/chat", label: "Assistant", icon: "chat", show: true },
    { to: "/documents", label: isAdmin ? "Documents" : "Library", icon: "documents", show: true },
    { to: "/team", label: "Team", icon: "team", show: isAdmin },
    { to: "/analytics", label: "Analytics", icon: "analytics", show: canViewAnalytics },
  ].filter((item) => item.show);

  const initials = userEmail
    ? userEmail
        .split("@")[0]
        .split(/[._-]/)
        .map((part) => part[0])
        .join("")
        .slice(0, 2)
        .toUpperCase()
    : "?";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-mark" aria-hidden="true">
            EK
          </div>
          <div>
            <strong>Knowledge</strong>
            <span>Assistant</span>
          </div>
        </div>

        <nav className="sidebar-nav" aria-label="Main">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}
            >
              <NavIcon name={item.icon} />
              <span className="nav-label">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-card">
            <div className="user-avatar">{initials}</div>
            <div className="user-meta">
              <span className="user-email">{userEmail}</span>
              <span className="role-pill">{userRole}</span>
            </div>
          </div>
          <button type="button" className="btn-ghost sidebar-signout" onClick={onLogout}>
            Sign out
          </button>
        </div>
      </aside>

      <div className="app-main">
        <Outlet />
      </div>
    </div>
  );
}
