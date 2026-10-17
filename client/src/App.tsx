import { useEffect, useState } from 'react';
import { api, clearToken, getToken } from './api';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Calendar from './pages/Calendar';
import Activities from './pages/Activities';

type User = { id: string; nombre: string; email: string; rol: string };
type Page = 'dashboard' | 'calendar' | 'activities';

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState<Page>('dashboard');

  useEffect(() => {
    if (!getToken()) {
      setLoading(false);
      return;
    }
    api
      .get<User>('/me')
      .then(setUser)
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="splash">Cargando…</div>;
  if (!user) return <Login onLogin={setUser} />;

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">UNAP</div>
          <div>
            <strong>Vicerrectorado</strong>
            <br />
            <small>Académico</small>
          </div>
        </div>
        <nav>
          <button
            className={page === 'dashboard' ? 'active' : ''}
            onClick={() => setPage('dashboard')}
          >
            📊 Dashboard
          </button>
          <button
            className={page === 'calendar' ? 'active' : ''}
            onClick={() => setPage('calendar')}
          >
            📅 Calendario
          </button>
          <button
            className={page === 'activities' ? 'active' : ''}
            onClick={() => setPage('activities')}
          >
            📋 Actividades
          </button>
        </nav>
        <div className="user-box">
          <div>{user.nombre}</div>
          <div className="muted small">{user.rol}</div>
          <button
            className="link"
            onClick={() => {
              clearToken();
              setUser(null);
            }}
          >
            Cerrar sesión
          </button>
        </div>
      </aside>
      <main className="content">
        {page === 'dashboard' && <Dashboard />}
        {page === 'calendar' && <Calendar />}
        {page === 'activities' && <Activities />}
      </main>
    </div>
  );
}