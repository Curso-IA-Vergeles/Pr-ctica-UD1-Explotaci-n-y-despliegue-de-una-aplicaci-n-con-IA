# Práctica UD1 · Explotación y despliegue de una aplicación con IA

**Módulo:** Explotación de Servicios de Procesamiento y Analítica de Datos  
**Enseñanza:** Curso de especialización de Inteligencia Artificial  
**Modalidad:** Grupos de 2–3 integrantes, salvo excepciones autorizadas por el profesorado  
**Dedicación:** 4 horas presenciales, más trabajo autónomo en casa  
**Entrega y defensa:** En las fechas y por el canal que indique el profesorado

> **Esta NO es principalmente una práctica de desarrollo de aplicaciones.** La miniapp es el vehículo para aprender a **configurar, desplegar, securizar, probar y explotar** una aplicación que consume un servicio de IA en **Vercel y AWS**. La evaluación dará más peso al despliegue, la configuración, la operación y su explicación que al desarrollo o al diseño visual.

## 1. El reto

Crearéis una miniaplicación de IA deliberadamente pequeña y la desplegaréis de forma incremental en dos entornos:

1. **Vercel:** frontend y backend FastAPI en **un único proyecto**, con ejecución del backend mediante tecnología Serverless. Después incorporaréis autenticación con Clerk y volveréis a desplegar.
2. **AWS:** la aplicación completa en **un único contenedor Docker**, ejecutado en una instancia **EC2 Linux**, accesible desde el navegador.

El resultado deberá funcionar, poder reproducirse a partir del repositorio y estar explicado en un `README.md`. Tendréis que demostrarlo y defender las decisiones tomadas.

## 2. Qué aprenderéis

Al completar la práctica deberéis poder:

- Preparar una aplicación mínima para distintos entornos de ejecución.
- Desplegar frontend y API Python en un proyecto Vercel, y realizar operaciones reales con su CLI.
- Configurar variables de entorno y distinguir configuración pública de secretos.
- Integrar Clerk y comprobar que el backend rechaza solicitudes no autenticadas.
- Construir una imagen Docker, ejecutar el contenedor y consultar su estado y sus logs.
- Configurar una EC2, sus puertos y sus Security Groups, y comprobar el servicio desde fuera de la instancia.
- Diagnosticar incidencias, actualizar y reiniciar el servicio, y documentar procedimientos reproducibles.
- Mantener un historial Git que muestre la evolución y la aportación de cada integrante.

## 3. Alcance de la miniapp

### 3.1. Requisitos mínimos

| Elemento | Requisito |
| --- | --- |
| Backend | Python con FastAPI. Recibe la entrada, llama a una API externa de IA y devuelve JSON. |
| Proveedor de IA | Elección libre: OpenAI —modelos asociados a ChatGPT—, Claude, Gemini, OpenRouter u otro proveedor con API. |
| Frontend | SPA con **Vue.js o React**, a elección del grupo. **TypeScript y Tailwind CSS obligatorios**. |
| Interfaz | Una única pantalla de trabajo, un único formulario, envío al backend y visualización de la respuesta. |
| Comportamiento | Validación básica, indicación de carga y mensaje comprensible si falla la petición. |
| Tests | Pocos tests de backend, centrados en comportamientos relevantes. |

**Sugerencia de endpoints:** una operación principal, por ejemplo `POST /api/generar`, y, si resulta útil, un endpoint sencillo de salud como `GET /api/health`. No necesitáis una API extensa.

El navegador llamará a vuestro backend; **la llamada al proveedor de IA y su clave API permanecerán en el servidor**. Deberéis usar una API real: una suscripción a una interfaz de chat no implica necesariamente disponer de acceso o saldo para su API. Cada grupo comprobará las condiciones, disponibilidad y costes del proveedor elegido.

Para los tests, se recomienda una selección de **2–4 casos**: entrada válida con proveedor simulado, entrada incorrecta, error del proveedor y, tras integrar Clerk, rechazo de una petición sin autenticación. Evitad llamadas de pago en los tests automáticos. Complementadlos con comprobaciones manuales de los despliegues.

### 3.2. Ejemplos permitidos

Elegid uno de estos ejemplos o una idea de complejidad equivalente:

- **Resumidor:** introducir un texto y obtener un resumen breve.
- **Reformulador:** introducir un texto y obtener una versión más clara o formal.
- **Generador de preguntas:** introducir un texto y obtener unas pocas preguntas de repaso.
- **Clasificador:** introducir un mensaje y obtener una categoría de una lista pequeña.
- **Extractor de información:** introducir un texto y obtener unos pocos campos en JSON.
- **Generador de descripciones:** introducir características de un objeto y obtener una descripción breve.

Una sola operación de IA es suficiente. No se exige entrenar modelos, desplegar un modelo propio ni implementar un chat con historial.

### 3.3. Qué NO se permite

Para evitar que el desarrollo desplace al objetivo de la práctica, **no se permiten**:

- Bases de datos ni almacenamiento persistente del historial.
- CRUD de entidades.
- Paneles de administración.
- Múltiples pantallas funcionales o módulos de negocio.
- Gestión de usuarios propia: la autenticación se delegará en Clerk.
- Arquitecturas complejas, microservicios, múltiples contenedores o servicios adicionales innecesarios.
- Funcionalidades que desvíen el esfuerzo del despliegue: pagos, gestión documental, agentes complejos, RAG, etc.

**Aclaración:** los componentes o flujos de inicio y cierre de sesión de Clerk sí forman parte del alcance. No justifican añadir un área de usuarios, perfiles o administración. La gestión externa de identidades de Clerk no implica crear una base de datos en vuestra aplicación.

## 4. Organización, trabajo incremental y Git

El repositorio será **público en GitHub**. Todos los integrantes deberán tener una participación individual identificable y comprender el conjunto de la solución. No basta con que una sola persona publique todo el trabajo al final.

Repartid tareas y registrad las aportaciones en el `README.md`. Utilizad cuentas propias y commits con autoría correcta. Si trabajáis conjuntamente, dejad constancia de la coautoría o del trabajo compartido. La participación incluye configuración, pruebas, diagnóstico y documentación, además de código.

Haced **commits significativos** cuando completéis cambios coherentes. Por ejemplo:

- `Añade endpoint de IA y gestión de errores`
- `Conecta el formulario TypeScript con FastAPI`
- `Configura rutas y variables para Vercel`
- `Valida sesiones de Clerk en el backend`
- `Construye la imagen con el frontend compilado`
- `Documenta ejecución y diagnóstico en EC2`

Al terminar los hitos, cread una versión identificable mediante **tags de Git** y, cuando resulte útil, una **release de GitHub** con una breve descripción. Los tags deberán estar publicados en el repositorio y apuntar a los commits correspondientes.

| Hito | Ejemplo de versión |
| --- | --- |
| Backend mínimo funcionando | `v0.1-backend` |
| Frontend conectado en local | `v0.2-frontend` |
| Primer despliegue en Vercel | `v0.3-vercel` |
| Clerk integrado y redespliegue | `v0.4-auth` |
| Contenedor completo probado | `v0.5-docker` |
| Despliegue final en AWS | `v1.0-aws` |

**Los nombres pueden variar.** Lo importante es que permitan reconstruir las fases y relacionar cada despliegue con una versión del código. No creéis todas las versiones sobre el mismo commit final.

Las 4 horas presenciales se destinarán a avanzar en los hitos y resolver dificultades con el profesorado. El trabajo en casa es necesario para completar despliegues, verificaciones, documentación y presentación. Preparad previamente las cuentas y herramientas necesarias.

## 5. Fases de trabajo

### Fase 0. Preparación

1. Formad el grupo y elegid una miniapp del alcance permitido.
2. Cread el repositorio público y acordad el reparto inicial de tareas.
3. Preparad Python, Node.js, Git, Docker y las cuentas de GitHub, Vercel, Clerk, AWS y el proveedor de IA.
4. Cread `.gitignore` y un `.env.example` con nombres de variables y valores ficticios.
5. Planificad los hitos y la documentación siguiendo la nota del apartado 7.

**Comprobación:** ningún secreto debe aparecer en el primer commit ni en los siguientes.

### Fase 1. Backend mínimo

1. Implementad el backend FastAPI con una operación principal sencilla.
2. Leed la clave de IA desde una variable de entorno.
3. Validad la entrada y devolved JSON con una estructura clara y estable.
4. Tratad de forma básica los errores y tiempos de espera del proveedor, sin exponer secretos ni detalles internos al usuario.
5. Ejecutad los pocos tests seleccionados y una prueba real controlada de la API.
6. Registrad el hito en Git.

**Resultado:** una petición válida obtiene una respuesta y una petición incorrecta o un fallo del proveedor produce un error controlado.

### Fase 2. Frontend mínimo

1. Cread una SPA Vue.js o React con TypeScript y Tailwind CSS.
2. Añadid el único formulario y la visualización de la respuesta.
3. Conectadlo con FastAPI y mostrad los estados de carga y error.
4. Comprobad el flujo completo en local y cread la versión del hito.

**Resultado:** desde el navegador se envía una entrada, el backend consulta la IA y el frontend muestra el resultado. No dediquéis tiempo a añadir funcionalidades ni a perfeccionar innecesariamente el diseño.

### Parte 1 · Fase 3. Primer despliegue Serverless en Vercel

1. Organizad el código y la configuración para desplegar **la SPA y FastAPI en un único proyecto Vercel**.
2. Configurad la compilación del frontend y las rutas del backend según la documentación vigente de Vercel. FastAPI deberá ejecutarse mediante Vercel Functions con runtime Python; no se subirá el contenedor Docker a Vercel.
3. Configurad las variables de entorno necesarias, distinguiendo los entornos Preview y Production cuando proceda.
4. Instalad y utilizad **Vercel CLI**. No basta con instalarla o iniciar sesión.
5. Realizad, como mínimo, estas operaciones reales desde la CLI:
   - Vincular o consultar el proyecto y sus despliegues.
   - Crear un despliegue y publicar el despliegue final con la opción correspondiente.
   - Añadir o actualizar una variable de entorno y consultar su configuración sin mostrar su valor secreto.
   - Inspeccionar un despliegue o consultar logs para comprobar su funcionamiento o diagnosticar un problema.
6. Documentad los comandos efectivamente utilizados, su finalidad y el resultado, ocultando los datos sensibles.
7. Comprobad desde el navegador el frontend y una petición real al backend. Anotad la URL y cread la versión del hito.

**Aclaraciones:** un único proyecto puede tener varios despliegues. No se aceptan dos proyectos separados para frontend y backend. Adaptad las rutas y la compilación a Vue o React; no copiéis sin revisar configuraciones destinadas a otros frameworks. Considerad los límites de ejecución de las funciones y evitad procesos permanentes o trabajos en segundo plano.

### Parte 1 · Fase 4. Clerk y redespliegue

1. Incorporad Clerk a la SPA para iniciar y cerrar sesión.
2. Permitid usar la operación de IA únicamente a usuarios autenticados.
3. Enviad al backend el token de sesión y **validadlo en FastAPI** mediante el SDK o un mecanismo oficial compatible. Comprobad firma, caducidad y los parámetros de validación aplicables a vuestra configuración.
4. Configurad los orígenes y redirecciones necesarios para cada entorno. Si utilizáis CORS, limitadlo a los orígenes necesarios: CORS no sustituye a la autenticación.
5. Configurad las variables públicas y privadas de Clerk en el lugar adecuado.
6. Redesplegad y comprobad estos casos: acceso autenticado correcto, cierre de sesión y llamada directa al endpoint de IA sin token rechazada con un error de autenticación.
7. Guardad evidencias y cread la versión del hito.

**No basta con ocultar el formulario.** Una petición directa sin autenticación válida no debe poder consumir la API de IA. El endpoint de salud puede permanecer público si no revela información sensible.

> **Entorno docente de Clerk:** utilizad una instancia de desarrollo y cuentas de prueba, conforme a la documentación de Clerk. No se exige activar su entorno de producción ni adquirir un dominio propio. La etiqueta «Production» de un despliegue Vercel no convierte una instancia de desarrollo de Clerk en producción.

### Parte 2 · Fase 5. Un único contenedor Docker

1. Preparad un `Dockerfile` que genere **una imagen con la aplicación completa**.
2. Incluid el frontend compilado y el backend FastAPI. Una solución sencilla es que FastAPI sirva los archivos estáticos de la SPA y los endpoints de la API desde el mismo servicio.
3. Podéis utilizar una construcción por etapas; eso no implica ejecutar varios contenedores.
4. Añadid `.dockerignore` y excluid secretos, archivos `.env` privados y material innecesario del contexto de construcción.
5. Inyectad los secretos **al ejecutar** el contenedor. No los incorporéis a la imagen, a sus capas ni al `Dockerfile`.
6. Configurad el servicio para escuchar en la interfaz adecuada dentro del contenedor y publicad el puerto necesario en el host.
7. Probad en local la aplicación completa, incluida la autenticación, consultad estado y logs, y comprobad que podéis detener y volver a iniciar el contenedor.
8. Documentad construcción y ejecución, y cread la versión del hito.

**Resultado:** un solo contenedor en ejecución sirve frontend y backend. No se exige Docker Compose ni un registro de imágenes. Documentad cómo trasladaréis o construiréis la imagen en EC2 y a qué versión corresponde.

### Parte 2 · Fase 6. Despliegue en AWS EC2

1. Cread una instancia EC2 Linux adecuada para esta aplicación y anotad región, sistema operativo y tipo de instancia.
2. Configurad el acceso SSH, protegiendo la clave privada y restringiendo su acceso en el Security Group a las IP necesarias.
3. Instalad Docker y comprobad que funciona.
4. Trasladad o construid la imagen correspondiente a vuestra versión del repositorio.
5. Configurad las variables de entorno en EC2 mediante un archivo privado excluido de Git u otro mecanismo equivalente. Limitad el acceso al archivo.
6. Ejecutad **un único contenedor**, publicad el puerto web y configurad una política de reinicio apropiada.
7. Configurad los **Security Groups** para permitir el puerto web elegido desde el origen necesario para la demo y la evaluación. No abráis todos los puertos ni expongáis el servicio de administración de Docker.
8. Comprobad desde un navegador externo a EC2 la URL `http://IP_PUBLICA:PUERTO` —el puerto puede omitirse si es el 80—, el formulario y la respuesta real de IA.
9. Mantened la autenticación de Clerk y la validación de sesión en el backend. Revisad la configuración del origen de EC2 y las redirecciones; no desactivéis la protección para hacer funcionar la demo.
10. Consultad estado y logs, reiniciad el contenedor y volved a comprobar la aplicación. Explicad cómo actualizarla a una nueva versión.
11. Anotad la URL, guardad evidencias y cread la versión final del hito.

> **Simplificación de esta práctica:** no se requiere configurar un dominio propio, certificados ni HTTPS en EC2. El HTTPS que proporciona Vercel se utiliza tal como viene. EC2 por HTTP es un entorno de demostración docente: utilizad datos y cuentas de prueba, y explicad en el README la limitación de transportar sesiones sin cifrado. Comprobad pronto la compatibilidad de Clerk con vuestro origen HTTP; si aparece una restricción del proveedor o del navegador, documentadla y tratadla con el profesorado, sin eliminar la autenticación.

No añadáis balanceadores, Kubernetes, bases de datos ni otros servicios AWS. Comprobad los costes y las condiciones de vuestra cuenta: no deis por hecho que EC2, la IP pública o las APIs son gratuitas. Conservad el entorno disponible para la defensa según indique el profesorado y, al terminar, detened o eliminad los recursos que ya no necesitéis, incluidos recursos asociados que puedan seguir generando costes. Una IP pública puede cambiar al detener y arrancar una instancia; actualizad la URL si ocurre.

## 6. Seguridad y configuración obligatorias

- **Nunca** publiquéis claves API, claves privadas, secretos de Clerk, tokens de sesión ni credenciales AWS en código, GitHub, capturas, logs o diapositivas.
- Usad `.env` para el trabajo local cuando proceda y excluidlo con `.gitignore`. Publicad únicamente `.env.example` con valores ficticios.
- Utilizad las variables de entorno de Vercel y configuración privada en AWS. Evitad escribir secretos literalmente en comandos que se guardarán en el historial o se capturarán como evidencia.
- Distinguid los valores públicos de los privados: la clave publicable de Clerk puede llegar al frontend; su clave secreta y la clave del proveedor de IA deben permanecer en el servidor.
- Las variables incorporadas al bundle del frontend son visibles en el navegador aunque procedan de un `.env`. Nunca pongáis secretos en ellas. Si cambia una variable pública utilizada durante la compilación, recompilad y redesplegad el frontend o reconstruid la imagen según corresponda.
- Evitad incluir credenciales o entradas sensibles de usuarios en los logs. Usad textos de prueba y límites sencillos de entrada y salida para controlar el consumo de IA.
- Proteged el endpoint de IA con autenticación después de la fase de Clerk, tanto en Vercel como en AWS.
- Si se filtra un secreto, revocadlo o rotadlo inmediatamente y corregid el repositorio y su historial. Borrar el valor del último archivo no elimina su exposición previa.

## 7. Documentación: un único README.md

> **ANTES DE DOCUMENTAR: APRENDED A PLANIFICAR LA DOCUMENTACIÓN.** Antes de redactar el README, leed una guía sobre cómo elaborar un **plan de documentación eficiente**. Debéis decidir quién leerá la documentación, qué necesitará reproducir, qué secciones hacen falta, quién las mantendrá y qué evidencias recogeréis en cada fase. No esperéis al final para reconstruir comandos y problemas de memoria.
>
> Conoced herramientas útiles: **Markdown y su vista previa**, tablas y enlaces relativos, listas de comprobación, **Mermaid** para esquemas sencillos, herramientas de captura y ocultación de datos sensibles, y Git para revisar y mantener los cambios. Como lectura inicial podéis consultar la [guía Diátaxis](https://diataxis.fr/) para distinguir tipos de documentación y la [guía de Markdown de GitHub](https://docs.github.com/en/get-started/writing-on-github). Adaptad sus ideas a un único README breve, ordenado y práctico; no necesitáis crear un portal de documentación.

La documentación técnica se entregará **exclusivamente en el `README.md` de la raíz del repositorio**. Las capturas o diagramas podrán guardarse como recursos, por ejemplo en `evidencias/`, e insertarse o enlazarse desde el README. La presentación de defensa es una entrega adicional, no sustituye a la documentación técnica.

El README deberá permitir que otra persona comprenda y reproduzca el despliegue. Incluirá:

1. **Identificación:** práctica, integrantes, miniapp elegida y aportaciones individuales.
2. **Plan de documentación:** breve explicación del destinatario, estructura, reparto y actualización por hitos; enlace a la guía consultada.
3. **Arquitectura:** recorrido navegador → backend → API de IA y papel de Clerk; diferencias entre Vercel Serverless y EC2 con Docker. Basta un esquema sencillo.
4. **Requisitos e instalación local:** versiones relevantes de herramientas, dependencias, comandos y comprobación del funcionamiento.
5. **Variables de entorno:** tabla con nombre, finalidad, carácter público o secreto, lugar de configuración y momento de uso —compilación o ejecución—, sin valores reales sensibles.
6. **Vercel:** organización del proyecto único, compilación, rutas, variables, operaciones reales de CLI, URL y versión desplegada.
7. **Clerk:** entorno utilizado, inicio y cierre de sesión, configuración de orígenes y validación en backend; evidencia del rechazo sin token.
8. **Docker:** cómo construir, ejecutar, parar, reiniciar y consultar logs; puerto y suministro de variables; prueba del contenedor completo.
9. **AWS:** EC2 Linux, instalación de Docker, ejecución, puertos, reglas del Security Group, URL y versión desplegada.
10. **Operación y verificación:** tests y resultados, comprobaciones manuales en ambos entornos, consulta de estado/logs, actualización y reinicio; gestión de recursos al finalizar.
11. **Problemas y soluciones:** incidencias reales, síntomas, diagnóstico, solución y comprobación posterior. Si no hubo incidencias relevantes, indicadlo sin inventarlas.
12. **Git y evidencias:** hitos, tags/releases y capturas con una breve explicación de qué demuestra cada una.

Priorizad instrucciones reproducibles y decisiones justificadas. No copiéis documentación genérica ni peguéis salidas completas sin explicar qué demuestran. Las instrucciones y evidencias deben corresponder a vuestra implementación final.

## 8. Entrega previa y defensa posterior

### 8.1. Entrega previa

Por el canal que establezca el profesorado —por ejemplo, Moodle—, entregad:

- Enlace al **repositorio público de GitHub**, identificando grupo e integrantes.
- Identificador de la versión final: tag y commit correspondiente.
- URL de Vercel y URL HTTP de EC2, también recogidas en el README.
- `README.md` completo, accesible en el repositorio, con sus evidencias.
- Presentación para la defensa, como archivo o enlace accesible.

No entreguéis credenciales como parte de la entrega. Preparad un método de acceso de prueba para la demo sin publicar contraseñas ni tokens. Las fechas, el formato de la presentación y la disponibilidad requerida de los despliegues se concretarán por el profesorado.

### 8.2. Defensa obligatoria con presentación oral y demo

Todos los integrantes participarán. La presentación deberá explicar de forma breve:

- Qué hace la miniapp y por qué su alcance es mínimo.
- Cómo se despliega en Vercel y cómo se ejecuta en Docker sobre EC2.
- Cómo se configuran los secretos y se valida la autenticación.
- Una incidencia o decisión relevante y su comprobación.
- Cómo se organiza el historial Git y qué aportó cada integrante.

La demo mostrará la aplicación funcionando en **ambos entornos**, una operación de IA autenticada y el rechazo de una llamada al backend sin autenticación válida. También deberéis poder localizar la configuración de Vercel, el contenedor y las reglas de red de EC2 sin revelar secretos.

**El profesorado podrá preguntar a cualquier integrante sobre cualquier parte del trabajo.** El reparto de tareas no exime de comprender la solución completa. Preparad evidencias de respaldo ante fallos externos; estas no sustituyen automáticamente la comprobación del despliegue.

## 9. Rúbrica de evaluación · 10 puntos

La complejidad adicional de la aplicación no aporta puntuación. Se valoran el cumplimiento del alcance, el funcionamiento verificable y la capacidad de explicar y reproducir la explotación.

| Criterio | Máximo | Evidencias para obtener la puntuación completa |
| --- | ---: | --- |
| Aplicación mínima | **1,0** | FastAPI llama a la API de IA y devuelve JSON; SPA Vue/React con TypeScript y Tailwind, un formulario, estados básicos y pocos tests relevantes. Respeta el alcance. |
| Vercel | **2,5** | Frontend y backend Serverless en un proyecto único; configuración y rutas correctas, despliegue comprobado, varias operaciones reales de CLI e integración incremental de Clerk con redespliegue. |
| Docker y AWS | **3,0** | Un contenedor con la app completa, prueba local y ejecución en EC2 Linux; Docker, variables, puertos y Security Groups correctamente configurados; acceso externo, logs, reinicio y procedimiento de actualización verificables. |
| Seguridad y configuración | **1,0** | Secretos fuera del código, del repositorio y de la imagen; distinción entre variables públicas y privadas; validación de autenticación en backend, prueba de rechazo y acceso de red limitado a lo necesario. |
| Documentación y Git | **1,0** | README reproducible y centrado en explotación, plan de documentación, evidencias explicadas, commits significativos, versiones por hitos y participación individual identificable. |
| Defensa y demo | **1,5** | Presentación clara, participación de todos, demo de ambos despliegues y respuestas fundamentadas sobre configuración, seguridad, operación y decisiones. |
| **Total** | **10,0** | |

En cada criterio se asignará puntuación parcial según el grado de cumplimiento y la calidad de las evidencias. Un requisito sin implementar o sin poder comprobarse no se considerará acreditado por mencionarlo en el README. La comprobación técnica de seguridad se valora en su criterio; la claridad con la que se explica se valora en documentación y defensa.

## 10. Checklist final de entrega y evidencias

### Aplicación y versiones

- [ ] La miniapp respeta el alcance: una pantalla, un formulario y una operación de IA sencilla.
- [ ] El frontend usa Vue.js o React, TypeScript y Tailwind CSS.
- [ ] FastAPI consume una API de IA y devuelve JSON; los pocos tests seleccionados pasan.
- [ ] El repositorio GitHub es público y todos los integrantes tienen aportaciones identificables.
- [ ] Hay commits significativos y tags/versiones publicados para los hitos completados.
- [ ] Se identifica el commit o tag desplegado en cada entorno.

### Vercel y Clerk

- [ ] Captura del proyecto Vercel y del despliegue correcto, mostrando que frontend y backend pertenecen al mismo proyecto.
- [ ] Evidencias de varias operaciones reales con Vercel CLI, explicadas en el README.
- [ ] Captura de los nombres y entornos de las variables de Vercel **sin revelar valores secretos**.
- [ ] URL de Vercel anotada y aplicación funcionando tras integrar Clerk.
- [ ] Evidencia de la configuración de Clerk pertinente, sin claves secretas ni datos personales innecesarios.
- [ ] Evidencia de inicio/cierre de sesión y petición autenticada correcta.
- [ ] Evidencia de una petición directa al endpoint de IA sin token rechazada por FastAPI.

### Docker y AWS

- [ ] `Dockerfile` y `.dockerignore` disponibles; imagen construida sin secretos.
- [ ] Evidencia del único contenedor local en ejecución y de la aplicación completa funcionando.
- [ ] Captura de EC2 con la información necesaria para identificar la instancia, su sistema y su estado.
- [ ] Evidencia de Docker instalado y del único contenedor ejecutándose en EC2; logs revisados sin datos sensibles.
- [ ] Captura de las reglas de entrada del **Security Group**, con protocolo, puertos y orígenes visibles.
- [ ] Configuración de variables en AWS explicada sin mostrar secretos ni claves SSH.
- [ ] URL HTTP de EC2 anotada y captura desde el navegador de la aplicación funcionando con respuesta de IA.
- [ ] Autenticación y rechazo sin token comprobados también en AWS.
- [ ] Reinicio del contenedor comprobado y procedimiento de actualización documentado.
- [ ] Plan de disponibilidad para la defensa y retirada posterior de recursos indicado.

### Documentación, entrega y defensa

- [ ] Se ha leído una guía sobre el plan de documentación eficiente y se citan las herramientas utilizadas.
- [ ] El README cubre arquitectura, instalación, variables, Vercel, Clerk, Docker, AWS, operación, pruebas y problemas/soluciones.
- [ ] Las evidencias están insertadas o enlazadas desde el README y se explica qué demuestra cada una.
- [ ] Se han revisado repositorio, capturas, logs y presentación para evitar secretos.
- [ ] Se han entregado repositorio, versión final, URLs/evidencias, README y presentación por el canal indicado.
- [ ] Está preparada la **presentación oral con demo** y todos los integrantes pueden responder sobre el conjunto.

## 11. Referencias oficiales de apoyo

Consultad la documentación vigente y registrad las versiones utilizadas. Estos enlaces orientan la configuración; no sustituyen la explicación de vuestro propio proceso:

- [FastAPI en Vercel](https://vercel.com/docs/frameworks/backend/fastapi): ejecución del backend Python mediante Vercel Functions.
- [Runtime Python de Vercel](https://vercel.com/docs/functions/runtimes/python): configuración y límites del entorno de ejecución.
- [Vercel CLI](https://vercel.com/docs/cli): operaciones de proyectos, despliegues, variables e inspección.
- [Entornos de Clerk](https://clerk.com/docs/guides/development/managing-environments): diferencias entre desarrollo y producción, y uso de claves de desarrollo con dominios del proveedor de hosting.
- [Documentación de Clerk](https://clerk.com/docs): integración del framework elegido y validación de sesiones en el backend Python.
- [Reglas de Security Groups de EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules-reference.html): configuración del acceso web y SSH por protocolo, puerto y origen.
