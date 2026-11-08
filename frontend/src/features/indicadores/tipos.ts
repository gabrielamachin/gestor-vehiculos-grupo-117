/** Reflejan las respuestas de /indicadores/vehiculos/{id}/... del backend. */

export interface CostoPorKm {
  estado: 'ok' | 'sin_lecturas' | 'sin_recorrido'
  costo_por_km: number | null
  km_recorridos: number | null
  total_gastado: number
}

export interface ItemCategoria {
  categoria_id: number
  codigo: string
  nombre: string
  tipo_costo: 'fijo' | 'variable'
  total: number
  cantidad: number
  porcentaje: number
}

export interface GastoPorCategoria {
  desde: string | null
  hasta: string | null
  total: number
  total_fijo: number
  total_variable: number
  categorias: ItemCategoria[]
}

export interface AlertaCombustible {
  estado: 'sin_datos' | 'historial_insuficiente' | 'normal' | 'alerta'
  mes_evaluado: string | null
  gasto_mes: number | null
  promedio_historico: number | null
  desvio_pct: number | null
  meses_en_historial: number
  umbral_pct: number
}

export interface ProximoMantenimiento {
  plan_id: string
  nombre: string
  intervalo_km: number
  ultimo_km: number | null
  proximo_km: number
  km_restantes: number | null
  estado: 'sin_lecturas' | 'al_dia' | 'proximo' | 'vencido'
  base: 'ultimo_mantenimiento' | 'multiplos'
}

export interface Senal {
  codigo: string
  descripcion: string
  cumplida: boolean
}

export interface Orientacion {
  estado: 'sin_datos' | 'reparar' | 'evaluar' | 'considerar_reemplazo'
  mensaje: string
  senales: Senal[]
  aviso: string
}

export interface Resumen {
  costo_por_km: CostoPorKm
  gasto_por_categoria: GastoPorCategoria
  alerta_combustible: AlertaCombustible
  proximos_mantenimientos: ProximoMantenimiento[]
  reparar_o_reemplazar: Orientacion
}
