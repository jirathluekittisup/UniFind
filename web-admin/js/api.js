const API_BASE = window.API_BASE || 'http://localhost:5001';

function getToken() { return localStorage.getItem('unifind_admin_token'); }
function setToken(t) { t ? localStorage.setItem('unifind_admin_token', t) : localStorage.removeItem('unifind_admin_token'); }

async function api(path, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' };
  const t = getToken();
  if (t) headers.Authorization = `Bearer ${t}`;
  const res = await fetch(API_BASE + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}
