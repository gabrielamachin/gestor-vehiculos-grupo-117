import { expect, test } from '@playwright/test'
import type { Page } from '@playwright/test'
import { conSesionDemo, tarjeta } from './ayudas'

/** Los datos de demo (scripts/cargar_datos_demo.py) están pensados para disparar cada indicador. */
async function abrirVehiculoDemo(page: Page, alias: string) {
  await conSesionDemo(page)
  await page.goto('/')
  await page.getByRole('link', { name: alias }).click()
  await expect(page.getByRole('heading', { name: alias })).toBeVisible()
}

test('Toyota Corolla: alerta de combustible y mantenimientos en tres estados', async ({ page }) => {
  await abrirVehiculoDemo(page, 'Toyota Corolla')

  await expect(tarjeta(page, 'Combustible vs. tu promedio')).toContainText('Gastaste más de lo habitual')

  const mantenimientos = tarjeta(page, 'Próximos mantenimientos')
  const fila = (nombre: string) => mantenimientos.getByRole('listitem').filter({ hasText: nombre })
  await expect(fila('Correa de distribución')).toContainText('Vencido')
  await expect(fila('Cambio de aceite')).toContainText('Próximo')
  await expect(fila('Filtros')).toContainText('Al día')
  await expect(fila('Frenos')).toContainText('Al día')
  // Lo más urgente primero
  await expect(mantenimientos.getByRole('listitem').first()).toContainText('Correa de distribución')

  await expect(tarjeta(page, '¿Reparar o reemplazar?')).toContainText('Seguir reparando parece razonable')
  await expect(tarjeta(page, 'Costo real por kilómetro')).toContainText('por km')
})

test('Ford Fiesta: orientación a considerar el reemplazo, con sus tres señales', async ({ page }) => {
  await abrirVehiculoDemo(page, 'Ford Fiesta')

  const orientacion = tarjeta(page, '¿Reparar o reemplazar?')
  await expect(orientacion).toContainText('Considerá evaluar un reemplazo')
  await expect(orientacion.getByRole('listitem')).toHaveCount(3)
  await expect(tarjeta(page, 'Combustible vs. tu promedio')).toContainText('Tu gasto está dentro de lo habitual')
})

test('Moto Honda: sin datos, cada indicador muestra su estado vacío', async ({ page }) => {
  await abrirVehiculoDemo(page, 'Moto Honda')

  await expect(tarjeta(page, 'Costo real por kilómetro')).toContainText('Cargá una lectura de kilometraje')
  await expect(tarjeta(page, 'Combustible vs. tu promedio')).toContainText('Todavía no cargaste gastos de combustible')
  await expect(tarjeta(page, 'Próximos mantenimientos')).toContainText('Todavía no definiste planes de mantenimiento')
  await expect(tarjeta(page, '¿Reparar o reemplazar?')).toContainText('Sin datos suficientes')
})
