import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './app/App'
import { AuthProvider } from './features/usuarios/AuthProvider'
import { AvisosProvider } from './shared/mensajes/AvisosProvider'
import { ConfirmacionProvider } from './shared/mensajes/ConfirmacionProvider'

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
