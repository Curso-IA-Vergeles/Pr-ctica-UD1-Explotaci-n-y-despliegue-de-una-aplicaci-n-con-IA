# syntax=docker/dockerfile:1

# Etapa 1: compila la SPA. La clave publicable de Clerk es pública y se
# incrusta en el bundle en tiempo de compilación; los secretos no entran aquí.
FROM node:22-alpine AS frontend
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY index.html vite.config.ts postcss.config.js ./
COPY tsconfig.json tsconfig.app.json tsconfig.node.json ./
COPY public ./public
COPY src ./src

ARG VITE_CLERK_PUBLISHABLE_KEY
RUN test -n "$VITE_CLERK_PUBLISHABLE_KEY" \
    || (echo "Falta el build-arg VITE_CLERK_PUBLISHABLE_KEY" >&2; exit 1)
ENV VITE_CLERK_PUBLISHABLE_KEY=${VITE_CLERK_PUBLISHABLE_KEY}
RUN npm run build

# Etapa 2: un único servicio con FastAPI y la SPA compilada.
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app/api

COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./
COPY --from=frontend /app/dist ./static

RUN groupadd --gid 10001 appuser \
    && useradd --create-home --uid 10001 --gid 10001 appuser \
    && chown -R 10001:10001 /app
USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"]

# Escucha en todas las interfaces para que el puerto publicado sea accesible.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
