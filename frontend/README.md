# ParkIndia Frontend

This is the frontend application for ParkIndia, built with Vue.js 3 and Vite.

## Project Setup

### Prerequisites
- Node.js 16 or higher
- npm or yarn package manager

### Installation

```sh
npm install
```

### Development

Start the development server with hot-reload:

```sh
npm run dev
```

The application will be available at `http://localhost:5173`

### Production Build

Compile and minify for production:

```sh
npm run build
```

### Preview Production Build

Preview the production build locally:

```sh
npm run preview
```

## Project Structure

- `src/App.vue` - Root component with navigation
- `src/main.js` - Application entry point
- `src/router/` - Vue Router configuration
- `src/views/` - Page-level components
- `src/components/` - Reusable UI components
- `src/assets/` - Static assets and styles

## Technologies

- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Bootstrap 5** - CSS framework
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **Vite** - Build tool and dev server

## Configuration

The frontend communicates with the backend API running on `http://localhost:5000`. Update the API base URL in components if needed.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).
