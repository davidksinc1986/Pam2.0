import { useEffect, useState } from "react";
import { apiRequest } from "../api";

export function CampaignBuilderPage({ session }: { session: { token: string } | null }) {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [form, setForm] = useState({ name: "", mode: "assisted", script: "", language: "es" });
  const [error, setError] = useState("");

  const load = async () => {
    if (!session) return;
    await apiRequest<any[]>("/campaigns", "GET", undefined, session.token).then(setCampaigns).catch((e) => setError(e.message));
  };
  useEffect(() => {
    void load();
  }, [session]);

  async function save() {
    if (!session) return;
    await apiRequest("/campaigns", "POST", form, session.token);
    setForm({ name: "", mode: "assisted", script: "", language: "es" });
    load();
  }

  return <section><h1>Creador de campañas</h1><div className="card"><label>Nombre de campaña <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label><label>Modo <select value={form.mode} onChange={(e) => setForm({ ...form, mode: e.target.value })}><option value="assisted">Agente asistido</option><option value="auto">IA automática</option></select></label><label>Guion inteligente<textarea value={form.script} onChange={(e) => setForm({ ...form, script: e.target.value })} /></label><button className="btn" onClick={save} disabled={!form.name}>Guardar campaña</button>{error && <p className="error">{error}</p>}</div><div className="grid">{campaigns.map((c) => <article key={c.id} className="card"><h3>{c.name}</h3><p>Modo: {c.mode}</p><p>Idioma: {c.language}</p></article>)}</div></section>;
}
