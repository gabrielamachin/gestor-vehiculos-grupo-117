export interface Categoria {
  id: number
  codigo: string
  nombre: string
  tipo_costo: 'fijo' | 'variable'
  activa: boolean
}
