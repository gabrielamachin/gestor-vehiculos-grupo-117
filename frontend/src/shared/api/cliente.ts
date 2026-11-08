import { ApiError, mensajeDeRespuesta } from './errores'

/**
 * Prefijo de la API. Se consume desde el MISMO ORIGEN que el frontend: en desarrollo lo atiende el
 * proxy de Vite (vite.config.ts) y en producción una regla de reescritura de Render. Así la cookie de
 * sesión es "first-party" y no hace falta configurar CORS.
 */
const URL_BASE = String(import.meta.env.VITE_API_URL ?? '/api').replace(/\/$/, '')

let alSesionVencida: (() => void) | null = null

/** El AuthProvider registra acá qué hacer cuando la API responde 401 en un endpoint protegido (sesión vencida). */
export function registrarManejadorSesionVencida(manejador: (() => void) | null): void {
  alSesionVencida = manejador
}

type Parametros = Record<string, string | number | boolean | null | undefined>

interface Opciones {
  metodo?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  cuerpo?: unknown
  params?: Parametros
  /**
   * Por defecto, un 401 significa "la sesión venció" y se avisa al AuthProvider para volver al login.
   * Poner false en login, logout y en la consulta inicial de sesión, donde un 401 es una respuesta esperada.
   */
  expiraSesion?: boolean
}

async function leerJson(respuesta: Response): Promise<unknown> {
  try {
    return await respuesta.json()
  } catch {
    return null
  }
}

/**
 * Único punto de contacto con la API: serializa JSON y normaliza los errores en ApiError.
 * La autenticación viaja en una cookie HttpOnly que el navegador envía solo: este código nunca ve el token.
 */
export async function solicitar<T>(ruta: string, opciones: Opciones = {}): Promise<T> {
  const { metodo = 'GET', cuerpo, params, expiraSesion = true } = opciones

  const consulta = new URLSearchParams()
  for (const [clave, valor] of Object.entries(params ?? {})) {
    if (valor !== null && valor !== undefined) consulta.set(clave, String(valor))
  }
  const texto = consulta.toString()
  const url = URL_BASE + ruta + (texto ? `?${texto}` : '')

  const headers: Record<string, string> = { Accept: 'application/json' }
  if (cuerpo !== undefined) headers['Content-Type'] = 'application/json'

  let respuesta: Response
  try {
    respuesta = await fetch(url, {
      method: metodo,
      headers,
      // Solo envía la cookie a su mismo origen. Con una API en otro origen habría que usar 'include' y CORS con credenciales.
      credentials: 'same-origin',
      body: cuerpo !== undefined ? JSON.stringify(cuerpo) : undefined,
    })
  } catch {
    throw new ApiError(0, 'No se pudo conectar con el servidor. Revisá tu conexión e intentá de nuevo.')
  }

  if (respuesta.status === 401 && expiraSesion) alSesionVencida?.()
  if (!respuesta.ok) {
    throw new ApiError(respuesta.status, mensajeDeRespuesta(respuesta.status, await leerJson(respuesta)))
  }
  if (respuesta.status === 204) return undefined as T
  return (await respuesta.json()) as T
}
