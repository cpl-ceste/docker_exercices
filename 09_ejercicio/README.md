# hello-genai

Una aplicación web sencilla de chatbot construida en Go, Python y Node.js que se conecta a un servicio local de modelo de lenguaje (LLM, llama.cpp) para proporcionar respuestas impulsadas por IA.

## Variables de Entorno

La aplicación utiliza las siguientes variables de entorno definidas en el archivo `.env`:

- `LLM_BASE_URL`: La URL base de la API del LLM
- `LLM_MODEL_NAME`: El nombre del modelo a utilizar

Para cambiar esta configuración, simplemente edita el archivo `.env` en el directorio raíz del proyecto.

## Inicio Rápido

1. Clona el repositorio:
   ```bash
   git clone https://github.com/docker/hello-genai
   cd hello-genai
   ```

2. Inicia la aplicación usando Docker Compose:
   ```bash
   docker compose up
   ```

3. Abre tu navegador y visita los siguientes enlaces:

   http://localhost:8080 para la aplicación GenAI en Go

   http://localhost:8081 para la aplicación GenAI en Python

   http://localhost:8082 para la aplicación GenAI en Node

   http://localhost:8083 para la aplicación GenAI en Rust

## Requisitos

- macOS (versión reciente)
- Puedes elegir entre:
  - Docker y Docker Compose (recomendado)
  - Go 1.21 o superior
- Servidor LLM local

Si estás utilizando una configuración de servidor LLM diferente, es posible que necesites modificar el archivo `.env`.
