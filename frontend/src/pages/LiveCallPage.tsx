import { useEffect, useState } from "react";
import { apiRequest } from "../api";

export function LiveCallPage({ session }: { session: { token: string } | null }) {
  const [calls, setCalls] = useState<any[]>([]);
  const [message, setMessage] = useState("");
  const [integrationBlocked, setIntegrationBlocked] = useState(false);

  const load = () => session && apiRequest<any[]>("/calls", "GET", undefined, session.token).then(setCalls).catch((e) => setMessage(e.message));
  useEffect(load, [session]);

  async function createOutbound() {
    if (!session) return;
    try {
      await apiRequest("/calls/outbound", "POST", { script: "Llamada comercial" }, session.token);
      setMessage("Llamada saliente creada correctamente");
      setIntegrationBlocked(false);
      load();
    } catch (e) {
      const txt = e instanceof Error ? e.message : "Error";
      setMessage(txt);
      if (txt.includes("Twilio")) setIntegrationBlocked(true);
    }
  }

  return <section><h1>Llamadas</h1>
    <div className="card"><button className="btn" onClick={createOutbound} disabled={integrationBlocked}>Iniciar llamada saliente</button>{integrationBlocked && <p>Falta conectar esta cuenta con Twilio para activar llamadas salientes.</p>}{message && <p>{message}</p>}</div>
    <div className="grid">{calls.map((call) => <article key={call.id} className="card"><h3>#{call.id} · {call.direction}</h3><p>Estado: {call.status}</p><p>{call.transcript || "Sin transcripción"}</p></article>)}</div>
  </section>;
}
