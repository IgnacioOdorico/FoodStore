import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Este es el "corazón" del arranque del frontend.
// Busco el div con ID 'root' que está en el index.html y ahí "inyecto toda la App de React.
createRoot(document.getElementById('root')!).render(
  // El StrictMode es una herramienta que nos avisa si estamos usando algo viejo o mal en React.
  // Solo funciona en desarrollo, en producción no hace nada.
  <StrictMode>
    <App />
  </StrictMode>,
)
