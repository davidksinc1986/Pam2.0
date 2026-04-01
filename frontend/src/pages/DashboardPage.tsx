import { useMemo, useState } from "react";

const labels: Record<string, { title: string; analytics: string; automations: string }> = {
  es: { title: "Panel general", analytics: "Analítica en tiempo real", automations: "Automatizaciones" },
  en: { title: "Overview", analytics: "Realtime analytics", automations: "Automations" },
  pt: { title: "Painel geral", analytics: "Análises em tempo real", automations: "Automações" }
};

export function DashboardPage() {
  const [lang, setLang] = useState("es");
  const text = useMemo(() => labels[lang] ?? labels.es, [lang]);

  return <section>
    <h1>{text.title}</h1>
    <label>Idioma <select value={lang} onChange={(e) => setLang(e.target.value)}><option value="es">Español</option><option value="en">English</option><option value="pt">Português</option></select></label>
    <h3>{text.analytics}</h3>
    <div className="grid"><article className="card"><h3>Llamadas activas</h3><p>4</p></article><article className="card"><h3>Contactos nuevos</h3><p>18 hoy</p></article><article className="card"><h3>Campañas</h3><p>3 en ejecución</p></article><article className="card"><h3>Score promedio</h3><p>67/100</p></article></div>
    <h3>{text.automations}</h3>
    <div className="grid"><article className="card"><h3>WhatsApp</h3><p>12 mensajes enviados</p></article><article className="card"><h3>Email follow-up</h3><p>9 correos enviados</p></article></div>
  </section>;
}
