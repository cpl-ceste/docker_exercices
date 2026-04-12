# Aplicación Mejorada de GenAI en Go

Una aplicación GenAI desarrollada en Go que puedes ejecutar localmente usando tu LLM favorito — solo sigue la guía para comenzar.

## Características

- **Respuestas Estructuradas**: Formato Markdown para una mejor legibilidad
- **Validación de Variables de Entorno**: Validación adecuada con valores predeterminados sensatos
- **Caché**: Caché de respuestas en memoria con TTL
- **Límite de Tasa (Rate Limiting)**: Basado en la dirección IP del cliente
- **Endpoint de Estado (Health Check)**: Información detallada del sistema para monitorización y orquestación
- **Documentación de la API**: Swagger UI para explorar y probar la API
- **Cabeceras de Seguridad**: Protección contra vulnerabilidades web comunes
- **Modo Oscuro**: La preferencia del usuario se guarda en el localStorage
- **Diseño Responsivo**: Funciona bien en dispositivos móviles
- **Manejo de Errores Mejorado**: Mejores mensajes de error y registros (logging)

## Variables de Entorno

- `PORT`: El puerto en el que se ejecutará el servidor (por defecto: 8080)
- `LLM_BASE_URL`: La URL base de la API del LLM (requerido)
- `LLM_MODEL_NAME`: El nombre del modelo a usar para las solicitudes de API (requerido)
- `LOG_LEVEL`: El nivel de registro o logging (por defecto: INFO)

## Endpoints de la API

- `GET /`: Interfaz principal del chat
- `POST /api/chat`: Endpoint de la API de chat
- `GET /health`: Endpoint de estado de salud con información detallada del sistema
- `GET /example`: Ejemplo de formato estructurado
- `GET /api/docs`: Swagger UI para la documentación de la API

## Ejecutando la Aplicación

### Usando Docker

```bash
docker build -t hello-genai-go .
docker run -p 8080:8080 -e LLM_BASE_URL=http://tu-api-llm -e LLM_MODEL_NAME=tu-modelo hello-genai-go
```

### Sin Docker

```bash
go mod download
go run main.go
```

## Solución de Problemas

### La Documentación de la API no Carga

Si la documentación de la API en `/api/docs` no se carga:

1. Comprueba si Swagger UI es accesible en `/api/docs`
2. Verifica que el archivo JSON de Swagger sea accesible en `/static/swagger.json`
3. Revisa la consola del navegador por si hay errores de JavaScript

### El Endpoint de Estado no Funciona

Si el endpoint de salud (health check) en `/health` no está devolviendo datos:

1. Comprueba si el endpoint es accesible
2. Verifica que la respuesta sea un formato JSON válido
3. Revisa los registros del servidor por si hay errores

### Los Archivos Estáticos no Cargan

Si los archivos estáticos no se están cargando:

1. Comprueba si la página de prueba es accesible a través de `/static/test.html` [Añade el archivo test.html si falta]
2. Verifica que el directorio de archivos estáticos esté montado correctamente en Docker
3. Revisa los permisos de los archivos en el directorio estático

## Desarrollo

Para ejecutar la aplicación en modo desarrollo:

```bash
export LLM_BASE_URL=http://tu-api-llm
export LLM_MODEL_NAME=tu-modelo
go run main.go
```
