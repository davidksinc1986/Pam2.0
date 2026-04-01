import { useEffect, useState } from "react";
import { apiRequest } from "../api";

export function LiveCallPage({ session }: { session: { token: string } | null }) {
  const [calls, setCalls] = useState<any[]>([]);
  const [message, setMessage] = useState("");
  const [integrationBlocked, setIntegrationBlocked] = useState(false);
  const [transferDestination, setTransferDestination] = useState("");

  const load = async () => {
    if (!session) return;
    await apiRequest<any[]>("/calls", "GET", undefined, session.token).then(setCalls).catch((e) => setMessage(e.message));
  };
  useEffect(() => {
    void load();
  }, [session]);

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

  async function transferCall(callId: number) {
    if (!session) return;
    setMessage("");
    try {
      await apiRequest(`/calls/${callId}/transfer`, "POST", { destination: transferDestination }, session.token);
      setMessage(`Llamada #${callId} transferida`);
      await load();
    } catch (e) {
      const txt = e instanceof Error ? e.message : "Error";
      setMessage(txt);
      if (txt.includes("Twilio")) setIntegrationBlocked(true);
    }
  }

  return <section><h1>Llamadas</h1>
    <div className="card"><button className="btn" onClick={createOutbound} disabled={integrationBlocked}>Iniciar llamada saliente</button>{integrationBlocked && <p>Falta conectar esta cuenta con Twilio para activar llamadas salientes.</p>}{message && <p>{message}</p>}</div>
    <div className="card">
      <label>Destino de transferencia<input value={transferDestination} onChange={(e) => setTransferDestination(e.target.value)} placeholder="+15551234567" /></label>
      <small>Necesitas Twilio conectado para transferir.</small>
    </div>
    <div className="grid">{calls.map((call) => <article key={call.id} className="card"><h3>#{call.id} · {call.direction}</h3><p>Estado: {call.status}</p><p>{call.transcript || "Sin transcripción"}</p><button className="btn-secondary" disabled={!transferDestination} onClick={() => transferCall(call.id)}>Transferir</button></article>)}</div>
  </section>;
}
