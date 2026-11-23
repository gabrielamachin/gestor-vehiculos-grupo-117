import { useEffect, useState } from 'react'
import { Link, Outlet } from 'react-router-dom'
import { Boton } from '../shared/componentes/Boton'
import { useAuth } from '../features/usuarios/useAuth'
import { IconoLuna, IconoSol } from '../shared/componentes/Iconos'

export function Layout() {
  const { usuario, cerrarSesion } = useAuth()
  const [modoOscuro, setModoOscuro] = useState(() =>
    localStorage.getItem('tema') === 'oscuro' ||
    (!localStorage.getItem('tema') && window.matchMedia('(prefers-color-scheme: dark)').matches),
  )

  useEffect(() => {
    document.documentElement.classList.toggle('dark', modoOscuro)
    localStorage.setItem('tema', modoOscuro ? 'oscuro' : 'claro')
  }, [modoOscuro])

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      <header className="border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
        <div className="mx-auto flex max-w-3xl items-center justify-between gap-3 px-4 py-3 lg:max-w-5xl">
          <Link to="/" className="font-semibold text-brand">
            Gestor de Vehículos
          </Link>
          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-slate-600 sm:inline">{usuario?.nombre}</span>
            <button
              type="button"
              onClick={() => setModoOscuro((actual) => !actual)}
              className="inline-flex h-11 w-11 items-center justify-center rounded-lg border border-slate-300 text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
              aria-label={modoOscuro ? 'Activar modo claro' : 'Activar modo oscuro'}
              title={modoOscuro ? 'Modo claro' : 'Modo oscuro'}
            >
              {modoOscuro ? <IconoSol /> : <IconoLuna />}
            </button>
            <Boton type="button" variante="secundario" onClick={() => void cerrarSesion().catch(() => undefined)}>
              Salir
            </Boton>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-4 py-6 lg:max-w-5xl">
        <Outlet />
      </main>
    </div>
  )
}
