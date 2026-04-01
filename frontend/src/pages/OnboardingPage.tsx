const steps = [
  ["Configurar número", "Conecta tu cuenta de telefonía y elige el número principal. Ejemplo: +1 415..."],
  ["Personalizar IA", "Elige nombre (PAM), tono (cercano) e idioma (español)."],
  ["Subir guion", "Pega tu guion comercial con objeciones y respuestas frecuentes."],
  ["Activar sistema", "Haz una llamada de prueba y activa el modo en vivo."]
];

export function OnboardingPage() {
  return <section><h1>Configuración guiada</h1><p>Te acompañamos paso a paso con lenguaje simple. Todo tiene valores recomendados.</p>{steps.map((s) => <div key={s[0]} className="card" title="Tip: usa los ejemplos para configurar más rápido"><h3>{s[0]}</h3><p>{s[1]}</p><button className="btn-secondary">Usar valor recomendado</button></div>)}</section>;
}
