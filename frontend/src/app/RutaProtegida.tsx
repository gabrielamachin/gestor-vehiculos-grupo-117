import { Navigate, Outlet } from 'react-router-dom'
import { Cargando } from '../shared/componentes/Cargando'
import { useAuth } from '../features/usuarios/useAuth'

/** Solo deja pasar a usuarios con sesión; el resto va al login. */
export function RutaProtegida() {
  const { usuario, cargando } = useAuth()
  if (cargando) return <Cargando mensaje="Conectando con el servidor…" />
  if (usuario === null) return <Navigate to="/login" replace />
  return <Outlet />
}
