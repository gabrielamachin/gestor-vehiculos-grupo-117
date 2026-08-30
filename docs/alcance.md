# Alcance del Proyecto — Gestor Inteligente de Vehículo

---

## Parte 1 — Problemática

### 1. Contexto del caso

El proyecto se plantea como un caso simulado en el marco del TPI. El escenario corresponde a una persona dueña de uno o varios vehículos particulares que necesita gestionar la información relacionada con su uso y mantenimiento (combustible, mantenimiento, reparaciones y otros gastos).

No se contempla una organización compleja ni actores externos (talleres, aseguradoras, concesionarias): el caso se acota deliberadamente a la gestión individual de vehículo(s) por parte de su propietario.

### 2. Situación actual

Actualmente, la información relacionada con el vehículo se gestiona de manera dispersa. El usuario recurre a una combinación de memoria, comprobantes en papel, notas del celular y aplicaciones o entidades bancarias. Algunas aplicaciones pueden registrar automáticamente ciertos gastos (por ejemplo, combustible), pero no existe un lugar único donde se concentre toda la información del vehículo.

Como consecuencia, resulta difícil:

- Conocer cuánto se gastó realmente en combustible durante un período.
- Conocer cuánto se gastó en mantenimiento y reparaciones.
- Diferenciar y relacionar los gastos fijos con los gastos variables.
- Determinar cuánto cuesta realmente mantener el vehículo en total.
- Calcular cuánto cuesta el vehículo en relación con los kilómetros recorridos.
- Recordar con precisión cuándo se realizó un mantenimiento y cuánto costó.
- Saber cuándo corresponde realizar el próximo mantenimiento.
- Identificar y cuantificar aumentos en los gastos a partir del historial.
- Contar con información histórica suficiente para analizar la evolución de los costos del vehículo.

El problema no es la ausencia total de datos, sino que estos datos están dispersos y resulta difícil transformarlos en información útil para analizar la situación del vehículo.

Hoy, esa información se utiliza principalmente de manera puntual —cuando surge una necesidad concreta, como realizar un mantenimiento, pagar combustible o afrontar una reparación— y no a partir de un historial integrado del vehículo.

### 3. Actores y necesidades

| | |
|---|---|
| **Actor** | Usuario propietario de uno o varios vehículos |
| **Rol** | Registra y consulta la información de sus vehículos, y utiliza los datos para analizar sus gastos y tomar decisiones. |

No se contemplan roles adicionales (administradores, talleres, aseguradoras) en esta primera versión.

**Necesidades principales:**
- Centralizar en un único lugar la información relacionada con sus vehículos.
- Registrar combustible, mantenimiento, reparaciones y otros gastos.
- Conocer el costo real de mantener y utilizar cada vehículo.
- Analizar los gastos a lo largo del tiempo.
- Detectar aumentos o comportamientos fuera de su propio promedio histórico.
- Recordar mantenimientos realizados y conocer los próximos mantenimientos estimados.
- Contar con información que lo ayude a evaluar decisiones relacionadas con el vehículo, como continuar reparando o considerar reemplazarlo.
- Si posee más de un vehículo, gestionar la información de cada uno de forma independiente.

**Limitaciones a contemplar:**
- El usuario no necesariamente posee conocimientos técnicos.
- La información depende de los datos que el propio usuario registre.
- No se contará con información automática proveniente del vehículo, bancos, estaciones de servicio u otros servicios externos.
- Los datos históricos pueden ser incompletos, especialmente al comenzar a usar el sistema.
- La calidad de los análisis y recomendaciones depende de la cantidad y precisión de los datos ingresados por el usuario.

### 4. Impacto

*Nota: por tratarse de un caso simulado, el impacto se plantea de forma cualitativa, como análisis del equipo. Para la evidencia externa que respalda o matiza este planteo, ver la sección 6 (Validación del problema).*

**Impacto principal:** la dificultad para obtener una visión integral e histórica del costo real del vehículo, lo que limita la capacidad del usuario para analizar sus gastos, planificarlos y tomar decisiones informadas.

**Caso particular — decisión de reparar o reemplazar:** cuando aparece una reparación importante o los costos de mantenimiento comienzan a aumentar, el usuario puede tener que decidir si continúa invirtiendo en el vehículo o considera reemplazarlo. Sin un historial consolidado de gastos y de la evolución de los costos, esta decisión suele tomarse a partir de percepciones o información parcial (no se encontró evidencia externa específica sobre cómo los propietarios llegan a esta decisión en la práctica; ver sección 6).

### 5. Enunciado del problema

> El dueño particular de uno o varios vehículos, que gestiona su información y sus gastos de forma dispersa (memoria, comprobantes en papel, notas del celular, aplicaciones bancarias), enfrenta el problema de no contar con una visión integral e histórica del costo real de mantener su vehículo. Esto le dificulta detectar aumentos de gastos, diferenciar gastos fijos de variables, anticipar próximos mantenimientos y tomar decisiones informadas —como continuar reparando o considerar reemplazar el vehículo— a partir de información parcial.
>
> Un sistema de gestión inteligente de vehículos podría centralizar esta información y transformarla en indicadores (costo real por km, gasto acumulado por categoría, comparación con el propio historial, estimación de próximos mantenimientos, orientación sobre reparar o reemplazar), a partir de los datos que el propio usuario registra.

### 6. Validación del problema

- **¿El problema está ocurriendo actualmente o es hipotético?** El proyecto aborda una problemática habitual en la gestión cotidiana de un vehículo particular: la dificultad para centralizar, comprender y utilizar la información relacionada con sus gastos, mantenimiento y evolución de costos. Es un caso de uso simulado en el marco del TPI, y la evidencia reunida a continuación respalda que se trata de una situación real y frecuente.

- **¿Los afectados reconocen el problema como tal?** Los componentes centrales de la problemática están respaldados por investigaciones externas:

  **Evidencia internacional:**
  - Una encuesta de Synchrony (EE. UU., 2025) encontró que los propietarios subestiman significativamente cuánto gastan realmente en sus vehículos, con una diferencia promedio del 167% entre el gasto estimado (USD 2.738) y el gasto real (USD 7.303) anual — respalda directamente el núcleo del problema: el desconocimiento del costo real del vehículo.
  - Un análisis publicado en *Nature* por Andor, Gerster, Gillingham y Horvath (2020), que compara el gasto autoestimado con una referencia externa objetiva del club automotor alemán ADAC, encontró subestimaciones superiores al 50% en Alemania y Suiza y evidenció que la mayoría de los compradores no había calculado previamente el costo de uso de su vehículo — confirma que la dificultad para dimensionar el gasto total es un patrón consistente entre mercados, no un caso aislado.
  - Distintas encuestas de EE. UU. (Utire, FinanceBuzz y CarMD) identifican que una proporción alta de propietarios posterga el mantenimiento y no recuerda datos básicos del vehículo (fecha del último service, kilometraje) — respalda la dificultad de seguimiento histórico que la propuesta busca resolver.

  **Evidencia contextual (Argentina):** existe cobertura periodística local que describe el mismo patrón: la combinación de gastos fijos y gastos espaciados en el tiempo (cubiertas, reparaciones puntuales) hace que muchos conductores sientan que el auto les cuesta más de lo que tenían anotado, porque esos gastos no entran en el cálculo hasta que ocurren — confirma que el patrón central también se observa en el contexto local.

  En conjunto, esta evidencia respalda los componentes centrales de la problemática: el desconocimiento del gasto real, la dificultad de seguimiento histórico y la falta de una visión integral del costo del vehículo. Los aspectos más puntuales —como la forma exacta en que cada usuario gestiona hoy su información, o el proceso específico de decisión entre reparar y reemplazar— se toman como supuestos de diseño consistentes con esta evidencia.

- **¿Existe alguna solución parcial actualmente? ¿Por qué no es suficiente?** Sí. Existen soluciones digitales orientadas al registro de determinados gastos del vehículo, como combustible o mantenimiento, pero no integran todas las categorías de información ni las transforman en una visión unificada de la evolución de los costos. El análisis detallado de estas alternativas se desarrolla en el análisis de competencia y diferenciación (`docs/viabilidad.md`, Integrante 3).

**En síntesis:** la evidencia reunida fundamenta la problemática planteada y justifica la propuesta de centralizar la información del vehículo y transformarla en indicadores que faciliten su análisis y la toma de decisiones.

---

## Parte 2 — Alcance

### 7. Propuesta de solución y valor diferencial

La propuesta no busca simplemente digitalizar el registro de gastos —eso ya es posible hoy con notas, planillas o apps de un solo rubro—, sino centralizar la información del vehículo y convertirla en indicadores que faciliten su análisis: costo real, evolución del gasto, comparación contra el propio historial y estimaciones que ayuden a anticipar decisiones (mantenimiento, reparación o reemplazo).

Frente a las soluciones parciales existentes (sección 6), el diferencial no es registrar más datos, sino cruzarlos: convertir cargas dispersas en indicadores comparables a lo largo del tiempo. Este enfoque se sostiene únicamente con datos que el propio usuario ingresa, sin depender de integraciones externas — lo que permite entregar ese valor de forma simple y confiable dentro de los plazos del TPI, en lugar de perseguir una integración de datos más completa pero técnicamente más riesgosa. El valor agregado no está en la tecnología en sí, sino en lo que permite hacer con datos que hoy existen pero están dispersos y sin relacionar entre sí.

### 8. Alcance del producto

Las funcionalidades de esta sección responden directamente a las necesidades identificadas en la sección 3 (Actores y necesidades).

**Criterio de corte del MVP:** una funcionalidad entra en esta primera versión si (a) puede resolverse únicamente con datos que el propio usuario carga, sin depender de integraciones con servicios externos (bancos, talleres, aseguradoras, APIs del vehículo), y (b) se resuelve con cálculos o heurísticas simples sobre esos datos, no con modelos predictivos ni tasaciones. Todo lo que requiere una fuente de datos externa, infraestructura adicional o un nivel de análisis más complejo que un cálculo directo queda fuera de esta versión.

#### 8.1 Incluido en esta primera versión (MVP)
- Gestión de uno o varios vehículos por usuario.
- Registro de combustible.
- Registro de mantenimiento.
- Registro de reparaciones y otros gastos.
- Cálculo del costo real por kilómetro.
- Visualización del gasto acumulado por categoría.
- Comparación del gasto de combustible con el promedio histórico propio.
- Estimación del próximo mantenimiento según kilometraje, a partir de un intervalo (ej. "cada 10.000 km") y el kilometraje actual, ambos cargados por el usuario. No se contemplan reglas específicas por marca o modelo.
- Heurística de orientación "reparar o reemplazar": herramienta de apoyo a la decisión a partir de los datos cargados por el usuario, no una recomendación financiera ni una tasación objetiva del vehículo.

#### 8.2 Explícitamente fuera de alcance
- Integración automática con el vehículo u OBD.
- Integración con bancos, billeteras o estaciones de servicio.
- Integración con talleres, aseguradoras u otros servicios externos.
- Obtención automática del valor de mercado del vehículo.
- Tasación profesional del vehículo.
- Machine learning o modelos predictivos complejos.
- Aplicación móvil nativa.
- Gestión multiusuario o vehículos compartidos entre distintos usuarios.

**Relación necesidad → funcionalidad → alcance:** el registro de combustible, mantenimiento, reparaciones y otros gastos, junto con la gestión de uno o varios vehículos, resuelve la necesidad de centralizar la información y gestionar cada vehículo de forma independiente. El costo real por kilómetro y el gasto acumulado por categoría resuelven la necesidad de conocer el costo real del vehículo. La comparación con el promedio histórico propio resuelve la necesidad de detectar aumentos. La estimación de próximo mantenimiento resuelve la necesidad de recordar y anticipar mantenimientos. La heurística de reparar o reemplazar resuelve la necesidad de contar con información para esa decisión (todas, necesidades de la sección 3). Lo que queda fuera de esta versión (8.2) son las funcionalidades que no son imprescindibles para resolver esas necesidades: requieren una fuente de datos externa (integración con el vehículo, bancos, talleres o aseguradoras), un análisis que excede un cálculo directo (tasación de mercado, modelos predictivos) o una ampliación de alcance no comprometida en esta etapa (aplicación móvil nativa, gestión multiusuario).

#### 8.3 Decisión de diseño: indicador en la aplicación, no notificación push

La estimación de próximo mantenimiento se muestra como un indicador dentro de la aplicación, no como una notificación push. Esto resuelve la misma necesidad identificada en la sección 3 —recordar mantenimientos y conocer los próximos— sin cambiar la lógica de uso del resto del producto: el usuario consulta sus indicadores cuando los necesita, y el aviso de mantenimiento se integra en esa misma consulta. Una notificación push cambiaría esa lógica —pasaría de ser una herramienta de consulta y análisis a un sistema que también interrumpe al usuario de forma proactiva—, algo que no forma parte del valor central que esta versión busca entregar.

### 9. Alcance del proyecto

El alcance del proyecto define el trabajo que el equipo se compromete a realizar para construir el producto descripto en la sección 8, dentro del marco del TPI — a diferencia del alcance del producto, que define qué hace el software.

- Se desarrollará una Progressive Web App (PWA) responsive, compuesta por frontend, backend y base de datos, que implementa las funcionalidades del MVP y sus indicadores/análisis definidos en la sección 8. El carácter responsive de la PWA cubre el acceso desde distintos dispositivos sin requerir una aplicación móvil nativa, ya excluida del alcance del producto (sección 8.2).
- El desarrollo se organiza en un repositorio único de GitHub, con el código fuente, la base de datos y la documentación del proyecto centralizados allí, conforme al requisito de repositorio único que exige la cátedra.
- Se realizará el despliegue en la nube , alojando  los componentes principales del sistema (backend, frontend y base de datos) en un servicio online.
- La elección de tecnologías específicas (lenguajes, frameworks, motor de base de datos, plataforma de despliegue) no forma parte de esta sección — se define y justifica en `docs/stack.md`. El cronograma, las tareas y los entregables por etapa se documentan en `docs/plan-de-trabajo.md`.
