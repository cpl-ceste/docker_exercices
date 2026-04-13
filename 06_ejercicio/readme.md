# Ejercicio 6: Entorno de Desarrollo para Aplicación Web Java (PetClinic)

## Descripción del problema
En este ejercicio resolvemos el reto técnico de configurar un entorno de desarrollo local completo para una aplicación web compleja (como Spring PetClinic en Java) utilizando `docker-compose`. En lugar de construir una imagen en cada cambio de código (lo cual es lento para el ciclo de desarrollo), el contenedor puede actuar como nuestro "entorno de ejecución". Para ello, ejecutaremos la aplicación directamente desde el código fuente de nuestra máquina mediante un volumen y utilizaremos un contenedor extra para la base de datos (MySQL). Esto facilita el desarrollo iterativo ("live-reload") y evita que tengamos que instalar Java, Maven o MySQL directamente en nuestra máquina.

## Pasos técnicos necesarios
* **Imágenes de desarrollo:** Para Spring Boot 3 / PetClinic, una imagen con JDK 17 (por ejemplo, `eclipse-temurin:17-jdk-jammy`) es ideal para tener las herramientas de compilación disponibles en el contenedor.
* **Volúmenes tipo Bind (Bind Mounts):** Necesitamos montar el directorio actual de nuestra máquina `.` al directorio de trabajo dentro del contenedor (por ejemplo, `/app`). Esto asegura que cuando modifiquemos código en nuestro editor, el contenedor lo vea al instante.
* **Caché de dependencias:** Para evitar que Maven o Gradle descarguen todo el Internet cada vez que se levanta el contenedor, utilizamos un volumen persistente mapeado al directorio donde se guardan las dependencias (`/root/.m2` para Maven).
* **Comando de arranque:** Debemos sobreescribir el `CMD` o `command` del contenedor de la aplicación para que ejecute la aplicación en modo desarrollo. En el caso de Spring Boot con el wrapper de Maven, sería `./mvnw spring-boot:run`.
* **Conexión entre contenedores:** Configuramos las variables de entorno de la base de datos (ej: `spring.datasource.url` en Java) para conectarse a través del nombre de servicio en la red de Compose (ej: `db`), y no a través de `localhost`.
* **Codigo fuente:** El desarrollador dispone de un codigo sobre el que esta trabajando, que en este caso descargaremos del repositorio oficial de GitHub: https://github.com/spring-projects/spring-petclinic.git

*Nota para el despliegue:* Para probar correctamente este archivo, se debe ubicar en la carpeta raíz del repositorio oficial clonado de `spring-petclinic`.

```bash
git clone https://github.com/spring-projects/spring-petclinic.git```

**NOTA IMPORTANTE**: Poner el fichero `docker-compose.yaml` dentro del directorio `spring-petclinic` que se habra creado despues de hacer el pull del repo y ejecutar `docker compose desde este directorio `spring-petclinic` para que el mapeo de volumenes sea correcto y arranque bien la aplicacion web de Spring Boot. 


## Test de Verificación
Una vez creado el `docker-compose.yml` movernos a la carpeta raíz del proyecto (`/spring-petclinic`), y en el terminal ejecutamos los comandos para levantar la aplicacion:

```bash
docker-compose up -d
```

Para comprobar que todo está bien configurado y el proyecto ha descargado sus librerías e iniciado sin errores, ejecutamos el monitoreo de los logs:

```bash
docker-compose logs -f web
```
*(Debemos buscar en los logs una frase similar a: `Started PetClinicApplication in XX seconds`)*.

Finalmente, si accedemos con nuestro navegador a:
**[http://localhost:8080/](http://localhost:8080/)** 
deberíamos ver la aplicación Spring PetClinic funcionando y conectada sin problemas.

Podemos modificar la aplicación en nuestro editor local y verificar que nuestro entorno de desarrollo funciona correctamente.
