import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'

interface Props {
  volverA: string
  textoVolver: string
  titulo: string
  subtitulo?: string
  children: ReactNode
}

/** Estructura común de las pantallas con un formulario: enlace para volver, título y tarjeta. */
export function PaginaFormulario({ volverA, textoVolver, titulo, subtitulo, children }: Props) {
  return (
    <section className="mx-auto max-w-lg">
      <Link to={volverA} className="text-sm font-medium text-brand hover:underline">
        ← {textoVolver}
      </Link>
      <h1 className="mt-3 text-xl font-semibold">{titulo}</h1>
      {subtitulo && <p className="text-sm text-slate-500">{subtitulo}</p>}
      <div className="mt-5 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">{children}</div>
    </section>
  )
}
