import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import '@fontsource-variable/lexend'
import './index.css'
import App from './app/App'
import { AuthProvider } from './features/usuarios/AuthProvider'
import { AvisosProvider } from './shared/mensajes/AvisosProvider'
import { ConfirmacionProvider } from './shared/mensajes/ConfirmacionProvider'
import { registerSW } from 'virtual:pwa-register'

const temaGuardado = localStorage.getItem('tema')
const usarModoOscuro =
  temaGuardado === 'oscuro' ||
  (temaGuardado === null && window.matchMedia('(prefers-color-scheme: dark)').matches)
document.documentElement.classList.toggle('dark', usarModoOscuro)

registerSW({ immediate: true })

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <AvisosProvider>
        <ConfirmacionProvider>
          <AuthProvider>
            <App />
          </AuthProvider>
        </ConfirmacionProvider>
      </AvisosProvider>
    </BrowserRouter>
  </StrictMode>,
)
