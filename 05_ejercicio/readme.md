# Ejercicio 05: Despliegue de Honeypot Seguro (Seguridad en Docker)

## Contexto de Ciberdefensa
Tu equipo de Blue Team quiere desplegar un **Honeypot Web** de baja interacción para detectar escaneos y ataques automatizados dentro de la red interna. La aplicación simula ser un portal de facturación interno antiguo y vulnerable.

Sin embargo, si el honeypot se compromete en algun ataque, no queremos que sirva de plataforma de salto para atacar la red real. Por tanto, el contenedor debe estar **extremadamente endurecido (hardened)**.

## El Objetivo: Hardening Básico
Debes crear una imagen de Docker para la aplicación (ubicada en `app/`) que cumpla con los siguientes requisitos de seguridad **obligatorios**:

1.  **Principio de Mínimo Privilegio**: El contenedor NO debe ejecutarse como root.
2.  **Usuario Específico**: Debes crear un usuario y grupo específicos para la aplicación dentro de la imagen.
3.  **Puertos Altos**: La aplicación debe escuchar en un puerto no privilegiado (mayor a 1024).

Además, al ejecutar el contenedor, debes aplicar las siguientes restricciones en tiempo de ejecución (runtime):
4.  **Sistema de Archivos de Solo Lectura**: El contenedor debe de mapear el sistema de archivos de la app pero no debe de poder escribir en ninguna parte de su sistema de archivos, excepto, si fuera necesario, en directorios temporales específicos.
5.  **Limitar Capacidades (Capabilities)**: El contenedor debe de eliminar TODAS las capacidades de Linux y no añadir ninguna.

## Trabajo Técnico
Vamos a investigar sobre las siguientes opciones para fortalecer la seguridad de los contenedores:
- **Dockerfile USER**: Investiga la instrucción `USER` en Dockerfile (https://docs.docker.com/reference/cli/docker/container/run/#read-only).
- **Root Filesystem Read-Only**: Busca el flag `--read-only` de `docker run`.
- **Capabilities**: Investiga sobre `--cap-drop` y `--cap-add` (https://docs.docker.com/engine/containers/run/#runtime-privilege-and-linux-capabilities) para eliminar todas las capacidades de Linux y no añadir ninguna.
- **Privilegios de ejecucion**: Investiga sobre `--security-opt` (https://docs.docker.com/reference/cli/docker/container/run/#security-opt) para deshabilitar que los procesos del contenedor puedan obtener mas privilegios.

## Construccion de la solución

### 1. El Dockerfile Seguro
Revisa el archivo `Dockerfile` en este directorio, donde se han incluido comentarios explicativos paso a paso.

### 2. Comando de Ejecución Seguro (Runtime Hardening)
Una vez construida la imagen, el comando para ejecutarla de forma segura es el siguiente:

1.  **Construir la imagen:**
    ```bash
    docker build -t secure-honeypot .
    ```

2.  **Ejecutar con Hardening:**
    ```bash
    docker run -d \
      --name honeypot-v1 \
      -p 8080:8080 \
      --read-only \
      -v $(pwd)/app:/app:ro \
      --tmpfs /tmp \
      --cap-drop=ALL \
      --security-opt=no-new-privileges \
      secure-honeypot
    ```

    **Explicación de los flags:**
    *   `--read-only`: Monta el sistema de archivos raíz del contenedor como de solo lectura. Si un atacante entra, no podrá descargar herramientas, modificar scripts ni borrar logs en disco.
    *   `--tmpfs /tmp`: Como Python/Flask puede necesitar escribir archivos temporales, montamos `/tmp` en memoria (RAM), lo cual es rápido y desaparece al reiniciar.
    *   `--cap-drop=ALL`: Elimina todas las capacidades del kernel de Linux (como `CHOWN`, `NET_ADMIN`, etc.). Un proceso web simple no necesita ninguna.
    *   `--security-opt=no-new-privileges`: Impide que el proceso gane privilegios adicionales (ej. vía `setuid`) durante la ejecución.

## Test de Verificación

Para comprobar que el contenedor es seguro, intenta ejecutar estos comandos “atacantes”:

1.  **Verificar usuario (Debe ser diferente de root/uid 0):**
    ```bash
    docker exec honeypot-v1 id
    ```
    *Resultado esperado: uid=100 (appuser) gid=101 (appgroup)*

2.  **Intentar escribir un archivo (Debe fallar):**
    ```bash
    docker exec honeypot-v1 touch /app/hacked.txt
    ```
    *Resultado esperado: touch: /app/hacked.txt: Read-only file system*

3.  **Verificar Capabilities (Debe estar casi vacío):**
    ```bash
    docker exec honeypot-v1 grep CapEff /proc/1/status
    ```
    *Resultado esperado: CapEff: 0000000000000000*
    
4.  **Intentar cambiar la fecha (Debe fallar):**
    ```bash
    docker exec honeypot-v1 date +%T -s “08:08:08"
    ```
    *Resultado esperado: date: cannot set date: Operation not permitted*

