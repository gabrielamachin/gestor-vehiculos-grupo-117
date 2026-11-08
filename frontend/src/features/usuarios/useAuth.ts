import { useContext } from 'react'
import { AuthContext } from './auth-context'
import type { AuthContextValor } from './auth-context'

export function useAuth(): AuthContextValor {
  const contexto = useContext(AuthContext)
  if (contexto === null) throw new Error('useAuth debe usarse dentro de <AuthProvider>')
  return contexto
}
