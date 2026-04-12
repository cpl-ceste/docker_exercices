# Ejercicio 16: Interacción Nativa y Web con Docker Model Runner

## Descripción del Problema
En este ejercicio vamos a explorar la nueva capacidad nativa de Docker Desktop para ejecutar modelos de Inteligencia Artificial locales (Docker Model Runner o DMR). Vamos a realizar una prueba de concepto en dos fases:

1. **Fase de CLI**: Veremos que es DMR y como se utiliza. Nos familiarizaremos con comandos interactivos de DMR cargando en segundo plano un modelo ligero (como `ai/smollm2`).

2. **Fase de Interfaz Gráfica**: Desplegaremos un contenedor de Open WebUI usando Docker Compose que se conecte transparente al motor subyacente de Docker Model Runner para ofrecer una experiencia estilo ChatGPT a los usuarios de nuestra red local.

El enfoque es crear aplicaciones de IA interactivas para desarrolladores y usuarios de nuestra red local de Docker utilizando herramientas tanto de terminal como gráficas en la web.

## Docker Model Runner (DMR)

Docker Model Runner permite ejecutar de forma nativa, segura y eficiente modelos de IA localmente mediante Docker. Para habilitar DMR en Docker Desktop hay que ir a Settings -> Pestaña IA habilitar "Model Runner". Las caracteristicas de configuracion pueden verse en [Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/)

Una vez habilitado podemos comprobar que esta corriendo:

`$ docker model status`

y testear el endpoint directamente en el navegador:

`http://localhost:12434`

Este motor de IA es compatible con las APIs de OpenAI y Ollama, por lo que se puede utilizar con cualquier herramienta compatible [IDE-integration](https://docs.docker.com/ai/model-runner/ide-integrations/)


## Parte 1: Consola (Docker CLI)

Ejecutamos de manera secuencial los comandos puros de la CLI de Docker local para:

1) Probar una petición al vuelo, ejecutando el comando para que se incie un chat de forma interactiva con el modelo.

`$ docker model run ai/smollm2`

2) Lanzar la instrucción para dejar un modelo pre-cargado en el *background* (`--detach`), para maximizar el rendimiento para llamadas subsecuentes al evitar la penalización de carga en disco duro a RAM persistente.

`$ docker model run --detach ai/smollm2`

Las caracteristicas de uso de `docker model` se pueden ver en [Docker Model Reference](https://docs.docker.com/reference/cli/docker/model/). Algunos comandos interesantes son:

`$ docker model list`: que permite ver la lista de modelos locales

`$ docker model logs <nombre_modelo>`: que permite ver los logs del modelo para debugging (respuestas, tiempo de genracion de respuesta, etc..)

`$ docker model rm <nombre_modelo>`: que permite eliminar el modelo



## Parte 2: Integración WebUI (Docker Compose)

Crea y levanta la aplicacion web de IA **Open WebUI** mediante el manifiesto `docker-compose.yml` adjunto:

1) Despliega la interfaz basándote en la imagen de contenedor `ghcr.io/open-webui/open-webui:main`.

2) Mapea la interfaz externa al puerto portuario `3000`.

3) Configura las variables de entorno necesarias para desactivar la autenticación de múltiples usuarios (`WEBUI_AUTH=false`) e indicar que el endpoint LLM se encuentra en la API de Docker: `http://host.docker.internal:12434`.

4) Enlaza el router interno a tu host con una resolución para Linux/Desktop usando `extra_hosts` y el atajo reservado `host-gateway`.

5) Verificación gráfica general:
Arranca la  ` $ docker-compose up -d`.
Accede por tu navegador a `http://localhost:3000`. En la interfaz, despliega la lista global en la parte super-izquierda (`Select a model`), deberías ver el agente de IA que Docker ya tiene listo (`ai/smollm2`). ¡Inicia el chat!

6) modificamos el docker compose para que utilice varios modelos y se descarguen al iniciar:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:12434
      - WEBUI_AUTH=false
      - DEFAULT_MODELS=ai/llama3.2
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data
    depends_on:
      model-setup:
        condition: service_completed_successfully

  model-setup:
    image: docker:cli
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: >
      sh -c "
        docker model pull ai/llama3.2 &&
        docker model pull ai/qwen2.5-coder &&
        docker model pull ai/smollm2
      "

volumes:
  open-webui:
```

7) cambia la configuracion de los modelos (temperatura y contexto) y vuelve a ejecutar el docker compose. Consulta las opciones disponibles [DMR Opciones de configuracion](https://docs.docker.com/ai/model-runner/configuration/). Compara los resultados con los anteriores.