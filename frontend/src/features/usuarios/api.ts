import { solicitar } from '../../shared/api/cliente'
import type { Usuario } from './tipos'

export function registrar(datos: { nombre: string; email: string; password: string }): Promise<Usuario> {
  return solicitar<Usuario>('/usuarios/registro', { metodo: 'POST', cuerpo: datos, expiraSesion: false })
}

/** Inicia sesión: la API guarda el token en una cookie HttpOnly y devuelve solo los datos del usuario. */
export function iniciarSesion(datos: { email: string; password: string }): Promise<Usuario> {
  return solicitar<Usuario>('/usuarios/sesion', { metodo: 'POST', cuerpo: datos, expiraSesion: false })
}

/** Cierra la sesión: la API borra la cookie (el JavaScript no podría hacerlo: es HttpOnly). */
export function cerrarSesion(): Promise<void> {
  return solicitar<void>('/usuarios/sesion', { metodo: 'DELETE', expiraSesion: false })
}

/** ¿Hay una sesión activa? Un 401 es la respuesta normal de quien todavía no inició sesión. */
export function consultarSesion(): Promise<Usuario> {
  return solicitar<Usuario>('/usuarios/me', { expiraSesion: false })
}
