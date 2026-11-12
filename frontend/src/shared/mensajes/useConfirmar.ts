import { useContext } from 'react'
import { ConfirmacionContext } from './confirmacion-context'
import type { Confirmar } from './confirmacion-context'

export function useConfirmar(): Confirmar {
  const confirmar = useContext(ConfirmacionContext)
  if (confirmar === null) throw new Error('useConfirmar debe usarse dentro de <ConfirmacionProvider>')
  return confirmar
}
