import type { ReactNode } from 'react'

export type Tono = 'neutro' | 'ok' | 'alerta' | 'peligro'

const ESTILOS: Record<Tono, string> = {
  neutro: 'border-slate-200 bg-white',
  ok: 'border-emerald-200 bg-emerald-50',
  alerta: 'border-amber-300 bg-amber-50',
  peligro: 'border-red-300 bg-red-50',
}

export function TarjetaIndicador({ titulo, tono = 'neutro', children }: { titulo: string; tono?: Tono; children: ReactNode }) {
  return (
    <section className={`rounded-2xl border p-4 shadow-sm ${ESTILOS[tono]}`}>
      <h2 className="mb-3 text-base font-semibold text-slate-700">{titulo}</h2>
      {children}
    </section>
  )
}
