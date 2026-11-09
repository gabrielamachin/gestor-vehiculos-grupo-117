import { solicitar } from '../../shared/api/cliente'
import type { Categoria } from './tipos'

/** Incluye las inactivas: los gastos históricos pueden pertenecer a una categoría que ya no se ofrece. */
export function listarCategorias(): Promise<Categoria[]> {
  return solicitar<Categoria[]>('/categorias', { params: { incluir_inactivas: true } })
}
