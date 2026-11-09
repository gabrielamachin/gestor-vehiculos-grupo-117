/** Formatos de presentación (es-AR). Los montos son pesos argentinos. */

const formateadores = new Map<string, Intl.NumberFormat>()

function numero(valor: number, decimales: number): string {
  const clave = `n${decimales}`
  let formateador = formateadores.get(clave)
  if (formateador === undefined) {
    formateador = new Intl.NumberFormat('es-AR', { minimumFractionDigits: decimales, maximumFractionDigits: decimales })
    formateadores.set(clave, formateador)
  }
  return formateador.format(valor)
}

export function formatoMoneda(valor: number, decimales = 0): string {
  return `$ ${numero(valor, decimales)}`
}

export function formatoKm(valor: number): string {
  return `${numero(valor, 0)} km`
}

/** Porcentaje con un decimal. `conSigno` agrega "+" a los positivos (los negativos ya traen "-"). */
export function formatoPorcentaje(valor: number, conSigno = false): string {
  return `${conSigno && valor > 0 ? '+' : ''}${numero(valor, 1)} %`
}

/** "2024-04-01" -> "abril de 2024". Se arma con año y mes para evitar corrimientos por zona horaria. */
export function formatoMes(fechaIso: string): string {
  const [anio, mes] = fechaIso.split('-').map(Number)
  return new Date(anio, mes - 1, 1).toLocaleDateString('es-AR', { month: 'long', year: 'numeric' })
}

function dosDigitos(valor: number): string {
  return String(valor).padStart(2, '0')
}

/** Fecha de hoy en la zona horaria del usuario, como "AAAA-MM-DD" (el formato de <input type="date"> y de la API). */
export function fechaDeHoy(): string {
  const hoy = new Date()
  return `${hoy.getFullYear()}-${dosDigitos(hoy.getMonth() + 1)}-${dosDigitos(hoy.getDate())}`
}

/** "2024-03-15" -> "15/03/2024". */
export function formatoFecha(fechaIso: string): string {
  const [anio, mes, dia] = fechaIso.split('-')
  return `${dia}/${mes}/${anio}`
}
