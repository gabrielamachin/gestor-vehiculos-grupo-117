import { expect } from '@playwright/test'
import type { Locator, Page } from '@playwright/test'

export const PASSWORD = 'clave-segura-123'
/** Usuario creado por scripts/cargar_datos_demo.py (solo lectura: ninguna prueba debe modificarlo ni borrarlo). */
export const DEMO = { email: 'demo@gestor.com', password: 'demo1234' }

export interface UsuarioPrueba {
  nombre: string
  email: string
  password: string
}

/** Cada prueba usa su propio usuario: así no se pisan entre sí ni dependen del orden. */
export function usuarioNuevo(): UsuarioPrueba {
  const sufijo = `${Date.now()}-${Math.floor(Math.random() * 1_000_000)}`
  return { nombre: 'Usuaria Prueba', email: `e2e-${sufijo}@prueba.com`, password: PASSWORD }
}

/** Fecha de hoy "AAAA-MM-DD" en la zona horaria de las pruebas (la misma que usa el navegador: ver playwright.config.ts). */
export function hoyIso(): string {
  // El locale en-CA da el formato AAAA-MM-DD
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Argentina/Buenos_Aires' }).format(new Date())
}

/*
 * Las funciones siguientes usan la API a través del proxy del frontend (/api). `page.request` comparte las cookies
 * con el navegador: una sesión abierta acá queda abierta en la página, igual que si el usuario hubiera ingresado.
 */

export async function registrarPorApi(page: Page): Promise<UsuarioPrueba> {
  const usuario = usuarioNuevo()
  const respuesta = await page.request.post('/api/usuarios/registro', { data: usuario })
  expect(respuesta.status()).toBe(201)
  return usuario
}

export async function abrirSesionPorApi(page: Page, email: string, password: string): Promise<void> {
  const respuesta = await page.request.post('/api/usuarios/sesion', { data: { email, password } })
  expect(respuesta.status()).toBe(200)
}

/** Usuario nuevo con la sesión ya abierta en la página. */
export async function conSesion(page: Page): Promise<UsuarioPrueba> {
  const usuario = await registrarPorApi(page)
  await abrirSesionPorApi(page, usuario.email, usuario.password)
  return usuario
}

export async function conSesionDemo(page: Page): Promise<void> {
  await abrirSesionPorApi(page, DEMO.email, DEMO.password)
}

export async function crearVehiculoPorApi(page: Page, alias: string, kilometrajeInicial: number): Promise<string> {
  const respuesta = await page.request.post('/api/vehiculos', { data: { alias, kilometraje_inicial: kilometrajeInicial } })
  expect(respuesta.status()).toBe(201)
  return ((await respuesta.json()) as { id: string }).id
}

export async function idDeVehiculo(page: Page, alias: string): Promise<string> {
  const respuesta = await page.request.get('/api/vehiculos')
  const vehiculos = (await respuesta.json()) as { id: string; alias: string }[]
  const encontrado = vehiculos.find((v) => v.alias === alias)
  expect(encontrado, `no existe el vehículo "${alias}"`).toBeTruthy()
  return (encontrado as { id: string }).id
}

export async function crearGastoPorApi(page: Page, vehiculoId: string, codigoCategoria: string, monto: number): Promise<void> {
  const categorias = (await (await page.request.get('/api/categorias')).json()) as { id: number; codigo: string }[]
  const categoria = categorias.find((c) => c.codigo === codigoCategoria)
  expect(categoria, `no existe la categoría "${codigoCategoria}"`).toBeTruthy()
  const respuesta = await page.request.post('/api/gastos', {
    data: { vehiculo_id: vehiculoId, categoria_id: (categoria as { id: number }).id, monto, fecha: hoyIso() },
  })
  expect(respuesta.status()).toBe(201)
}

/** La tarjeta del dashboard (o sección) cuyo título es `titulo`: el contenedor directo del encabezado. */
export function tarjeta(page: Page, titulo: string): Locator {
  return page.getByRole('heading', { name: titulo }).locator('xpath=..')
}
