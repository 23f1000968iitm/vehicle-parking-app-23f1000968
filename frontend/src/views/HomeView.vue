<template>
  <div class="bg-white">
    <!-- Navigation Header -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container">
        <router-link class="navbar-brand d-flex align-items-center text-decoration-none" to="/">
          <span class="bg-white text-primary rounded d-flex align-items-center justify-content-center me-2 fw-bold fs-4" 
                style="width: 2rem; height: 2rem;">P</span>
          ParkIndia
        </router-link>
        
        <div class="navbar-nav ms-auto">
          <router-link class="nav-link" to="/login">
            <i class="fas fa-sign-in-alt me-1"></i>
            Login
          </router-link>
          <router-link class="nav-link" to="/register">
            <i class="fas fa-user-plus me-1"></i>
            Register
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section bg-white py-5" style="padding-top: 120px;">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8 text-center">
            <h1 class="display-4 fw-bold text-dark mb-4">Welcome to ParkIndia!</h1>
            <p class="fs-5 text-dark mb-4">
              A comprehensive parking management platform designed to simplify parking operations and improve customer satisfaction.
            </p>
            <p class="fs-6 text-muted mb-4">
              Get started today to experience intelligent parking solutions, live status updates, and detailed performance insights.
            </p>
            <div class="d-flex gap-3 justify-content-center flex-wrap">
              <router-link to="/register" class="btn btn-primary btn-lg px-4">
                Get Started
              </router-link>
              <router-link to="/login" class="btn btn-outline-secondary btn-lg px-4">
                Login
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-5 bg-light">
      <div class="container">
        <div class="row g-4">
          <div class="col-lg-4 col-md-6">
            <div class="card h-100 border-0 shadow-sm feature-card">
              <div class="card-body text-center p-4">
                <div class="bg-primary bg-opacity-10 rounded-3 d-inline-flex p-3 mb-3">
                  <i class="fas fa-chart-line text-primary fs-2"></i>
                </div>
                <h5 class="fw-bold mb-3">Live Status Tracking</h5>
                <p class="text-muted">
                  Monitor parking spot availability instantly with continuous updates and real-time alerts for smooth operations.
                </p>
              </div>
            </div>
          </div>

          <div class="col-lg-4 col-md-6">
            <div class="card h-100 border-0 shadow-sm feature-card">
              <div class="card-body text-center p-4">
                <div class="bg-success bg-opacity-10 rounded-3 d-inline-flex p-3 mb-3">
                  <i class="fas fa-chart-bar text-success fs-2"></i>
                </div>
                <h5 class="fw-bold mb-3">Advanced Analytics</h5>
                <p class="text-muted">
                  Discover usage trends, identify busy periods, and explore revenue enhancement strategies through comprehensive data analysis.
                </p>
              </div>
            </div>
          </div>

          <div class="col-lg-4 col-md-6">
            <div class="card h-100 border-0 shadow-sm feature-card">
              <div class="card-body text-center p-4">
                <div class="bg-info bg-opacity-10 rounded-3 d-inline-flex p-3 mb-3">
                  <i class="fas fa-mobile-alt text-info fs-2"></i>
                </div>
                <h5 class="fw-bold mb-3">Cross-Platform Support</h5>
                <p class="text-muted">
                  Use the parking management system on any device through our responsive web interface and mobile applications.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-5 bg-white">
      <div class="container">
        <div class="row g-4 text-center">
          <div class="col-lg-3 col-md-6">
            <div class="h2 text-primary fw-bold">10,000+</div>
            <p class="text-muted mb-0">Parking Spots Managed</p>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="h2 text-primary fw-bold">500+</div>
            <p class="text-muted mb-0">Active Locations</p>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="h2 text-primary fw-bold">99.9%</div>
            <p class="text-muted mb-0">System Uptime</p>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="h2 text-primary fw-bold">24/7</div>
            <p class="text-muted mb-0">Customer Support</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-5 bg-dark text-white">
      <div class="container text-center">
        <h2 class="display-5 fw-bold mb-3">Ready to Enhance Your Parking Operations?</h2>
        <p class="fs-5 mb-4 opacity-75">
          Join numerous organizations that rely on ParkIndia for their parking management requirements.
        </p>
        <router-link to="/register" class="btn btn-primary btn-lg px-5">
          Start Free Trial
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4">
      <div class="container text-center">
        <p class="mb-0">© 2025 ParkIndia | All rights reserved | Made with ❤️ for smart parking</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
/* Simple hover effects for cards */
.feature-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

/* Hero section spacing */
.hero-section {
  min-height: 60vh;
  display: flex;
  align-items: center;
}

/* Navbar brand styling */
.navbar-brand {
  font-weight: 700;
  color: #0d6efd;
}
</style>