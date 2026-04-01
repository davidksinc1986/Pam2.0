import React from "react";

const steps = [
  "1) Crea una campaña y conecta tu número de Twilio.",
  "2) Sube tu script de call-calling en el módulo Scripts.",
  "3) Activa la captura de leads de Facebook/Instagram.",
  "4) Monitorea llamadas y leads en tiempo real desde el dashboard.",
];

export function Onboarding() {
  return (
    <section style={{ border: "1px solid #ccc", padding: 16, borderRadius: 10 }}>
      <h2>Onboarding paso a paso</h2>
      <ul>
        {steps.map((step) => (
          <li key={step} title="Sigue este paso para completar tu configuración inicial">
            {step}
          </li>
        ))}
      </ul>
    </section>
  );
}
