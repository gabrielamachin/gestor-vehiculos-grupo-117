import { expect, test } from '@playwright/test'
import { conSesion, crearVehiculoPorApi, hoyIso, tarjeta } from './ayudas'

test('flujo completo: vehículo, kilometraje y gasto hasta ver el costo real por km', async ({ page }) => {
  await conSesion(page)
  await page.goto('/')

  // Alta del vehículo
  await page.getByRole('link', { name: '+ Agregar' }).click()
  await page.getByLabel('Alias').fill('Auto E2E')
  await page.getByLabel('Kilometraje actual').fill('1000')
  await page.getByRole('button', { name: 'Guardar vehículo' }).click()
  await expect(page.getByText('Vehículo agregado')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Auto E2E' })).toBeVisible()

  // Lectura de kilometraje: 6.000 km (5.000 recorridos desde el inicial)
  await page.getByRole('link', { name: '+ Cargar kilometraje' }).click()
  await page.getByLabel('Kilometraje actual del odómetro').fill('6000')
  await page.getByRole('button', { name: 'Guardar lectura' }).click()
  await expect(page.getByText('Lectura guardada')).toBeVisible()
  await expect(page.getByText('6.000 km', { exact: true })).toBeVisible()
  await expect(page.getByText('Actual', { exact: true })).toBeVisible()

  // Gasto de $5.000 -> $1 por km
  await page.getByRole('link', { name: '+ Cargar gasto' }).click()
  await page.getByLabel('Categoría').selectOption({ label: 'Combustible' })
  await page.getByLabel('Monto ($)').fill('5000')
  await page.getByRole('button', { name: 'Guardar gasto' }).click()
  await expect(page.getByText('Gasto guardado')).toBeVisible()

  const costo = tarjeta(page, 'Costo real por kilómetro')
  await expect(costo).toContainText('$ 1,00')
  await expect(costo).toContainText('$ 5.000')
  await expect(costo).toContainText('5.000 km')
})

test('el formulario de gasto valida monto, fecha y kilometraje antes de enviar', async ({ page }) => {
  await conSesion(page)
  const id = await crearVehiculoPorApi(page, 'Auto validaciones', 1000)
  await page.goto(`/vehiculos/${id}/gastos/nuevo`)

  const guardar = page.getByRole('button', { name: 'Guardar gasto' })
  const error = page.getByRole('alert')

  await guardar.click()
  await expect(error).toContainText('Elegí una categoría.')

  await page.getByLabel('Categoría').selectOption({ label: 'Combustible' })
  await page.getByLabel('Monto ($)').fill('10.123') // tres decimales
  await guardar.click()
  await expect(error).toContainText('Ingresá un monto mayor a cero, con hasta 2 decimales.')

  await page.getByLabel('Monto ($)').fill('100')
  await page.getByLabel('Fecha', { exact: true }).fill('2999-01-01')
  await guardar.click()
  await expect(error).toContainText('La fecha no puede ser futura.')

  await page.getByLabel('Fecha', { exact: true }).fill(hoyIso())
  await page.getByLabel('Kilometraje (opcional)').fill('500') // menor al inicial (1.000)
  await guardar.click()
  await expect(error).toContainText('El kilometraje no puede ser menor al inicial del vehículo (1.000 km).')
})
