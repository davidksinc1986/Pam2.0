import { useEffect, useState } from "react";
import { apiRequest } from "../api";

type UserRow = {
  id: number;
  email: string;
  preferred_language: string;
  is_active: boolean;
};

export function UsersPage({ session }: { session: { token: string } | null }) {
  const [users, setUsers] = useState<UserRow[]>([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ email: "", password: "", preferred_language: "es" });

  const load = async () => {
    if (!session) return;
    await apiRequest<UserRow[]>("/users", "GET", undefined, session.token).then(setUsers).catch((e) => setError(e.message));
  };
  useEffect(() => {
    void load();
  }, [session]);

  async function createUser() {
    if (!session) return;
    setError("");
    try {
      await apiRequest("/users", "POST", form, session.token);
      setForm({ email: "", password: "", preferred_language: "es" });
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo crear el usuario");
    }
  }

  async function toggleUser(row: UserRow) {
    if (!session) return;
    setError("");
    try {
      await apiRequest(`/users/${row.id}`, "PATCH", { is_active: !row.is_active }, session.token);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo actualizar el usuario");
    }
  }

  return <section>
    <h1>Usuarios de la empresa</h1>
    <div className="card">
      <h3>Crear usuario</h3>
      <label>Email<input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
      <label>Contraseña<input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
      <label>Idioma<select value={form.preferred_language} onChange={(e) => setForm({ ...form, preferred_language: e.target.value })}><option value="es">Español</option><option value="en">English</option><option value="pt">Português</option></select></label>
      <button className="btn" onClick={createUser} disabled={!form.email || form.password.length < 10}>Guardar usuario</button>
      {error && <p className="error">{error}</p>}
    </div>
    <div className="grid">
      {users.map((row) => <article key={row.id} className="card"><h3>{row.email}</h3><p>Idioma: {row.preferred_language}</p><p>Estado: {row.is_active ? "Activo" : "Desactivado"}</p><button className="btn-secondary" onClick={() => toggleUser(row)}>{row.is_active ? "Desactivar" : "Reactivar"}</button></article>)}
    </div>
  </section>;
}
