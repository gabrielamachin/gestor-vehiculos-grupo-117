import { useContext } from 'react'
import { AvisosContext } from './avisos-context'
import type { Avisos } from './avisos-context'

export function useAvisos(): Avisos {
  const avisos = useContext(AvisosContext)
  if (avisos === null) throw new Error('useAvisos debe usarse dentro de <AvisosProvider>')
  return avisos
}
