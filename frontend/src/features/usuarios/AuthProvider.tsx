import { useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import { registrarManejadorSesionVencida } from '../../shared/api/cliente'
import {
  cerrarSesion as cerrarSesionEnApi,
  consultarSesion,
  iniciarSesion as iniciarSesionEnApi,
  registrar,
} from './api'
import { AuthContext } from './auth-context'
import type { AuthContextValor } from './auth-context'
import type { Usuario } from './tipos'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null)
  // El token vive en una cookie HttpOnly que el JavaScript no puede leer: la única forma de saber si
  // hay sesión es preguntarle a la API, así que al abrir la app siempre hay una verificación inicial.
  const [cargando, setCargando] = useState(true)

  // Una sesión vencida (401 en un endpoint protegido) solo limpia el estado local: la cookie ya no sirve.
  const limpiarSesion = useCallback(() => setUsuario(null), [])

  useEffect(() => {
    registrarManejadorSesionVencida(limpiarSesion)
    return () => registrarManejadorSesionVencida(null)
  }, [limpiarSesion])

  useEffect(() => {
    let cancelado = false
    consultarSesion()
      .then((perfil) => {
        if (!cancelado) setUsuario(perfil)
      })
      .catch(() => {
        /* sin sesión (401) o API no disponible: se queda en el login */
      })
      .finally(() => {
        if (!cancelado) setCargando(false)
      })
    return () => {
      cancelado = true
    }
  }, [])

  const iniciarSesion = useCallback(async (email: string, password: string) => {
    setUsuario(await iniciarSesionEnApi({ email, password }))
  }, [])

  const registrarse = useCallback(
    async (nombre: string, email: string, password: string) => {
      await registrar({ nombre, email, password })
      await iniciarSesion(email, password)
    },
    [iniciarSesion],
  )

  const cerrarSesion = useCallback(async () => {
    try {
      await cerrarSesionEnApi()
    } finally {
      setUsuario(null) // aunque falle la llamada, el usuario sale de la pantalla
    }
  }, [])

  const valor = useMemo<AuthContextValor>(
    () => ({ usuario, cargando, iniciarSesion, registrarse, cerrarSesion }),
    [usuario, cargando, iniciarSesion, registrarse, cerrarSesion],
  )

  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>
}
