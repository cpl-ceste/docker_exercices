# Ejercicio 09: Monitorización de Infraestructura Crítica (SRE & Security)

## Contexto Operativo
En infraestructuras de defensa, la **Visibilidad** es el primer paso para la seguridad. Un sistema que no se monitoriza es un sistema comprometido en potencia.

El objetivo de este laboratorio es desplegar un stack de observabilidad (Prometheus + Grafana + Node Exporter) que sea capaz de recolectar métricas del Host (CPU, Memoria, Red) y del motor de Docker. Sin embargo, al dar acceso al Host a un contenedor (`node-exporter`), abrimos una brecha de seguridad potencial enorme. El reto es cerrar esa brecha aplicando **Hardening Estricto**.

## Arquitectura Segura

### Componentes
1.  **Node Exporter (Sensor)**: Debe leer `/proc` y `/sys` del Host.
    *   *Riesgo*: Un contenedor con acceso al sistema de archivos raíz puede ser usado para escalar privilegios.
    *   *Mitigación*: Montajes de **Solo Lectura (:ro)** y eliminación de todas las capacidades (`cap_drop: ALL`).
2.  **Prometheus (Cerebro)**: Recolecta las métricas.
    *   *Persistencia*: Utiliza volúmenes Docker para no perder histórico.
    *   *Configuración*: Inyectada vía volumen (Simulando ConfigMap).
3.  **Grafana (Visualización)**: Dashboard para el operador.
    *   *Seguridad*: Credenciales inyectadas vía variables de entorno (`.env`), nunca hardcoded.

## Construcción de la solución (docker-compose.yml)

El fichero `docker-compose.yml` incluido implementa las siguientes medidas de SRE y Seguridad:

### 1. Hardening de Node Exporter
```yaml
node-exporter:
  # ...
  # Aislamiento de Red: Usamos 'host' para ver las interfaces reales, 
  # pero al ser solo lectura y sin capabilities, reducimos el vector de ataque.
  network_mode: host 
  pid: host
  volumes:
    # CRÍTICO: El flag ':ro' asegura que el contenedor NO pueda modificar 
    # archivos del sistema operativo anfitrión.
    - /proc:/host/proc:ro,rslave
    - /sys:/host/sys:ro,rslave
    - /:/rootfs:ro,rslave
```

### 2. Límites de Recursos (Deploy Resources)
En entornos críticos, un sistema de monitorización no puede tumbar la producción.
```yaml
deploy:
  resources:
    limits:
      cpus: '0.1'     # Node exporter es ligero, no necesita más
      memory: 64M     # Si consume más, hay un leak o ataque, mejor matarlo
```

### 3. Gestión de Secretos
Las credenciales de Grafana no están en el YAML, sino en un fichero `.env` que no se sube al repositorio (se ignora en .gitignore).

## Check de Auditoría

Para verificar que el sistema es robusto y seguro:

1.  **Verificar Flujo de Métricas (Prometheus):**
    Accede a `http://localhost:9090/targets`.
    *   *Estado Esperado*: Todos los endpoints deben estar en estado **UP**.
    *   *Prueba de Query*: Ejecuta `up` en la caja de búsqueda. Resultado: `1`.

2.  **Auditoría de Solo Lectura (Node Exporter):**
    Intenta escribir en el sistema de archivos del host desde el contenedor.
    ```bash
    docker exec -it host_monitor touch /rootfs/etc/hacked
    ```
    *Resultado Esperado*: `Read-only file system`.

3.  **Verificar Grafana:**
    Accede a `http://localhost:3000`.
    *   Usa las credenciales definidas en tu fichero `.env`.
    *   Configura el datasource de Prometheus. La URL es `http://prometheus:9090` porque grafana y prometheus están en la misma red.
    *   Importa el Dashboard ID **1860** (Node Exporter Full) para ver los datos.
