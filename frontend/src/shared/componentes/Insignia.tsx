import type { ReactNode } from 'react'
import type { Tono } from './TarjetaIndicador'

const ESTILOS: Record<Tono, string> = {
  neutro: 'bg-slate-100 text-slate-700',
  ok: 'bg-emerald-100 text-emerald-800',
  alerta: 'bg-amber-100 text-amber-800',
  peligro: 'bg-red-100 text-red-800',
}

export function Insignia({ tono, children }: { tono: Tono; children: ReactNode }) {
  return <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${ESTILOS[tono]}`}>{children}</span>
}
