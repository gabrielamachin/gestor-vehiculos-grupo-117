import type { ButtonHTMLAttributes } from 'react'

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  cargando?: boolean
  variante?: 'primario' | 'secundario'
}

export function Boton({ cargando = false, variante = 'primario', disabled, className = '', children, ...resto }: Props) {
  const estilos =
    variante === 'primario'
      ? 'bg-brand text-white hover:bg-brand/90'
      : 'border border-slate-300 bg-white text-slate-700 hover:bg-slate-50'

  return (
    <button
      {...resto}
      disabled={disabled || cargando}
      className={`inline-flex min-h-11 items-center justify-center rounded-lg px-4 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-60 ${estilos} ${className}`}
    >
      {cargando ? 'Un momento…' : children}
    </button>
  )
}
