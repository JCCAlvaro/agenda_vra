import { useEffect, useState } from 'react';
import { api } from '../api';

type Act = {
  id: string;
  titulo: string;
  descripcion: string;
  inicio: string;
  fin: string;
  lugar: string;
  prioridad: string;
  estado: string;
  origen: string;
};

const empty = {
  titulo: '',
  descripcion: '',
  inicio: '',
  fin: '',
  lugar: '',
  prioridad: 'media',
  origen: 'interna',
  recordatorio_min: 30,
};

export default function Activities() {
  const [list, setList] = useState<Act[]>([]);
  const [form, setForm] = useState<any>(empty);
  const [showForm, setShowForm] = useState(false);

  async function load() {
    try {
      setList(await api.get<Act[]>('/actividades'));
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function create(e: React.FormEvent) {
    e.preventDefault();
    try {
      const body = {
        ...form,
        inicio: new Date(form.inicio).toISOString(),
        fin: new Date(form.fin).toISOString(),
      };
      await api.post('/actividades', body);
      setShowForm(false);
      setForm(empty);
      load();
    } catch (e) {
      console.error(e);
    }
  }

  async function del(id: string) {
    if (!confirm('¿Eliminar actividad?')) return;
    await api.del(`/actividades/${id}`);
    load();
  }

  return (
    <div>
      <div className="toolbar">
        <h1>Actividades</h1>
        <button className="primary" onClick={() => setShowForm((v) => !v)}>
          {showForm ? 'Cancelar' : '+ Nueva actividad'}
        </button>
      </div>

      {showForm && (
        <form className="card form" onSubmit={create}>
          <label>Título *</label>
          <input
            value={form.titulo}
            onChange={(e) => setForm({ ...form, titulo: e.target.value })}
            required
          />
          <label>Descripción</label>
          <textarea
            value={form.descripcion}
            onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
          />
          <div className="row">
            <div>
              <label>Inicio *</label>
              <input
                type="datetime-local"
                value={form.inicio}
                onChange={(e) => setForm({ ...form, inicio: e.target.value })}
                required
              />
            </div>
            <div>
              <label>Fin *</label>
              <input
                type="datetime-local"
                value={form.fin}
                onChange={(e) => setForm({ ...form, fin: e.target.value })}
                required
              />
            </div>
          </div>
          <label>Lugar</label>
          <input
            value={form.lugar}
            onChange={(e) => setForm({ ...form, lugar: e.target.value })}
          />
          <div className="row">
            <div>
              <label>Prioridad</label>
              <select
                value={form.prioridad}
                onChange={(e) => setForm({ ...form, prioridad: e.target.value })}
              >
                <option value="alta">Alta</option>
                <option value="media">Media</option>
                <option value="baja">Baja</option>
              </select>
            </div>
            <div>
              <label>Recordatorio (min antes)</label>
              <input
                type="number"
                value={form.recordatorio_min}
                onChange={(e) =>
                  setForm({ ...form, recordatorio_min: +e.target.value })
                }
              />
            </div>
          </div>
          <button className="primary" type="submit">
            Guardar
          </button>
        </form>
      )}

      <div className="list">
        {list.map((a) => (
          <div key={a.id} className={`item prio-${a.prioridad}`}>
            <div>
              <div className="titulo">{a.titulo}</div>
              <div className="muted small">
                {new Date(a.inicio).toLocaleString('es-PE')} —{' '}
                {new Date(a.fin).toLocaleTimeString('es-PE')}
                {a.lugar && ` · ${a.lugar}`}
              </div>
            </div>
            <div className="actions">
              <span className={`badge ${a.prioridad}`}>{a.prioridad}</span>
              <span className="badge">{a.estado}</span>
              <button className="link danger" onClick={() => del(a.id)}>
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}