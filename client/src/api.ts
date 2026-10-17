const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8080/api';

export const getToken = () => localStorage.getItem('token');
export const setToken = (t: string) => localStorage.setItem('token', t);
export const clearToken = () => localStorage.removeItem('token');

async function req<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(init.headers as any),
  };
  const t = getToken();
  if (t) headers['Authorization'] = `Bearer ${t}`;

  const r = await fetch(BASE + path, { ...init, headers });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export const api = {
  get: <T>(p: string) => req<T>(p),
  post: <T>(p: string, body: any) =>
    req<T>(p, { method: 'POST', body: JSON.stringify(body) }),
  put: <T>(p: string, body: any) =>
    req<T>(p, { method: 'PUT', body: JSON.stringify(body) }),
  del: <T>(p: string) => req<T>(p, { method: 'DELETE' }),
};