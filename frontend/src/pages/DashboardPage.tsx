import React, { useState } from "react";
import { Onboarding } from "../components/Onboarding";

export function DashboardPage() {
  const [campaignName, setCampaignName] = useState("Campaña Demo");

  return (
    <main style={{ fontFamily: "Inter, sans-serif", margin: "0 auto", maxWidth: 960, padding: 20 }}>
      <h1>PAM CallLeadCenter</h1>
      <p title="Panel principal de operación para agentes y supervisores">
        Dashboard unificado para llamadas, scripts guiados y captación de leads.
      </p>

      <label>
        Nombre de campaña:
        <input
          value={campaignName}
          onChange={(e) => setCampaignName(e.target.value)}
          style={{ marginLeft: 8 }}
        />
      </label>

      <Onboarding />

      <section style={{ marginTop: 20 }}>
        <h2>Tooltips rápidos</h2>
        <button title="Abre el panel para aceptar o transferir llamadas">Llamadas en vivo</button>
        <button title="Carga y ejecuta scripts guiados para el agente" style={{ marginLeft: 8 }}>
          Scripts
        </button>
        <button title="Visualiza leads de Facebook/Instagram" style={{ marginLeft: 8 }}>
          Leads
        </button>
      </section>
    </main>
  );
}
