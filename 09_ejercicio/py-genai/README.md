# Aplicación GenAI en Python

Una aplicación GenAI en Python que puedes ejecutar localmente usando tu LLM favorito — solo sigue la guía para comenzar.

## Variables de Entorno

La aplicación utiliza las siguientes variables de entorno:

- `LLM_BASE_URL`: La URL base de la API del LLM
- `LLM_MODEL_NAME`: El nombre del modelo a utilizar
- `PORT`: El puerto en el que se ejecutará la aplicación (por defecto: 8081)
- `DEBUG`: Establecer en "true" para habilitar el modo de depuración (por defecto: "false")
- `LOG_LEVEL`: Establece el nivel de registro o logging (por defecto: "INFO")

## Endpoints de la API

- `GET /`: Interfaz web para la aplicación de chat
- `POST /api/chat`: Envía un mensaje a la IA y obtén una respuesta
- `GET /health`: Endpoint de verificación de estado (health check)
- `GET /api/docs`: Documentación de la API

## Ejecutando la Aplicación

### Usando Docker Compose

```bash
docker-compose up python-genai
```

### Ejecutando de Forma Local

```bash
cd py-genai
pip install -r requirements.txt
python app.py
```
