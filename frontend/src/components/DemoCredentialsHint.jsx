import { useEffect, useId, useRef, useState } from "react";

export default function DemoCredentialsHint({ email, password, onUseDemo }) {
  const [open, setOpen] = useState(false);
  const panelId = useId();
  const rootRef = useRef(null);

  useEffect(() => {
    if (!open) return undefined;

    function handlePointerDown(event) {
      if (rootRef.current && !rootRef.current.contains(event.target)) {
        setOpen(false);
      }
    }

    function handleEscape(event) {
      if (event.key === "Escape") setOpen(false);
    }

    document.addEventListener("mousedown", handlePointerDown);
    document.addEventListener("keydown", handleEscape);
    return () => {
      document.removeEventListener("mousedown", handlePointerDown);
      document.removeEventListener("keydown", handleEscape);
    };
  }, [open]);

  return (
    <div className="demo-credentials" ref={rootRef}>
      <button
        type="button"
        className="demo-credentials-trigger"
        aria-label="Demo login credentials"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((value) => !value)}
        title="Demo login"
      >
        <span className="demo-credentials-label">Demo</span>
        <span className="demo-credentials-icon" aria-hidden>
          i
        </span>
      </button>
      {open && (
        <div className="demo-credentials-panel" id={panelId} role="dialog" aria-label="Demo credentials">
          <p className="demo-credentials-title">Try the demo (admin)</p>
          <dl className="demo-credentials-list">
            <div>
              <dt>Email</dt>
              <dd>{email}</dd>
            </div>
            <div>
              <dt>Password</dt>
              <dd>{password}</dd>
            </div>
          </dl>
          <button
            type="button"
            className="btn-secondary btn-full"
            onClick={() => {
              onUseDemo();
              setOpen(false);
            }}
          >
            Use demo account
          </button>
        </div>
      )}
    </div>
  );
}
