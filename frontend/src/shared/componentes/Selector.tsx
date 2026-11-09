import type { SelectHTMLAttributes } from 'react'

interface Props extends SelectHTMLAttributes<HTMLSelectElement> {
  etiqueta: string
  /** Se usa como id y name del select (y para asociar la etiqueta). */
  nombre: string
  ayuda?: string
}

export function Selector({ etiqueta, nombre, ayuda, className = '', children, ...resto }: Props) {
  return (
    <div className="space-y-1">
      <label htmlFor={nombre} className="block text-sm font-medium text-slate-700">
        {etiqueta}
      </label>
      <select
        id={nombre}
        name={nombre}
        {...resto}
        className={`block min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3 text-base text-slate-900 focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand/20 ${className}`}
      >
        {children}
      </select>
      {ayuda && <p className="text-xs text-slate-500">{ayuda}</p>}
    </div>
  )
}
