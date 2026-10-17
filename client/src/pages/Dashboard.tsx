import { useEffect, useState } from 'react';
import { api } from '../api';

type Dash = {
  hoy: Record<string, number>;
  proximas: {
    id: string;
    titulo: string;
    inicio: string;
    prioridad: string;
    estado: string;
  }[];
  semana_total: number;
};

export default function Dashboard() {
  const [data, setData] = useState<Dash | null>(null);

  useEffect(() => {
    api.get<Dash>('/dashboard').then(setData).catch(console.error);
  }, []);

  if (!data) return <div>Cargando…</div>;
  const totalHoy = Object.values(data.hoy).reduce((a, b) => a + b, 0);

  return (
    <div>
      <h1>Dashboard</h1>
      <p className="muted">
        {new Date().toLocaleDateString('es-PE', {
          weekday: 'long',
          day: 'numeric',
          month: 'long',
          year: 'numeric',
        })}
      </p>

      <div className="cards">
        <div className="card">
          <div className="kpi">{totalHoy}</div>
          <div>Hoy</div>
        </div>
        <div className="card prio-alta">
          <div className="kpi">{data.hoy.alta || 0}</div>
          <div>Alta</div>
        </div>
        <div className="card prio-media">
          <div className="kpi">{data.hoy.media || 0}</div>
          <div>Media</div>
        </div>
        <div className="card prio-baja">
          <div className="kpi">{data.hoy.baja || 0}</div>
          <div>Baja</div>
        </div>
        <div className="card">
          <div className="kpi">{data.semana_total}</div>
          <div>Esta semana</div>
        </div>
      </div>

      <h2>Próximas actividades</h2>
      <div className="list">
        {data.proximas.length === 0 && (
          <div className="muted">Sin actividades próximas</div>
        )}
        {data.proximas.map((a) => (
          <div key={a.id} className={`item prio-${a.prioridad}`}>
            <div>
              <div className="titulo">{a.titulo}</div>
              <div className="muted small">
                {new Date(a.inicio).toLocaleString('es-PE')}
              </div>
            </div>
            <span className={`badge ${a.prioridad}`}>{a.prioridad}</span>
          </div>
        ))}
      </div>
    </div>
  );
}