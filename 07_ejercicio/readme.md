# Ejercicio 7: Observabilidad Completa (Host + Contenedores) con Node Exporter y cAdvisor

## Contexto Operativo
En infraestructuras de IT, la **Visibilidad** es el primer paso para garantizar la seguridad y la continuidad del servicio. Un sistema que no se monitoriza es un sistema comprometido en potencia.

El objetivo de este laboratorio es desplegar un stack de observabilidad completo (Prometheus + Grafana + Node Exporter + cAdvisor + AlertManager). El sistema utilizara diversas aplicaciones de recoleccion de metricas de operaciones, una base de datos donde las almacenará, un sistema de visualización para interpretarlas y un sistema de disparo de alarmas en funcion de reglas definidas sobre las metricas.

El diagrama total de la infraestructura desplegada puede verse en la siguiente figura:

![image](https://blog.nashtechglobal.com/wp-content/uploads/2025/12/82630796-10899900-9bf4-11ea-8815-5a373c604b6c.png)

Los agentes que monitorizan las metricas requieren dar acceso al Host a un contenedor (`node-exporter` y `cAdvisor`), esto abre una brecha de seguridad potencial. El reto es cerrar esa brecha aplicando **Hardening Estricto**.

En ejercicios anteriores monitorizamos la infraestructura de red a nivel de Sistema Operativo Host utilizando **Node Exporter**. Sin embargo, en un entorno de microservicios, necesitamos visibilidad profunda y analítica *dentro* del motor de contenedores para conocer qué contenedor consume CPU, cuál tiene fugas (*leaks*) de memoria y cuánto I/O genera cada servicio. 


## Arquitectura 

### Componentes
1.  **Node Exporter (Sensor de Máquina Base)**: Lee `/proc` y `/sys` del Host. Un contenedor con acceso al sistema de archivos raíz puede ser usado para escalar privilegios e implica un riesago de seguridad. Para ello hacemos los montajes de **Solo Lectura (:ro)** y eliminamos todas las capacidades (`cap_drop: ALL`).
2.  **cAdvisor (Sensor de Contenedores)**: Monitorea el `Runtime/Docker Engine`. Al ser un agente de bajo nivel requiere tambien el montaje de volumenes, parseo de sockets y Cgroups en modo lectura (`:ro`).
3.  **Prometheus (Cerebro Recolector)**: Configurado en su YAML para realizar *scraping* automático tanto de las métricas Host y de Contenedores.
4.  **Grafana (Visualización)**: Panel de control de Inteligencia en tiempo de ejecución.
5.  **AlertManager (Gestión de Alertas)**: Recibe alertas de Prometheus y las envía a diferentes destinos (Slack, Email, PagerDuty, etc.).

## Construcción de la solución (docker-compose.yml)

El fichero `docker-compose.yml` incluido implementa las siguientes medidas de fiabilidad operativa (SRE - Site Reliability Engineering) y Seguridad:

### 1. Prometheus
El servicio de Prometheus se configura para recolectar métricas de los diferentes agentes. Se le asigna un volumen para persistir las métricas y se configura el logging para que no ocupe más de 5 archivos de 100MB cada uno.
Las metricas se recogen en un volumen gestionado internamente por docker. Los ficheros de configuracion de prometheus y las reglas de alertas se montan como solo lectura.

```yaml
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./prometheus/rules.yml:/etc/prometheus/rules.yml:ro
      - prometheus_data:/prometheus
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "100m"
```
La red interna para que se conecten todos los contenedores es ```monitoring_net```. Conectamos `prometheus` a esta red, por lo que cualquier contenedor podra encontrarle en ```prometheus:9090```. Tambien le asignamos recursos limitados por seguridad.

```yaml
    networks:
      - monitoring_net
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```
La instruccion extra_hosts es la instrucción de Docker Compose equivalente a editar manualmente el archivo /etc/hosts dentro de un sistema Linux:

```yaml
    extra_hosts:
      - "host.docker.internal:host-gateway"
```
No afecta a cómo se resuelve la IP del contenedor de Prometheus en la red de Docker, sino a cómo Prometheus resuelve una dirección externa. En este caso, permite que Prometheus resuelva el nombre de host `host.docker.internal` como la IP de la máquina host. Esto es útil para que Prometheus pueda recolectar métricas de otros servicios que se ejecutan en la máquina host pero no dentro de un contenedor en la red de Docker.

### 2. Node Exporter

Se despliega de forma segura, sin mapear el puerto 9100 al host, con montajes de solo lectura y sin capacidades.

```yaml
node-exporter:
  cap_drop:
    - ALL
  expose:
    - 9100
  volumes:
    # CRÍTICO: El flag ':ro' asegura que el contenedor NO pueda modificar 
    # archivos del sistema operativo anfitrión.
    - /proc:/host/proc:ro,rslave
    - /sys:/host/sys:ro,rslave
    - /:/rootfs:ro,rslave
```
Y restringiendo el acceso a los recursos. En entornos críticos, un sistema de monitorización no puede tumbar la producción.

```yaml
deploy:
  resources:
    limits:
      cpus: '0.1'     # Node exporter es ligero, no necesita más
      memory: 64M     # Si consume más, hay un leak o ataque, mejor matarlo
```
Adicionalmente, se anexa el Job en ```prometheus/prometheus.yml``` para interpelar a ```node-exporter:9100```.

### 3. cAdvisor
A este contenedor le cuesta un tiempo arrancar, por lo que se le da un poco más de recursos. A nivel Docker, cAdvisor es muy voraz leyendo metadatos. Se le debe denegar la escritura a nivel root por diseño seguro.

Exponemos al host el puerto 8080 para poder acceder a la interfaz de cAdvisor y ver los datos en crudo que sirve.

```yaml
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.49.0
    container_name: cadvisor_monitor
    # Los montajes de solo lectura (:ro) protegen al Daemon del Host y rootfs
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    ports:
      - "8080:8080"
```

Adicionalmente, se anexa el Job en ```prometheus/prometheus.yml``` para interpelar a ```cadvisor:8080```.

### 4. Grafana
Se gestionan de forma adecuada los secretos de acceso a la aplcicación. Las credenciales de Grafana no están en el YAML, sino en un fichero `.env` que no se sube al repositorio (se ignora en .gitignore).

### 5. AlertManager
Se ha añadido el servicio de AlertManager para el envío de notificaciones.
La configuración para enviar los correos se ha de modificar en el fichero `alertmanager/alertmanager.yml`. Para que el envío funcione correctamente hacia `user@gmail.com`, se debe de reemplazar en ese archivo los campos `auth_username`, `auth_password` (se recomienda usar Contraseñas de Aplicación de Google) y enviar desde la cuenta de `gmail`. Además, las reglas de disparo se han centralizado en `prometheus/rules.yml` listando alertas básicas.

## Test de verificación del funcionamiento

Para verificar que el sistema es robusto y seguro:

1.  **Despliegue General:**
    Construye y levanta la topología con `docker compose up -d` (usa el fichero `.env`).
    
2.  **Verificar Flujo de Métricas (Prometheus):**
    Accede a `http://localhost:9090/targets`.
    *   *Estado Esperado*: Todos los endpoints deben estar en estado **UP**.
    *   *Prueba de Query*: Ejecuta `up` en la caja de búsqueda. Resultado: `1`.

3.  **Auditoría de Solo Lectura (Node Exporter):**
    Intenta escribir en el sistema de archivos del host desde el contenedor.
    ```bash
    docker exec -it host_monitor touch /rootfs/etc/hacked
    ```
    *Resultado Esperado*: `Read-only file system`.

4.  **Verificar Grafana:**
    Accede a `http://localhost:3000`.
    *   Usa las credenciales definidas en el fichero `.env`.
    *   Configura el datasource de Prometheus. La URL es `http://prometheus:9090` porque grafana y prometheus están en la misma red.
    *   En Dashboards-> New-> Import, importa el Dashboard ID **1860** ([Node Exporter Full](https://grafana.com/grafana/dashboards/1860-node-exporter-full/)) para ver los datos. Tambien importa el Dashboard ID **19908** ([cAdvisor Docker Insights](https://grafana.com/grafana/dashboards/19908-docker-container-monitoring-with-prometheus-and-cadvisor/)) para ver los datos.

5.  **Auditoría de cAdvisor en Crudo (Web UI Local):**
    cAdvisor tiene interfaz web embebida. Abre el navegador en: `http://localhost:8080`. Navega a la vista "*Docker Containers*" integrada.

6.  **Testear Integración Final con Prometheus:**
    Accede a Prometheus: `http://localhost:9090/targets` y confirma que `cadvisor` y `node_exporter` se encuentran conectados (*State: UP*). 
    Puedes probar una metrica en PromQL como por ejemplo: `container_cpu_usage_seconds_total` y verás que se muestran todas las metricas de uso de CPU que esta recibiendo prometheus.
    Prueba en `http://localhost:9090/alertmanager-discovery` que se ha detectado el servicio de AlertManager. 

7.  **Representación Visual en Grafana:**
    Conéctate a Grafana (`http://localhost:3000`), vincula el origen de datos de Prometheus (URL http://prometheus:9090) e importa el Template Dashboard oficial **14282** (o bien **193** "Docker monitoring") desde Grafana Labs para presenciar los datos enriquecidos.

8.  **Auditoría de AlertManager y Notificaciones:**
    *   Navega a Prometheus `http://localhost:9090/alerts`. Comprobarás que las reglas importadas (como `InstanciaCaida`) están en estado verde (*Inactive*).
    *   Verifica que la web de AlertManager está accesible en `http://localhost:9093`.
    *   Simula un fallo deteniendo un agente de monitorización de forma manual: `docker stop host_monitor`.
    *   Espera cerca de 1 minuto y observarás en Prometheus cómo la alerta cambia a *Pending* y posteriormente a *Firing*. En ese instante el disparo pasa a Alertmanager, que tratará de enrutar la notificación SMTP por email a `[EMAIL_ADDRESS]` usando la configuración que introdujiste en el YAML de alertmanager.
    *   (Restablece la alerta iniciando el servicio con `docker start host_monitor`).
