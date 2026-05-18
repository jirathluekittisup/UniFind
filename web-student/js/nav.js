function renderNav(active) {
  const user = getUser();
  const name = user?.display_name || user?.email || '';
  const pages = [
    ['browse.html', 'Browse'],
    ['report.html', 'Report'],
    ['profile.html', 'My Account'],
  ];
  const links = pages.map(([h, l]) =>
    `<a href="${h}" class="${active === h ? 'active' : ''}">${l}</a>`
  ).join('');
  document.body.insertAdjacentHTML('afterbegin', `
    <nav class="nav">
      <a href="browse.html" class="brand" style="color:var(--dark)">
        <span class="dot"></span>UniFind<span>Lost &amp; Found</span>
      </a>
      ${links}
      <div class="spacer"></div>
      <span class="muted" style="font-size:13px">${esc(name)}</span>
      <button class="logout" onclick="logout()">Logout</button>
    </nav>
  `);
}
