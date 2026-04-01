import { Link, Navigate, Route, Routes } from "react-router-dom";
import { useMemo, useState } from "react";
import { HomePage } from "./pages/HomePage";
import { OnboardingPage } from "./pages/OnboardingPage";
import { DashboardPage } from "./pages/DashboardPage";
import { LiveCallPage } from "./pages/LiveCallPage";
import { CampaignBuilderPage } from "./pages/CampaignBuilderPage";
import { CRMPage } from "./pages/CRMPage";
import { UsersPage } from "./pages/UsersPage";
import { apiRequest } from "./api";

type Session = { token: string; email: string; tenant_id: number };

function LoginPage({ onLogin }: { onLogin: (s: Session) => void }) {
  const [email, setEmail] = useState("davidksinc@gmail.com");
  const [password, setPassword] = useState("PamAdmin123!");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit() {
    setLoading(true);
    setError("");
    try {
      const data = await apiRequest<{ access_token: string; user: { email: string; tenant_id: number } }>("/auth/login", "POST", { email, password });
      const nextSession = { token: data.access_token, email: data.user.email, tenant_id: data.user.tenant_id };
      localStorage.setItem("pam_session", JSON.stringify(nextSession));
      onLogin(nextSession);
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo iniciar sesión");
    } finally {
      setLoading(false);
    }
  }

  return <section><h1>Login</h1><div className="card"><label>Email<input value={email} onChange={(e) => setEmail(e.target.value)} /></label><label>Contraseña<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>{error && <p className="error">{error}</p>}<button className="btn" onClick={submit} disabled={loading}>{loading ? "Entrando..." : "Entrar"}</button></div></section>;
}

function Protected({ session, children }: { session: Session | null; children: JSX.Element }) {
  if (!session) return <Navigate to="/login" replace />;
  return children;
}

export function App() {
  const [session, setSession] = useState<Session | null>(() => {
    const raw = localStorage.getItem("pam_session");
    return raw ? JSON.parse(raw) as Session : null;
  });

  const links = useMemo(() => ([
    ["/", "Inicio"], ["/onboarding", "Configuración guiada"], ["/dashboard", "Panel"], ["/live-call", "Llamadas"], ["/campaigns", "Campañas"], ["/crm", "CRM"], ["/users", "Usuarios"],
  ]), []);

  return (
    <div className="shell">
      <aside className="sidebar">
        <h2>PAM</h2>
        {session ? <>
          <small>{session.email}</small>
          {links.map(([to, label]) => <Link key={to} to={to}>{label}</Link>)}
          <button className="btn-secondary" onClick={() => { localStorage.removeItem("pam_session"); setSession(null); }}>Salir</button>
        </> : <Link to="/login">Login</Link>}
      </aside>
      <main className="content">
        <Routes>
          <Route path="/login" element={<LoginPage onLogin={setSession} />} />
          <Route path="/" element={<Protected session={session}><HomePage /></Protected>} />
          <Route path="/onboarding" element={<Protected session={session}><OnboardingPage session={session} /></Protected>} />
          <Route path="/dashboard" element={<Protected session={session}><DashboardPage session={session} /></Protected>} />
          <Route path="/live-call" element={<Protected session={session}><LiveCallPage session={session} /></Protected>} />
          <Route path="/campaigns" element={<Protected session={session}><CampaignBuilderPage session={session} /></Protected>} />
          <Route path="/crm" element={<Protected session={session}><CRMPage session={session} /></Protected>} />
          <Route path="/users" element={<Protected session={session}><UsersPage session={session} /></Protected>} />
        </Routes>
      </main>
    </div>
  );
}
