import { Link } from "react-router-dom";

export function HomePage() {
  return <section><h1>PAM AI Contact Center</h1><p>Tu recepcionista con IA, campañas de llamadas, captación de contactos y CRM en una sola app para tu empresa.</p><ul><li>Atiende llamadas entrantes automáticamente.</li><li>Lanza campañas salientes con IA o con apoyo para equipo humano.</li><li>Organiza oportunidades en un pipeline visual.</li></ul><Link className="btn" to="/onboarding">Start Setup</Link></section>;
}
