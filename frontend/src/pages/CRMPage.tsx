const stages = ["New", "Contacted", "Qualified", "Closed"];
const leads = [{ id: 1, name: "Acme Co", stage: "New" }, { id: 2, name: "SolTech", stage: "Contacted" }];

export function CRMPage() {
  return <section><h1>CRM Pipeline</h1><p>Arrastra tarjetas entre columnas para actualizar estado.</p><div className="kanban">{stages.map((stage) => <div key={stage} className="column"><h3>{stage}</h3>{leads.filter((l) => l.stage === stage).map((l) => <div key={l.id} className="lead-card">{l.name}<small>Historial, llamadas y notas</small></div>)}</div>)}</div></section>;
}
