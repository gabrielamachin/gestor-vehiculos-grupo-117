import type { ReactNode } from 'react'

/** Contenedor centrado para las pantallas de login y registro. */
export function TarjetaAuth({ titulo, subtitulo, children }: { titulo: string; subtitulo: string; children: ReactNode }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-8">
      <div className="w-full max-w-sm">
        <p className="mb-6 text-center text-lg font-semibold text-brand">Gestor de Vehículos</p>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-xl font-semibold text-slate-900">{titulo}</h1>
          <p className="mb-5 mt-1 text-sm text-slate-500">{subtitulo}</p>
          {children}
        </div>
      </div>
    </div>
  )
}
