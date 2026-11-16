import { expect, test } from '@playwright/test'
import { conSesion, crearVehiculoPorApi } from './ayudas'

test('un usuario no puede ver ni abrir el vehículo de otro', async ({ page, browser, baseURL }) => {
  await conSesion(page)
  const id = await crearVehiculoPorApi(page, 'Privado E2E', 1000)

  // Otro usuario, en un navegador distinto (cookies separadas)
  const contextoB = await browser.newContext({ baseURL })
  try {
    const paginaB = await contextoB.newPage()
    await conSesion(paginaB)

    await paginaB.goto(`/vehiculos/${id}`)
    await expect(paginaB.getByText('Vehículo no encontrado')).toBeVisible()

    await paginaB.goto('/')
    await expect(paginaB.getByText('Privado E2E')).toHaveCount(0)

    // Y la API responde lo mismo, sin revelar que el vehículo existe
    expect((await paginaB.request.get(`/api/vehiculos/${id}`)).status()).toBe(404)
    expect((await paginaB.request.get(`/api/gastos?vehiculo_id=${id}`)).status()).toBe(404)
  } finally {
    await contextoB.close()
  }
})
