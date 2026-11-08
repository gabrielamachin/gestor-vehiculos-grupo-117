import type { ReactNode } from 'react'
import { formatoMes, formatoMoneda, formatoPorcentaje } from '../../shared/formato'
import { TarjetaIndicador } from '../../shared/componentes/TarjetaIndicador'
import type { Tono } from '../../shared/componentes/TarjetaIndicador'
import type { AlertaCombustible } from './tipos'

export function AlertaCombustibleTarjeta({ datos }: { datos: AlertaCombustible }) {
  let tono: Tono = 'neutro'
  let contenido: ReactNode

  const completo =
    datos.mes_evaluado !== null && datos.gasto_mes !== null && datos.promedio_historico !== null && datos.desvio_pct !== null

  if (datos.estado === 'sin_datos') {
    contenido = <p className="text-sm text-slate-500">Todavía no cargaste gastos de combustible.</p>
  } else if (datos.estado === 'historial_insuficiente') {
    contenido = (
      <p className="text-sm text-slate-500">
        Todavía no hay historial suficiente para comparar tu gasto (meses anteriores con cargas: {datos.meses_en_historial}).
        Seguí registrando tus cargas.
      </p>
    )
  } else if (completo) {
    const mes = formatoMes(datos.mes_evaluado as string)
    const desvio = datos.desvio_pct as number
    const alerta = datos.estado === 'alerta'
    tono = alerta ? 'alerta' : 'ok'
    contenido = (
      <>
        <p className="text-lg font-semibold text-slate-900">
          {alerta ? 'Gastaste más de lo habitual' : 'Tu gasto está dentro de lo habitual'}
        </p>
        <p className="mt-1 text-sm text-slate-700">
          En {mes} gastaste {formatoMoneda(datos.gasto_mes as number)} en combustible ({formatoPorcentaje(desvio, true)} respecto de tu
          promedio de {formatoMoneda(datos.promedio_historico as number)}).
        </p>
        <p className="mt-2 text-xs text-slate-500">
          Se avisa cuando supera al promedio en {formatoPorcentaje(datos.umbral_pct)} o más. Promedio de {datos.meses_en_historial} meses
          anteriores con cargas.
        </p>
      </>
    )
  } else {
    contenido = <p className="text-sm text-slate-500">No hay datos para mostrar.</p>
  }

  return (
    <TarjetaIndicador titulo="Combustible vs. tu promedio" tono={tono}>
      {contenido}
    </TarjetaIndicador>
  )
}
