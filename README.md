# React + TypeScript + Vite
# Práctica UD1 - Explotación y Despliegue de una Aplicación con IA

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.
Aplicación completa compuesta por un frontend en **React + TypeScript + Vite** y un backend en **Python (FastAPI)** que interactúa con proveedores de IA.

Currently, two official plugins are available:
---

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)
## 🚀 Backend (Python / FastAPI)

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

See the [Oxlint rules documentation](https://oxc.rs/docs/guide/usage/linter/rules) for the full list of rules and categories.
2. Configura tu API Key según el proveedor que vayas a utilizar:

#### Opción A: Google Gemini (Recomendado)
Obtén tu API key gratuita en [Google AI Studio](https://aistudio.google.com/):
```env
AI_PROVIDER_API_KEY=tu_api_key_de_gemini
AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
AI_MODEL=gemini-3.5-flash
```

#### Opción B: OpenAI
Obtén tu API key en [OpenAI Platform](https://platform.openai.com/api-keys):
```env
AI_PROVIDER_API_KEY=sk-...tu_api_key_de_openai
AI_MODEL=gpt-3.5-turbo
```

> [!NOTE]
> El archivo `.env` está incluido en `.gitignore` para proteger tus claves y evitar que se suban accidentalmente al repositorio.

### 2. Configuración y ejecución

Navega al directorio de la API:

```bash
cd api
```

#### Paso A: Crear y activar el entorno virtual (si no está creado)

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual en Linux/macOS
source venv/bin/activate
```

> En Windows (PowerShell):
> ```powershell
> .\venv\Scripts\Activate.ps1
> ```

#### Paso B: Instalar dependencias

```bash
pip install -r requirements.txt
```

#### Paso C: Iniciar el servidor

Arranca el servidor en el puerto **8000** (puerto esperado por el proxy de Vite):

```bash
uvicorn main:app --reload --port 8000
```

*Alternativa directa sin activar el venv (Linux):*
```bash
./venv/bin/uvicorn main:app --reload --port 8000
```

### 3. Endpoints disponibles

Una vez iniciado el servidor:
- **Health Check:** [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
- **Documentación Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Endpoint principal:** `POST /api/generar`

---

## 💻 Frontend (React + Vite)

Desde la raíz del proyecto:

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend iniciará normalmente en `http://localhost:5173` y redirigirá automáticamente las peticiones hacia `/api/*` al backend en el puerto `8000`.

---

## 🛠️ Herramientas y Linter

El proyecto incluye soporte para Oxlint y TypeScript. Para revisar reglas de linter:
- Configuración en `.oxlintrc.json`

