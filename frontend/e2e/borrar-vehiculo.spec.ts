import { expect, test } from '@playwright/test'
import { conSesion, crearGastoPorApi, crearVehiculoPorApi } from './ayudas'

test('un vehículo sin datos se elimina sin pedir confirmación escrita', async ({ page }) => {
  await conSesion(page)
  const id = await crearVehiculoPorApi(page, 'Vacío E2E', 0)
  await page.goto(`/vehiculos/${id}`)

  await page.getByRole('button', { name: 'Eliminar vehículo' }).click()
  const dialogo = page.getByRole('dialog')
  await expect(dialogo).toContainText('todavía no tiene gastos, lecturas ni planes')
  await expect(dialogo.getByRole('textbox')).toHaveCount(0)

  await dialogo.getByRole('button', { name: 'Eliminar vehículo' }).click()
  await expect(page.getByText('Vehículo eliminado')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Mis vehículos' })).toBeVisible()
  await expect(page.getByText('Vacío E2E')).toHaveCount(0)
})

test('un vehículo con datos informa qué se pierde y exige escribir el alias', async ({ page }) => {
  await conSesion(page)
  const id = await crearVehiculoPorApi(page, 'Con Datos E2E', 1000)
  await crearGastoPorApi(page, id, 'combustible', 1500)
  await page.goto(`/vehiculos/${id}`)

  await page.getByRole('button', { name: 'Eliminar vehículo' }).click()
  const dialogo = page.getByRole('dialog')
  await expect(dialogo).toContainText('Se eliminarán también 1 gasto, 0 lecturas de kilometraje y 0 planes de mantenimiento')

  const confirmar = dialogo.getByRole('button', { name: 'Eliminar vehículo' })
  await expect(confirmar).toBeDisabled()

  await dialogo.getByRole('textbox').fill('con datos')
  await expect(confirmar).toBeDisabled() // texto incompleto

  await dialogo.getByRole('textbox').fill('con datos e2e') // en minúsculas: no distingue mayúsculas
  await expect(confirmar).toBeEnabled()
  await confirmar.click()

  await expect(page.getByText('Vehículo eliminado')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Mis vehículos' })).toBeVisible()
  await expect(page.getByText('Con Datos E2E')).toHaveCount(0)
})

test('cancelar el diálogo (Esc o botón) no elimina el vehículo', async ({ page }) => {
  await conSesion(page)
  const id = await crearVehiculoPorApi(page, 'Sigue Existiendo E2E', 0)
  await page.goto(`/vehiculos/${id}`)
  const dialogo = page.getByRole('dialog')

  await page.getByRole('button', { name: 'Eliminar vehículo' }).click()
  await expect(dialogo).toBeVisible()
  await page.keyboard.press('Escape')
  await expect(dialogo).toBeHidden()

  await page.getByRole('button', { name: 'Eliminar vehículo' }).click()
  await dialogo.getByRole('button', { name: 'Cancelar' }).click()
  await expect(dialogo).toBeHidden()

  await expect(page.getByRole('heading', { name: 'Sigue Existiendo E2E' })).toBeVisible()
  expect((await page.request.get(`/api/vehiculos/${id}`)).status()).toBe(200)
})

test('eliminar un gasto pide confirmación y actualiza la lista', async ({ page }) => {
  await conSesion(page)
  const id = await crearVehiculoPorApi(page, 'Auto gastos E2E', 1000)
  await crearGastoPorApi(page, id, 'combustible', 2500)
  await page.goto(`/vehiculos/${id}`)

  await page.getByRole('button', { name: 'Eliminar', exact: true }).click()
  const dialogo = page.getByRole('dialog')
  await expect(dialogo).toContainText('¿Eliminar este gasto?')
  await dialogo.getByRole('button', { name: 'Eliminar', exact: true }).click()

  await expect(page.getByText('Gasto eliminado')).toBeVisible()
  await expect(page.getByText('Todavía no cargaste gastos para este vehículo.')).toBeVisible()
})
