function requireAdmin() {
  if (!getToken()) { location.href = 'index.html'; return null; }
  return api('/api/auth/me').then(u => {
    const user = u.user || u;
    if (user.role !== 'admin' && user.role !== 'super_admin') {
      setToken(null); location.href = 'index.html';
      throw new Error('Forbidden');
    }
    return user;
  }).catch(() => { setToken(null); location.href = 'index.html'; });
}

function logout() { setToken(null); location.href = 'index.html'; }

function renderShell(activePage, user) {
  const nav = [
    { id: 'dashboard', label: '📊 Overview', href: 'dashboard.html' },
    { id: 'items',     label: '📦 Items',    href: 'items.html' },
    { id: 'users',     label: '👥 Users',    href: 'users.html' },
    { id: 'claims',    label: '✅ Claims',   href: 'claims.html' },
  ].map(n => `<a href="${n.href}" class="${n.id === activePage ? 'active' : ''}">${n.label}</a>`).join('');

  document.getElementById('shell').innerHTML = `
    <aside class="sidebar">
      <div class="brand">
        <span class="logo-dot"></span>
        <h1>UniFind<span>Admin</span></h1>
      </div>
      <nav>${nav}</nav>
      <div class="spacer"></div>
      <div class="user">
        <div><strong>${user?.name || ''}</strong></div>
        <div>${user?.email || ''}</div>
        <button onclick="logout()">Log out</button>
      </div>
    </aside>
    <main class="main" id="main"></main>
  `;
}
