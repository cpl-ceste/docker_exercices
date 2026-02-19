# Ejercicio 08: Despliegue de Mini-SIEM Seguro (Resource Limits & Network Segmentation)

## Contexto de Ciberdefensa
Tu organización requiere un **SIEM (Security Information and Event Management)** ligero para correlacionar logs de seguridad. Has elegido **Wazuh**.

Al ser una aplicación basada en Java y ElasticSearch (OpenSearch), Wazuh es propenso a consumir toda la RAM disponible en el servidor si no se controla, provocando un fallo general (DoS accidental). Además, la base de datos de índices contiene información sensible de seguridad y **NUNCA** debe estar expuesta directamente a la red de usuarios ni a Internet.

## El Objetivo
Diseñamos un `docker-compose.yml` para desplegar Wazuh (Indexer + Manager + Dashboard) cumpliendo estrictamente con:

1.  **Prevención de Resource Exhaustion**:
    *   Configura límites duros (`limits`) de memoria RAM para cada contenedor.
    *   Limita la memoria del heap de Java (`-Xms/-Xmx`) para que coincida con los límites del contenedor y evitar que el proceso sea matado por el OOM Killer del kernel de forma inesperada.

2.  **Segmentación de Red (Network Sandboxing)**:
    *   Crea una red **backend** interna donde residan el Indexer y el Manager. Esta red **NO** debe ser accesible desde el exterior.
    *   Crea una red **public** donde solo esté el Dashboard (puerto 443).
    *   El Manager debe tener doble interfaz: una interna para hablar con la base de datos y una externa para recibir logs de los agentes.

## Trabajo Técnico
*   **Docker Compose Networks**: Investigamos `internal: true` (https://docs.docker.com/reference/compose-file/networks/#internal).
*   **JVM Flags**: Buscamos la variable de entorno `OPENSEARCH_JAVA_OPTS` (https://docs.wazuh.com/current/installation-guide/wazuh-indexer/tuning.html).
*   **OOM Killer**: ¿Qué pasa si le asignas 2GB de límite al contenedor pero la JVM intenta usar 4GB?

## Construccion de la solución

Revisa el archivo `docker-compose.yml` en este directorio. Observa cómo hemos definido las redes y los límites:

*   **Red `wazuh-backend-net`**: Definida con `internal: true`. Esto aísla completamente el tráfico de base de datos. Si un atacante entra en la red puente por defecto, no verá el puerto 9200 del indexer.
*   **`deploy.resources.limits.memory`**: Establecido en 1.5G para el indexer.
*   **Env `OPENSEARCH_JAVA_OPTS`**: `-Xmx512m` asegura que Java sepa que tiene un techo mucho antes de llegar al límite del contenedor, permitiendo un manejo de memoria más estable.

## Test de Verificación

1.  **Levantar el stack:**
    ```bash
    docker compose up -d
    ```

2.  **Verificar límites de memoria:**
    ```bash
    docker stats
    ```
    *Comprueba que la columna LIMIT muestre los valores configurados (ej. 1.5GiB) y no la memoria total de tu máquina.*

3.  **Verificar aislamiento de red (Desde otro contenedor):**
    Intenta conectar al puerto del Indexer (9200) desde un contenedor fuera de su red privada.
    ```bash
    docker run --rm --network wazuh-public-net alpine curl -v http://wazuh-indexer:9200
    ```
    *Resultado esperado: "Could not resolve host: wazuh-indexer" o timeout. El contenedor público no debería poder ver al backend privado.*
