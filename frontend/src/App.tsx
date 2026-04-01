import { Link, Route, Routes } from "react-router-dom";
import { HomePage } from "./pages/HomePage";
import { OnboardingPage } from "./pages/OnboardingPage";
import { DashboardPage } from "./pages/DashboardPage";
import { LiveCallPage } from "./pages/LiveCallPage";
import { CampaignBuilderPage } from "./pages/CampaignBuilderPage";
import { CRMPage } from "./pages/CRMPage";

export function App() {
  return (
    <div className="shell">
      <aside className="sidebar">
        <h2>PAM</h2>
        <Link to="/">Inicio</Link>
        <Link to="/onboarding">Configuración guiada</Link>
        <Link to="/dashboard">Panel</Link>
        <Link to="/live-call">Llamada en vivo</Link>
        <Link to="/campaigns">Campañas</Link>
        <Link to="/crm">CRM</Link>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/live-call" element={<LiveCallPage />} />
          <Route path="/campaigns" element={<CampaignBuilderPage />} />
          <Route path="/crm" element={<CRMPage />} />
        </Routes>
      </main>
    </div>
  );
}
