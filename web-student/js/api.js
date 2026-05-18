const API_BASE = window.API_BASE || 'http://localhost:5001';

function getToken() { return localStorage.getItem('unifind_token'); }
function setToken(t) { t ? localStorage.setItem('unifind_token', t) : localStorage.removeItem('unifind_token'); }
function getUser() { try { return JSON.parse(localStorage.getItem('unifind_user') || 'null'); } catch { return null; } }
function setUser(u) { u ? localStorage.setItem('unifind_user', JSON.stringify(u)) : localStorage.removeItem('unifind_user'); }

async function api(path, method = 'GET', body = null) {
  const headers = {};
  if (!(body instanceof FormData)) headers['Content-Type'] = 'application/json';
  const t = getToken();
  if (t) headers.Authorization = `Bearer ${t}`;
  const res = await fetch(API_BASE + path, {
    method,
    headers,
    body: body ? (body instanceof FormData ? body : JSON.stringify(body)) : null,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

function requireAuth() {
  if (!getToken()) { location.href = 'index.html'; return false; }
  return true;
}

function logout() {
  setToken(null); setUser(null); location.href = 'index.html';
}

function fmtDate(s) {
  if (!s) return '';
  const d = new Date(s);
  return isNaN(d) ? s : d.toLocaleDateString();
}

function resolvePhotoUrl(url) {
  if (!url) return '';
  if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:') || url.startsWith('blob:')) return url;
  if (url.startsWith('/')) return API_BASE.replace(/\/$/, '') + url;
  return url;
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
