export function CampaignBuilderPage() {
  return <section><h1>Creador de campañas</h1><div className="card"><label>Nombre de campaña <input defaultValue="Renovaciones Abril"/></label><label>Modo <select><option>Agente asistido</option><option>IA automática</option></select></label><label>Guion inteligente<textarea defaultValue="Hola {{nombre}}, te llamo de..."/></label><button className="btn">Lanzar campaña</button></div></section>;
}
