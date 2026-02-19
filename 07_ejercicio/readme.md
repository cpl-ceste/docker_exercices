# Ejercicio 07: Análisis de Tráfico Seguro con Suricata (Capabilities)

## Contexto de Ciberdefensa
Necesitamos desplegar **Suricata**, un sistema de detección de intrusiones (IDS) de alto rendimiento, junto con **EveBox** para visualizar las alertas.

Nos inspiramos en la solucion publicada en este repo https://github.com/upmcplanetracker/test-suricata. Es importante conocer el interfaz de red de la máquina host para configurar correctamente el contenedor de Suricata. En mi caso es `eth0`. Para conocer el interfaz de red de la máquina host se puede usar el comando `ip a` o `ifconfig`. Tambien es importante considerar que EveBox se expone en un puerto `https` y que el usuario de acceso y la password se muestran en los logs de arranque del contenedor.

El desafío es que Suricata requiere privilegios elevados para interceptar tráfico de red (`NET_ADMIN`), pero por política de seguridad de la empresa **NO PODEMOS** otorgar acceso `root` completo al host (`privileged: true`) ya que esto permitiría escapar del contenedor fácilmente.

## El Objetivo
Configura un `docker-compose.yml` que levante la pila Suricata + EveBox + un generador de tráfico (ej. Alpine con curl) cumpliendo:

1.  **Capabilities Granulares**: Otorga a Suricata SOLO las capacidades de Linux necesarias para gestionar la red. NUNCA uses `privileged: true`.
2.  **Límites de Recursos**: Protege el host contra denegación de servicio (DoS) limitando la CPU y RAM que Suricata puede consumir.
3.  **Aislamiento de Componentes**: EveBox (la interfaz web) debe tener su sistema de archivos en **Solo Lectura** y no debe tener ninguna capability extra.
4.  **Least Privilege entre Servicios**: EveBox debe poder leer los logs de Suricata, pero Suricata no debe poder escribir en la configuración de EveBox.

## Trabajo Técnico
- **Capabilities**: Investigamos `cap_add` con `NET_ADMIN`, `NET_RAW` y `SYS_NICE` (https://docs.docker.com/reference/cli/docker/container/run/#runtime-privilege-and-linux-capabilities)(https://medium.com/@ghabrimouheb/mastering-linux-kernel-capabilities-with-docker-your-guide-to-secure-containers-8070b174c000).
- **Docker Compose Limits**: Revisa la sección `deploy: resources:` de la versión 3 (https://docs.docker.com/compose/compose-file/deploy/).
- **Volúmenes**: Diferencia entre volúmenes de lectura/escritura (`rw`) y solo lectura (`ro`) (https://docs.docker.com/storage/volumes/).

## Construccion de la solución

Revisa el archivo `docker-compose.yml` en este directorio. Presta especial atención a:

*   **`cap_add: [NET_ADMIN, NET_RAW]`**: Estas son las llaves mínimas para que funcione el IDS sin abrir todas las puertas.
*   **`read_only: true` en EveBox**: Si comprometen la web de EveBox, el atacante no podrá persistir malware en el disco del contenedor.
*   **`deploy.resources.limits`**: Si Suricata se vuelve loco procesando tráfico, no tumbará el servidor host (Docker matará el proceso si excede 512MB RAM).

## Test de Verificación

1.  **Levantar el stack:**
    ```bash
    docker compose up -d
    ```

2.  **Verificar Capabilidades de Suricata (Debe tener solo las necesarias):**
    ```bash
    docker exec suricata_ids capsh --print
    ```
    *Busca `cap_net_admin` y `cap_net_raw` en "Effective capabilities".*

3.  **Verificar que EveBox es Read-Only:**
    ```bash
    docker exec evebox_ui touch /test_file
    ```
    *Resultado esperado: Read-only file system*

4.  **Verificar Alertas (EveBox):**
    Abre en tu navegador `http://localhost:5636`. Deberías ver eventos generados por el contenedor `bad_actor` haciendo peticiones.

5.  **Verificar que Suricata tiene las capacidades necesarias:**
    ```bash
    docker exec suricata_ids capsh --print
    ```
    *Busca `cap_net_admin` y `cap_net_raw` en "Effective capabilities".*
