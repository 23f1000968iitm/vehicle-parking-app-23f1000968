const App = {
  data() {
    return {
      me: {},
      login: { email: '', password: '' },
      register: { name: '', email: '', password: '' },
      lotForm: { prime_location_name: '', address: '', pin_code: '', price: 50, number_of_spots: 10 },
      lots: [],
      history: [],
      error: '',
    };
  },
  async mounted() {
    await this.refreshMe();
    if (this.me.role === 'admin') await this.loadAdminLots();
    if (this.me.role === 'user') { await this.loadUserLots(); await this.loadHistory(); }
  },
  methods: {
    async refreshMe() { this.me = await api.me(); },
    async doLogin() {
      try { await api.login(this.login.email, this.login.password); this.error=''; await this.refreshMe(); if (this.me.role==='admin') await this.loadAdminLots(); else { await this.loadUserLots(); await this.loadHistory(); } }
      catch(e){ this.error = e.message; }
    },
    async logout(){ await api.logout(); location.reload(); },
    async doRegister(){ await api.register(this.register); alert('Registered! Now login.'); },
    async loadAdminLots(){ this.lots = await api.adminLots(); },
    async createLot(){ await api.createLot(this.lotForm); await this.loadAdminLots(); },
    async deleteLot(id){ if(confirm('Delete lot?')){ await api.deleteLot(id); await this.loadAdminLots(); } },
    async loadUserLots(){ this.lots = await api.userLots(); },
    async book(lot_id){ const r = await api.book(lot_id); alert('Booked spot '+r.spot_id); await this.loadUserLots(); await this.loadHistory(); },
    async release(res_id){ const r = await api.release(res_id); alert('Released, cost ₹'+r.cost); await this.loadUserLots(); await this.loadHistory(); },
    async loadHistory(){ this.history = await api.history(); },
    async exportCsv(){ const r = await api.exportCsv(); alert('Export started: '+r.task_id+' — file will appear in frontend/exports'); },
  }
};

Vue.createApp(App).mount('#app');



