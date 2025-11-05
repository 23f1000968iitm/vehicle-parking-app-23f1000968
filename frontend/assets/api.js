const api = {
  async request(path, opts = {}) {
    const res = await fetch(`/api${path}`, {
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      ...opts,
    });
    if (!res.ok) throw new Error((await res.json()).error || res.statusText);
    return res.json();
  },
  me() { return this.request('/auth/me', { method: 'GET' }); },
  login(email, password) { return this.request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }); },
  logout() { return this.request('/auth/logout', { method: 'POST' }); },
  register(payload) { return this.request('/auth/register', { method: 'POST', body: JSON.stringify(payload) }); },
  adminLots() { return this.request('/admin/lots', { method: 'GET' }); },
  createLot(payload) { return this.request('/admin/lots', { method: 'POST', body: JSON.stringify(payload) }); },
  deleteLot(id) { return this.request(`/admin/lots/${id}`, { method: 'DELETE' }); },
  userLots() { return this.request('/user/lots', { method: 'GET' }); },
  book(lot_id) { return this.request('/user/book', { method: 'POST', body: JSON.stringify({ lot_id }) }); },
  release(reservation_id) { return this.request('/user/release', { method: 'POST', body: JSON.stringify({ reservation_id }) }); },
  history() { return this.request('/user/history', { method: 'GET' }); },
  exportCsv() { return this.request('/user/export', { method: 'POST' }); },
};

window.api = api;



