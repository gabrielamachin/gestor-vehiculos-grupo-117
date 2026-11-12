import { createContext } from 'react'

export interface Avisos {
  /** Aviso verde que se cierra solo (p. ej. "Gasto guardado"). */
  exito: (texto: string) => void
  /** Aviso rojo que se cierra solo. Los errores de un formulario se siguen mostrando en el propio formulario. */
  error: (texto: string) => void
}

export const AvisosContext = createContext<Avisos | null>(null)
