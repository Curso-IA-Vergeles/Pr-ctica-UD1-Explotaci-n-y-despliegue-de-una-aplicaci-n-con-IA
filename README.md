# Práctica UD1 · Resumidor de textos con IA

Miniapp de una sola pantalla que resume un texto mediante la API de Google Gemini. El
frontend es una SPA de **React + TypeScript + Tailwind CSS** y el backend es **FastAPI**.
La autenticación se delega en **Clerk** y el backend valida el JWT de sesión antes de
consumir la API de IA.

> **Alcance:** una pantalla, un formulario y una operación de IA. No hay base de datos,
> historial, CRUD ni gestión propia de usuarios.

## 1. Identificación

| Campo | Valor |
| --- | --- |
| Práctica | UD1 · Explotación y despliegue de una aplicación con IA |
| Miniapp | Resumidor de textos |
| Repositorio | <https://github.com/davidlt17/PUD1> |
| Integrantes | Pendiente de completar por el grupo (autores en Git: `davidlt17`, `CesarCorderoAndrade`) |
| Aportaciones | Pendiente de registrar por hitos |

## 2. Plan de documentación

La documentación está pensada para que el profesorado y cualquier integrante pueda
reproducir el despliegue sin ayuda: qué se ejecuta, con qué variables, cómo se comprueba
y qué evidencias existen. Se mantiene en este único `README.md`, se actualiza al cerrar
cada hito y las capturas viven en `evidencias/` cuando se añadan.

Se han consultado la [guía Diátaxis](https://diataxis.fr/) para separar explicación,
procedimientos y referencia, y la
[guía de Markdown de GitHub](https://docs.github.com/en/get-started/writing-on-github)
para tablas, enlaces relativos y diagramas Mermaid.

## 3. Arquitectura

```mermaid
flowchart LR
    U[Navegador] -->|"login / JWT Clerk"| F["React + TS + Tailwind (SPA)"]
    F -->|"POST /api/generar + Bearer JWT"| A[FastAPI]
    A -->|"valida firma, exp y azp"| C[Clerk]
    A -->|"prompt"| G[Google Gemini]
    G -->|"resumen"| A
    A -->|"JSON {resumen}"| F
# React + TypeScript + Vite
# Práctica UD1 - Explotación y Despliegue de una Aplicación con IA

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.
Aplicación completa compuesta por un frontend en **React + TypeScript + Vite** y un backend en **Python (FastAPI)** que interactúa con proveedores de IA.

Currently, two official plugins are available:
---

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)
## Backend (Python / FastAPI)

## React Compiler
El backend se encuentra dentro de la carpeta [`api/`](file:///home/David/Documentos/IDES/espa/Pr-ctica-UD1-Explotaci-n-y-despliegue-de-una-aplicaci-n-con-IA/api).

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).
### 1. Configuración de la API Key y Variables de Entorno

## Expanding the Oxlint configuration
El backend requiere una clave de API para comunicarse con el modelo de lenguaje.

If you are developing a production application, we recommend enabling type-aware lint rules by installing `oxlint-tsgolint` and editing `.oxlintrc.json`:
1. Crea o edita el archivo `.env` en la **raíz del proyecto** (puedes tomar como base [.env.example](file:///home/David/Documentos/IDES/espa/Pr-ctica-UD1-Explotaci-n-y-despliegue-de-una-aplicaci-n-con-IA/.env.example)):

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "options": {
    "typeAware": true
  },
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

- **Vercel:** un único proyecto. La SPA se compila como sitio estático y `api/main.py`
  se ejecuta como Vercel Function con runtime Python. `vercel.json` reescribe `/api/*`
  hacia la función.
- **Docker/EC2:** una única imagen y un único contenedor. FastAPI sirve la SPA compilada
  desde `api/static` y atiende `/api/*` en el mismo puerto `8000`.

## 4. Requisitos e instalación local

Versiones usadas para verificar este repositorio:

| Herramienta | Versión |
| --- | --- |
| Python | 3.13 |
| Node.js | 22 |
| npm | 10 |
| FastAPI | 0.162.0 |
| google-genai | 2.34.0 |
| clerk-backend-api | 7.1.0 |
| React | 19 |
| Vite | 8 |
| Tailwind CSS | 4.3 |

### 4.1. Backend

```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload --port 8000
```

- Health: <http://127.0.0.1:8000/api/health>
- Swagger: <http://127.0.0.1:8000/docs>
- Operación principal: `POST /api/generar`

### 4.2. Frontend

```bash
npm install
npm run dev
```

Vite sirve la SPA en `http://localhost:5173` y redirige `/api/*` a
`http://127.0.0.1:8000` mediante el proxy de `vite.config.ts`.

### 4.3. Compilación de producción

```bash
npm run build
```

Genera `dist/`. Tailwind CSS v4 se procesa con `@tailwindcss/postcss` y
`@import "tailwindcss"` en `src/index.css`; ya no se usan las directivas `@tailwind`
de la versión 3.

## 5. Variables de entorno

La plantilla pública es [`.env.example`](.env.example). El `.env` real está ignorado por
Git y nunca debe subirse.

| Nombre | Finalidad | Carácter | Dónde se configura | Cuándo se usa |
| --- | --- | --- | --- | --- |
| `AI_PROVIDER_API_KEY` | Clave de Google AI Studio para Gemini | **Secreto** | `.env`, Vercel, EC2 | Ejecución (servidor) |
| `AI_MODEL` | Modelo principal de Gemini | Configuración | `.env`, Vercel, EC2 | Ejecución (servidor) |
| `AI_FALLBACK_MODEL` | Modelo de respaldo si el principal está saturado | Configuración | `.env`, Vercel, EC2 | Ejecución (servidor) |
| `AI_TIMEOUT_SECONDS` | Tiempo máximo de espera del proveedor | Configuración | `.env`, Vercel, EC2 | Ejecución (servidor) |
| `VITE_CLERK_PUBLISHABLE_KEY` | Clave publicable de Clerk | Público | `.env`, Vercel, build-arg Docker | Compilación del frontend |
| `CLERK_SECRET_KEY` | Clave secreta para validar el JWT | **Secreto** | `.env`, Vercel, EC2 | Ejecución (servidor) |
| `CLERK_AUTHORIZED_PARTIES` | Orígenes permitidos para `azp`, separados por comas | Configuración | `.env`, Vercel, EC2 | Ejecución (servidor) |
| `STATIC_DIR` | Directorio de la SPA compilada | Configuración | Solo Docker (opcional) | Ejecución (servidor) |

La clave `VITE_CLERK_PUBLISHABLE_KEY` se incrusta en el bundle y es visible en el
navegador: es pública por diseño. `AI_PROVIDER_API_KEY` y `CLERK_SECRET_KEY` no salen
nunca del servidor. Si cambia la clave publicable hay que recompilar el frontend o
reconstruir la imagen.

## 6. Vercel

El proyecto único contiene la SPA y la función Python:

- `vercel.json` reescribe `/api/(.*)` a `/api/main`.
- La función expone `GET /api/health` y `POST /api/generar`.
- Variables de servidor: `AI_PROVIDER_API_KEY`, `AI_MODEL`, `AI_FALLBACK_MODEL`,
  `AI_TIMEOUT_SECONDS`, `CLERK_SECRET_KEY`, `CLERK_AUTHORIZED_PARTIES`.
- Variable de compilación: `VITE_CLERK_PUBLISHABLE_KEY`.
- `CLERK_AUTHORIZED_PARTIES` debe incluir el dominio de producción y los de preview que
  se vayan a usar; no se debe limitar a `localhost`.

**Estado:** el repositorio conserva la configuración de Vercel y su historial de
despliegues, pero la URL final, las operaciones de CLI y sus capturas aún no están
registradas en este README. Queda pendiente cerrar ese hito con evidencias reales
(`vercel link`, `vercel deploy --prod`, `vercel env ls`, `vercel inspect`/`vercel logs`).

## 7. Clerk

- La SPA envuelve la aplicación en `ClerkProvider` (`src/main.tsx`) y muestra el
  formulario solo con `SignedIn`.
- `useAuth().getToken()` obtiene el JWT y lo envía como `Authorization: Bearer ...`.
- FastAPI valida el token con el SDK oficial `clerk-backend-api` en `require_user()`:
  firma, caducidad, `nbf`, `azp` y parámetros aplicables. Sin token válido devuelve
  **401** y no se llama al proveedor de IA.
- La clave secreta y la validación viven solo en el servidor; ocultar el formulario no
  sustituye a esta comprobación.
- Entorno previsto: instancia de desarrollo de Clerk con cuentas de prueba.

Evidencia automática del rechazo: `test_generar_rechaza_peticion_sin_token` y
`test_generar_rechaza_token_invalido` en [`api/test_main.py`](api/test_main.py).

Comprobación manual con el backend en marcha:

```bash
curl -i -X POST http://127.0.0.1:8000/api/generar \
  -H 'Content-Type: application/json' \
  -d '{"texto":"Texto de prueba"}'
# HTTP/1.1 401 Unauthorized
```

## 8. Docker

La imagen es multi-etapa: Node compila la SPA y Python ejecuta FastAPI con los estáticos
copiados a `api/static`. Hay **un único contenedor**.

### 8.1. Construcción

```bash
docker build \
  --build-arg VITE_CLERK_PUBLISHABLE_KEY="pk_test_..." \
  -t resumidor-ia:local .
```

El build-arg solo contiene la clave publicable. Si falta, el `Dockerfile` falla a
propósito. Los secretos no se pasan en la construcción.

### 8.2. Ejecución

Con Compose (recomendado; usa [`docker-compose.yml`](docker-compose.yml) y `.env`):

```bash
docker compose up -d --build
docker compose ps
```

Equivalente con Docker directo:

```bash
docker build \
  --build-arg VITE_CLERK_PUBLISHABLE_KEY="pk_test_..." \
  -t resumidor-ia:local .
docker run -d --name resumidor-ia --restart unless-stopped \
  -p 8000:8000 --env-file .env resumidor-ia:local
```

`--env-file` inyecta los secretos **en ejecución**; no se copian a la imagen. El
`.dockerignore` excluye `.env`, `.venv`, `node_modules`, `dist`, tests y documentación.
El proceso corre como usuario no root y escucha en `0.0.0.0:8000`.

### 8.3. Direcciones de acceso

El puerto se publica en `0.0.0.0:8000` y `[::]:8000`. Direcciones comprobadas en esta
máquina:

| Desde | URL |
| --- | --- |
| El propio host | <http://localhost:8000/> o <http://127.0.0.1:8000/> |
| La red local (WLAN actual) | <http://192.168.14.128:8000/> |
| IP interna del contenedor (desde el host) | <http://172.18.0.2:8000/> |
| Otro contenedor de la red Compose | <http://app:8000/> |

La IP `172.18.0.2` cambia si se recrea el contenedor; para el uso normal utiliza
`localhost:8000` o la IP LAN. La IP LAN puede cambiar por DHCP.

### 8.4. Estado, logs y ciclo de vida

```bash
docker ps
docker logs --tail 100 resumidor-ia
docker compose logs -f
docker stop resumidor-ia
docker start resumidor-ia
docker restart resumidor-ia
docker compose restart
docker compose down
docker rm -f resumidor-ia
```

Comprobación:

```bash
curl http://127.0.0.1:8000/api/health   # {"status":"ok"}
```

La imagen incluye un `HEALTHCHECK` contra `/api/health`.

**Estado verificado:** imagen `resumidor-ia:local` construida con Docker 29.9.2;
contenedor `resumidor-ia` en estado `healthy` con el puerto `8000` publicado. Se
comprobaron `/api/health` (200), `/` (200), `POST /api/generar` sin token (401) y una
llamada real a Gemini desde el contenedor (200). La primera prueba autenticada desde el
navegador devolvió 502 porque Gemini respondió 503 por saturación del modelo; el backend
ahora reintenta brevemente, usa `AI_FALLBACK_MODEL` y devuelve un 503 comprensible si
todos los modelos están ocupados.

## 9. AWS EC2

Procedimiento previsto para el hito final (aún sin evidencias en este README):

1. Instancia Linux (Amazon Linux 2023 o Ubuntu) con Docker instalado.
2. Security Group: `22/tcp` solo desde la IP de administración; `80/tcp` (o `8000/tcp`)
   solo desde la IP de demo/evaluación. No abrir el puerto de administración de Docker.
3. Clonar el repositorio, construir la imagen con el build-arg público y ejecutar un
   único contenedor:

   ```bash
   docker build --build-arg VITE_CLERK_PUBLISHABLE_KEY="pk_test_..." -t resumidor-ia:aws .
   docker run -d --name resumidor-ia --restart unless-stopped \
     -p 80:8000 --env-file /home/ec2-user/resumidor.env resumidor-ia:aws
   ```

4. Configurar `CLERK_AUTHORIZED_PARTIES` con `http://IP_PUBLICA` (o el puerto elegido).
5. Comprobar desde un navegador externo `http://IP_PUBLICA` y el rechazo sin token.
6. Actualizar: `git pull`, reconstruir la imagen, `docker rm -f resumidor-ia` y volver a
   ejecutar con el mismo `--env-file`.

> EC2 se usa por HTTP en un entorno docente: no hay TLS ni dominio propio. Las sesiones
> de Clerk viajan sin cifrar; deben usarse cuentas y datos de prueba. Hay que comprobar
> pronto la compatibilidad de la instancia de desarrollo de Clerk con el origen HTTP y
> documentar cualquier restricción sin desactivar la autenticación.

## 10. Operación y verificación

### Tests de backend

```bash
cd api
source venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

Resultado verificado: **8 passed**. Casos cubiertos:

| Test | Qué demuestra |
| --- | --- |
| `test_health_check_es_publico` | El health responde 200 sin autenticación |
| `test_generar_resumen_con_sesion_valida` | Flujo correcto con sesión válida y proveedor simulado |
| `test_generar_usa_modelo_de_respaldo_si_el_primario_esta_saturado` | Si el modelo principal devuelve 503, se usa el de respaldo |
| `test_generar_devuelve_503_si_todos_los_modelos_estan_saturados` | Saturación total controlada, sin filtrar el detalle del proveedor |
| `test_generar_rechaza_texto_vacio` | Validación de entrada (400) |
| `test_generar_devuelve_502_si_falla_el_proveedor` | Error del proveedor controlado y sin filtrar detalles internos |
| `test_generar_rechaza_peticion_sin_token` | 401 sin `Authorization` |
| `test_generar_rechaza_token_invalido` | 401 con token rechazado por Clerk |

Los tests no hacen llamadas de pago: el proveedor y la validación de Clerk se simulan.

### Comprobaciones manuales

```bash
# SPA y health (Docker o simulación local)
curl -I http://127.0.0.1:8000/
curl http://127.0.0.1:8000/api/health

# Logs del contenedor sin datos sensibles
docker logs --tail 100 resumidor-ia
```

En el navegador: iniciar sesión, enviar un texto, ver el resumen y cerrar sesión. Después,
repetir la petición directa sin token y comprobar el 401.

## 11. Problemas y soluciones

| Síntoma | Diagnóstico | Solución | Comprobación |
| --- | --- | --- | --- |
| `ModuleNotFoundError: No module named 'google'` al ejecutar tests | El venv no tenía instaladas las dependencias del backend | `pip install -r requirements-dev.txt` | `pytest -q` importa y ejecuta |
| `TypeError: Client.__init__() got an unexpected keyword argument 'app'` | Venv con versiones incompatibles de `httpx`/Starlette | Actualizar dependencias y fijarlas en `requirements*.txt` | Tests en verde con `httpx==0.28.1` |
| `vite build` no resuelve `@clerk/clerk-react` | `node_modules` desincronizado con `package.json` | `npm install` y conservar `package-lock.json` | `npm run build` compila |
| El frontend se ve sin estilos y el CSS pesa ~1,8 kB | Tailwind v4 sin plugin PostCSS y con directivas `@tailwind` de v3 | `@tailwindcss/postcss` + `@import "tailwindcss"` | El CSS generado incluye `.min-h-screen` y pesa ~13,8 kB |
| El endpoint de IA aceptaba peticiones sin sesión | El backend no validaba el JWT de Clerk | Dependencia `require_user` con el SDK oficial | Tests 401 y `curl` sin token |
| `502 Bad Gateway` al generar desde el navegador | Gemini devolvió `503 UNAVAILABLE` por alta demanda del modelo (`gemini-2.5-flash`), no por la API key | Reintento corto en el SDK, modelo de respaldo `gemini-3.5-flash` y 503 con mensaje claro | Llamada real a Gemini 200; tests de fallback y 503 |

## 12. Git, versiones y evidencias

Hitos y commits relevantes de este cambio:

- Validación de sesión de Clerk y servido de la SPA desde FastAPI.
- Tests reescritos con proveedor simulado y rechazo 401.
- Tailwind CSS v4 configurado.
- Imagen Docker multi-etapa y `.dockerignore`.
- Reintento corto y modelo de respaldo ante la saturación de Gemini.
- `docker-compose.yml` para construir y ejecutar el contenedor local.
- Documentación de tests, Docker, direcciones y variables.

El tag `v0.5-docker` apunta al commit de documentación de este hito. Las capturas de
Vercel, Clerk, Docker y EC2 se guardarán en `evidencias/` y se enlazarán aquí cuando
existan; no se incluyen capturas simuladas.

## 13. Referencias

- [FastAPI en Vercel](https://vercel.com/docs/frameworks/backend/fastapi)
- [Runtime Python de Vercel](https://vercel.com/docs/functions/runtimes/python)
- [Vercel CLI](https://vercel.com/docs/cli)
- [Clerk: entornos de desarrollo y producción](https://clerk.com/docs/guides/development/managing-environments)
- [Clerk: SDK de Python](https://clerk.com/docs/references/python/overview)
- [Reglas de Security Groups de EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules-reference.html)
