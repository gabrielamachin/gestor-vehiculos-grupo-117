import { expect, test } from '@playwright/test'
import { registrarPorApi, usuarioNuevo } from './ayudas'

test('registro: crea la cuenta, entra, la sesión sobrevive a recargar y se puede cerrar', async ({ page }) => {
  const usuario = usuarioNuevo()

  await page.goto('/registro')
  await page.getByLabel('Nombre').fill(usuario.nombre)
  await page.getByLabel('Email').fill(usuario.email)
  await page.getByLabel('Contraseña', { exact: true }).fill(usuario.password)
  await page.getByLabel('Repetir contraseña').fill(usuario.password)
  await page.getByRole('button', { name: 'Crear cuenta' }).click()

  const titulo = page.getByRole('heading', { name: 'Mis vehículos' })
  await expect(titulo).toBeVisible()

  // La sesión vive en una cookie HttpOnly: recargar debe seguir dentro
  await page.reload()
  await expect(titulo).toBeVisible()

  await page.getByRole('button', { name: 'Salir' }).click()
  await expect(page.getByRole('heading', { name: 'Iniciar sesión' })).toBeVisible()
})

test('login: una contraseña incorrecta muestra el error y la correcta permite entrar', async ({ page }) => {
  const usuario = await registrarPorApi(page) // registrada, pero sin sesión abierta

  await page.goto('/login')
  await page.getByLabel('Email').fill(usuario.email)
  await page.getByLabel('Contraseña').fill('otra-clave-123')
  await page.getByRole('button', { name: 'Ingresar' }).click()
  await expect(page.getByRole('alert')).toContainText('Credenciales inválidas')
  await expect(page).toHaveURL(/\/login$/)

  await page.getByLabel('Contraseña').fill(usuario.password)
  await page.getByRole('button', { name: 'Ingresar' }).click()
  await expect(page.getByRole('heading', { name: 'Mis vehículos' })).toBeVisible()
})

test('una pantalla protegida sin sesión redirige al login', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveURL(/\/login$/)
})
