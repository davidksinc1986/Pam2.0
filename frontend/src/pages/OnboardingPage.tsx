import { useEffect, useState } from "react";
import { apiRequest } from "../api";

export function OnboardingPage({ session }: { session: { token: string } | null }) {
  const [form, setForm] = useState({ onboarding_step: 1, ai_assistant_name: "PAM", ai_tone: "profesional", ai_behavior: "resolver rápido", playbook: "" });
  const [status, setStatus] = useState("");

  useEffect(() => {
    if (!session) return;
    apiRequest<any>("/companies/me", "GET", undefined, session.token).then((data) => setForm({ onboarding_step: data.onboarding_step, ai_assistant_name: data.ai_assistant_name, ai_tone: data.ai_tone, ai_behavior: data.ai_behavior, playbook: data.playbook })).catch((e) => setStatus(e.message));
  }, [session]);

  async function save() {
    if (!session) return;
    await apiRequest("/companies/me/onboarding", "PUT", form, session.token);
    setStatus("Configuración guardada y persistida");
  }

  return <section><h1>Configuración guiada</h1><div className="card"><label>Paso actual (1-4)<input type="number" min={1} max={4} value={form.onboarding_step} onChange={(e) => setForm({ ...form, onboarding_step: Number(e.target.value) })} /></label><label>Nombre del asistente<input value={form.ai_assistant_name} onChange={(e) => setForm({ ...form, ai_assistant_name: e.target.value })} /></label><label>Tono<input value={form.ai_tone} onChange={(e) => setForm({ ...form, ai_tone: e.target.value })} /></label><label>Comportamiento<textarea value={form.ai_behavior} onChange={(e) => setForm({ ...form, ai_behavior: e.target.value })} /></label><label>Guion base<textarea value={form.playbook} onChange={(e) => setForm({ ...form, playbook: e.target.value })} /></label><button className="btn" onClick={save}>Guardar configuración</button>{status && <p>{status}</p>}</div></section>;
}
