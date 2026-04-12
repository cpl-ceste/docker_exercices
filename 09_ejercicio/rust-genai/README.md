# Aplicación GenAI en Rust

Esta es una implementación en Rust de la aplicación Hello-GenAI.

## Variables de Entorno
- `PORT`: El puerto en el que se ejecutará el servidor (por defecto: 8083)
- `LLM_BASE_URL`: La URL base de la API del LLM (requerido)
- `LLM_MODEL_NAME`: El nombre del modelo a usar para las peticiones a la API (requerido)
- `LOG_LEVEL`: El nivel de registro o logging (por defecto: INFO)

## Endpoints de la API
- `GET /`: Interfaz principal del chat
- `POST /api/chat`: Endpoint de la API del chat
- `GET /health`: Endpoint de verificación de estado (health check)
- `GET /example`: Ejemplo de formateo estructurado
- `GET /api/docs`: Interfaz Swagger UI para la documentación de la API

---

## Ejecutando la Aplicación

Puedes ejecutar la aplicación usando Docker Compose o compilarla y ejecutarla de forma nativa.

### Prerrequisitos
- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/) para la configuración en contenedores
- [Cadena de herramientas de Rust](https://www.rust-lang.org/tools/install) (cargo, rustc) para la compilación nativa

### Variables de Entorno

Antes de ejecutar, copia `.env.example` a `.env` y completa los valores requeridos:

```sh
cp .env.example .env
# Edita .env según sea necesario
```

### Usando Docker Compose

1. Construye e inicia los servicios:

   ```sh
   docker-compose up --build
   ```

2. La aplicación estará disponible en [http://localhost:8083](http://localhost:8083).

3. Para detener los servicios:

   ```sh
   docker-compose down
   ```

### Ejecutando Nativamente (Sin Docker)

1. Instala la cadena de herramientas de Rust (cargo, rustc).
2. Clona el repositorio y entra en el directorio.
3. Copia `.env.example` a `.env` y completa los valores requeridos.
4. Construye y ejecuta:

   ```sh
   cargo build --release
   cargo run --release
   ```

5. La aplicación estará disponible en [http://localhost:8083](http://localhost:8083).

---

## Desarrollo
- Requiere Rust (edición 2021)
- Utiliza Actix-web, Tera, DashMap y otros crates

---

¡Siéntete libre de abrir issues o contribuir!
