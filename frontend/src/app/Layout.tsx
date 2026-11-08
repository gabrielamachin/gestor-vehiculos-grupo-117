import { Outlet } from 'react-router-dom'
import { Boton } from '../shared/componentes/Boton'
import { useAuth } from '../features/usuarios/useAuth'

export function Layout() {
  const { usuario, cerrarSesion } = useAuth()

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-3xl items-center justify-between gap-3 px-4 py-3">
          <span className="font-semibold text-brand">Gestor de Vehículos</span>
          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-slate-600 sm:inline">{usuario?.nombre}</span>
            <Boton type="button" variante="secundario" onClick={() => void cerrarSesion().catch(() => undefined)}>
              Salir
            </Boton>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
