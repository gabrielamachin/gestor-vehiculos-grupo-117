import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'

interface Props {
  to: string
  variante?: 'primario' | 'secundario'
  className?: string
  children: ReactNode
}

/** Enlace con la misma apariencia que <Boton>. */
export function BotonEnlace({ to, variante = 'primario', className = '', children }: Props) {
  const estilos =
    variante === 'primario'
      ? 'bg-brand text-white hover:bg-brand/90'
      : 'border border-slate-300 bg-white text-slate-700 hover:bg-slate-50'

  return (
    <Link
      to={to}
      className={`inline-flex min-h-11 items-center justify-center rounded-lg px-4 text-sm font-medium transition ${estilos} ${className}`}
    >
      {children}
    </Link>
  )
}
