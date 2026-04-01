import { useEffect, useState } from "react";
import { apiRequest } from "../api";

export function DashboardPage({ session }: { session: { token: string } | null }) {
  const [data, setData] = useState<Record<string, number> | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!session) return;
    apiRequest<Record<string, number>>("/analytics/dashboard", "GET", undefined, session.token).then(setData).catch((e) => setError(e.message));
  }, [session]);

  if (error) return <p className="error">{error}</p>;
  if (!data) return <p>Cargando métricas reales...</p>;

  return <section>
    <h1>Panel general</h1>
    <div className="grid">
      <article className="card"><h3>Leads totales</h3><p>{data.leads_total}</p></article>
      <article className="card"><h3>Leads calificados</h3><p>{data.qualified_total}</p></article>
      <article className="card"><h3>Llamadas registradas</h3><p>{data.calls_total}</p></article>
      <article className="card"><h3>Campañas</h3><p>{data.campaigns_total}</p></article>
      <article className="card"><h3>Mensajes WhatsApp</h3><p>{data.whatsapp_messages}</p></article>
      <article className="card"><h3>Emails de seguimiento</h3><p>{data.email_followups}</p></article>
    </div>
  </section>;
}
