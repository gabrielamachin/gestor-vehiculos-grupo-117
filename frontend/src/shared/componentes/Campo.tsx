import type { InputHTMLAttributes } from 'react'

interface Props extends InputHTMLAttributes<HTMLInputElement> {
  etiqueta: string
  /** Se usa como id y name del input (y para asociar la etiqueta). */
  nombre: string
  ayuda?: string
}

export function Campo({ etiqueta, nombre, ayuda, className = '', ...resto }: Props) {
  return (
    <div className="space-y-1">
      <label htmlFor={nombre} className="block text-sm font-medium text-slate-700">
        {etiqueta}
      </label>
      {/* text-base (16 px) evita el zoom automático de iOS al enfocar el campo */}
      <input
        id={nombre}
        name={nombre}
        {...resto}
        className={`block min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3 text-base text-slate-900 placeholder:text-slate-400 focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand/20 ${className}`}
      />
      {ayuda && <p className="text-xs text-slate-500">{ayuda}</p>}
    </div>
  )
}
