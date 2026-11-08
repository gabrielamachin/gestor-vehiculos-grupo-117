import { Navigate, Outlet } from 'react-router-dom'
import { Cargando } from '../shared/componentes/Cargando'
import { useAuth } from '../features/usuarios/useAuth'

/** Pantallas de login y registro: si ya hay sesión, redirige a la pantalla principal. */
export function RutaPublica() {
  const { usuario, cargando } = useAuth()
  if (cargando) return <Cargando mensaje="Conectando con el servidor…" />
  if (usuario !== null) return <Navigate to="/" replace />
  return <Outlet />
}
