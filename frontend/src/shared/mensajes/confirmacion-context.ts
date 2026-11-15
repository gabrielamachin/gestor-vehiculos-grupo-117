import { createContext } from 'react'

export interface OpcionesConfirmacion {
  titulo: string
  mensaje: string
  /** Texto del botón de confirmación (por defecto "Confirmar"). */
  textoConfirmar?: string
  /** true para acciones destructivas: el botón de confirmación se muestra en rojo. */
  peligro?: boolean
}

/** Muestra el diálogo y devuelve true si el usuario confirma, false si cancela, cierra o presiona Esc. */
export type Confirmar = (opciones: OpcionesConfirmacion) => Promise<boolean>

export const ConfirmacionContext = createContext<Confirmar | null>(null)
