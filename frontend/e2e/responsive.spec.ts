import { expect, test } from '@playwright/test'
import type { Page, TestInfo } from '@playwright/test'
import { conSesionDemo, idDeVehiculo } from './ayudas'

// Un celular chico: con la fuente Lexend (más ancha que la del sistema) es donde algo podría desbordarse
test.use({ viewport: { width: 360, height: 740 } })

async function hayDesborde(page: Page): Promise<boolean> {
  return page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth)
}

/** Adjunta una captura de página completa al informe (npm run test:e2e:informe) para revisarla a ojo. */
async function adjuntarCaptura(page: Page, testInfo: TestInfo, nombre: string) {
  await testInfo.attach(nombre, { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' })
}

test.describe('a 360 px de ancho no hay desborde horizontal', () => {
  test('inicio', async ({ page }, testInfo) => {
    await conSesionDemo(page)
    await page.goto('/')
    await expect(page.getByRole('link', { name: 'Toyota Corolla' })).toBeVisible()
    await adjuntarCaptura(page, testInfo, 'inicio-360')
    expect(await hayDesborde(page)).toBe(false)
  })

  test('vehículo con el dashboard completo', async ({ page }, testInfo) => {
    await conSesionDemo(page)
    await page.goto(`/vehiculos/${await idDeVehiculo(page, 'Ford Fiesta')}`)
    await expect(page.getByRole('heading', { name: '¿Reparar o reemplazar?' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Planes de mantenimiento' })).toBeVisible()
    await adjuntarCaptura(page, testInfo, 'vehiculo-360')
    expect(await hayDesborde(page)).toBe(false)
  })

  test('vehículo con mantenimientos y alerta (el de más texto)', async ({ page }, testInfo) => {
    await conSesionDemo(page)
    await page.goto(`/vehiculos/${await idDeVehiculo(page, 'Toyota Corolla')}`)
    await expect(page.getByRole('heading', { name: 'Próximos mantenimientos' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Planes de mantenimiento' })).toBeVisible()
    await adjuntarCaptura(page, testInfo, 'corolla-360')
    expect(await hayDesborde(page)).toBe(false)
  })

  test('formulario de gasto', async ({ page }, testInfo) => {
    await conSesionDemo(page)
    await page.goto(`/vehiculos/${await idDeVehiculo(page, 'Toyota Corolla')}/gastos/nuevo`)
    await expect(page.getByRole('button', { name: 'Guardar gasto' })).toBeVisible()
    await adjuntarCaptura(page, testInfo, 'formulario-gasto-360')
    expect(await hayDesborde(page)).toBe(false)
  })
})
