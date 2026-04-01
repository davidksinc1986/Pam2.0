import { useEffect, useState } from "react";
import { apiRequest } from "../api";

const stages = ["New", "Contacted", "Qualified", "Closed"];

export function CRMPage({ session }: { session: { token: string } | null }) {
  const [leads, setLeads] = useState<any[]>([]);
  const [form, setForm] = useState({ name: "", contact: "" });
  const [error, setError] = useState("");

  const load = async () => {
    if (!session) return;
    await apiRequest<any[]>("/leads", "GET", undefined, session.token).then(setLeads).catch((e) => setError(e.message));
  };
  useEffect(() => {
    void load();
  }, [session]);

  async function createLead() {
    if (!session) return;
    await apiRequest("/leads", "POST", { ...form, source: "manual" }, session.token);
    setForm({ name: "", contact: "" });
    load();
  }

  async function moveLead(id: number, stage: string) {
    if (!session) return;
    await apiRequest(`/leads/${id}/stage`, "PATCH", { stage }, session.token);
    load();
  }

  return <section><h1>CRM Pipeline</h1>
    <div className="card"><h3>Nuevo lead</h3><label>Nombre<input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label><label>Contacto<input value={form.contact} onChange={(e) => setForm({ ...form, contact: e.target.value })} /></label><button className="btn" onClick={createLead} disabled={!form.name || !form.contact}>Guardar lead</button></div>
    {error && <p className="error">{error}</p>}
    <div className="kanban">{stages.map((stage) => <div key={stage} className="column"><h3>{stage}</h3>{leads.filter((l) => l.stage === stage).map((l) => <div key={l.id} className="lead-card">{l.name}<small>{l.contact}</small><select value={l.stage} onChange={(e) => moveLead(l.id, e.target.value)}>{stages.map((s) => <option key={s}>{s}</option>)}</select></div>)}</div>)}</div>
  </section>;
}
