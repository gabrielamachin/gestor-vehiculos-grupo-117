import { createContext } from 'react'
import type { Usuario } from './tipos'

export interface AuthContextValor {
  /** Usuario con sesión iniciada, o null. */
  usuario: Usuario | null
  /** true mientras se averigua si hay una sesión activa al abrir la aplicación. */
  cargando: boolean
  iniciarSesion: (email: string, password: string) => Promise<void>
  registrarse: (nombre: string, email: string, password: string) => Promise<void>
  cerrarSesion: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValor | null>(null)
