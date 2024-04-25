# EJERCICIO 5 - DOCKER COMPOSE

Documentacion de referencia:
- [Docker Docs](https://docs.docker.com/)
- [Docker Compose Manual](https://docs.docker.com/compose/)


## Levantar una aplicacion web con multiples contenedores

Normalmente las aplicaciones se modularizan en diferentes contenedores. En general, cada contenedor debe de especializarse en hacer una cosa y hacerla bien. Las siguientes son algunas razones para ejecutar el contenedor por separado:

- Es muy probable que tengas que escalar las APIs y las webs de forma diferente a las bases de datos.
- Los contenedores separados nos permiten versionar y actualizar versiones de forma aislada.
- Si bien se puede utilizar un contenedor para la base de datos localmente, es posible que desee utilizar un servicio administrado para la base de datos en producción. Entonces no querremos publicar el motor de base de datos con la aplicación en la misma imagen.
- La ejecución de múltiples procesos en un mismo contenedor requerirá un administrador de procesos (el contenedor solo inicia un proceso), lo que agrega complejidad al inicio/apagado del contenedor.

Y hay más razones. Entonces, como en el siguiente diagrama, es mejor ejecutar su aplicación en varios contenedores.

Para levantar una aplicación con multiples contenedores podemos ejecutarlos individualmente y conectarlos o utilizar Docker Compose.

### Ejecutar una aplicacion web con base de datos

Tenemos una aplicacion web que se ejecuta en node y tiene una configuracion interna en la que si queremos puede conectarse a una base de datos.

![image](https://docs.docker.com/get-started/images/multi-container.webp?w=350h=250)

Ejecutaremos primero a aplicacion sola y la ejecutaremos conectandola a otro contenedor MySQL

1) Navegamos hasta el dir `/app` y ejecutamos un contenedor con node en el que mapeamos nuestro volumen con la aplicacion web y la construimos con `yarn`

`$ docker run -dp 127.0.0.1:3000:3000 \
  --rm \
  -w /app -v "$(pwd):/app" \
  node:18-alpine \
  sh -c "yarn install && yarn run dev"`

Ver los logs, le cuesta un ratito levantar
Creamos algunos `todos` en la aplicacion

2) Paramos el contendor y la modificamos cambiando en el fichero `src/static/js/app.js` la linea 56 como sigue:

`- <p className="text-center">No items yet! Add one above!</p>`

`+ <p className="text-center">You have no todo items yet! Add one above!</p>`

3) Volvemos a ejecutarla para ver los cambios

`$ docker run -dp 127.0.0.1:3000:3000 \
  --rm \
  -w /app -v "$(pwd):/app" \
  node:18-alpine \
  sh -c "yarn install && yarn run dev"`

Vemos que hemos actualizado la aplicacion web pero los `todos` anteriores no se han guardado.
La aplicacion guarda los datos en un fichero interno y este desaparece cada vez que reiniciamos el contenedor.
Puede guardar los datos en una base de datos mysql porque la aplicacion viene preparada para conectarse a una.

4) Vamos a levantar otro contenedor de MySQL y a conectarlos para tener una aplicacion multicontendor completa

- Primero creamos una red
`$ docker network create todo-app`

- Luego levantamos un contendor mysql en esa red

`$ docker run -d \
    --name mysql_container \
    --network todo-app --network-alias mysql \
    -v todo-mysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=1234 \
    -e MYSQL_DATABASE=todos \
    mysql:8.0`

- Posteriomente nos conectamos a ese contenedor, ejecutamos el comando mysql para acceder a la base de datos. 

`$ docker exec -it mysql_container mysql -u root -p`

- Listamos las Bases de Datos y salimos
`mysql> SHOW DATABASES;`
`mysql> EXIT;`

- Finalmente y para ver como se ha levantado en la red, vamos a usar un contenedor que tiene una serie de herramientas de red entre ellas el comando `dig` para resolver nombres de dominio en la red

`$ docker run -it --network todo-app nicolaka/netshoot`

Y ejecutamos el comando:

`$ dig mysql`

y vemos que en el DNS de la red se resuelve ok este nombre de dominio, que es un registro de DNS de tipo ALIAS A para el nombre -> mysql. Asi que no hace falta que usemos la ip de la red para conectarnos a la Base de Datos desde otro contenedor, usaremos el alias

5) Ahora levantamos nuestra aplicacion web añadiendo las variables de entorno que tiene configuradas para conectarse a una base de datos MySQL. En nuestro caso nos conectamos al contenedor de MySQL que tenemos en la red el host de conexion es el Alias de la maquina en la red (la direccion del host es nuestro alias mysql).

`$ docker run -dp 127.0.0.1:3000:3000 \
  -w /app -v "$(pwd):/app" \
  --network todo-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=1234 \
  -e MYSQL_DB=todos \
  node:18-alpine \
  sh -c "yarn install && yarn run dev"`

- Comprobamos el funcionamiento de la aplicacion. Vemos los logs de la aplicación, porque le cuesta un ratito levantar
Metemos algunos todos

- Nos conectamos a la base de datos todo y vemos la tabla todo_items
`$ docker exec -it mysql_container mysql -p todos`

`select * from todo_items`

5) Borramos los contenedores, volumenes y redes


## Levantamos la aplicacion web con base de datos con docker compose

Docker Compose es un plug-in de Docker, una herramienta que nos ayuda a definir y compartir aplicaciones de múltiples contenedores. Con Compose, podemos crear un archivo YAML que contiene toda la definicion de los servicios y con un solo comando, podemos activar o desactivar toda esa definición.

Esta definición puede entenderse como infraestructura como codigo IaaC, porque tenemos un archivo declarativo YAML que hace que Docker cree imagenes, levante conetnedores, volumenes y redes, los comunique, etc... con un solo comando en Docker Compose.

La gran ventaja de usar Compose es que puede definir todo el stack de nuestra aplicación en un solo archivo, mantenerlo en la raíz del repositorio de nuestro proyecto (ahora tiene control de versión) y permitir fácilmente que otra persona contribuya a nuestro mismo proyecto. Alguien sólo necesitaría clonar nuestro repositorio e iniciar la aplicación usando Compose. De hecho, es posible que veas bastantes proyectos en GitHub/GitLab haciendo exactamente esto ahora.

1)  Navegamos al directorio `/app` y abrimos el fichero `compose.yaml`

Analizamos las partes del fichero y lo comparamos con el despliegue que hemos hecho en la actividad anterior, ¿que similitudes y diferencias observamos?

2) Levantamos la aplicacion en modo dettached con el comando `$ docker compose up -d`

Inspeccionamos los contenedores

3) Probamos otros comandos de docker compose donde podemos trabajar con los contenedores individuales, identificados por el nombre del `service` que hemos definido en el fichero `compose.yaml`:

`$ docker compose ps`

`$ docker compose stop <service>`

`$ docker compose start <service>`

`$ docker compose logs <service>`

3) Ejecutamos el comando para borrar los contenedores y borramos redes y volumenes que queden sin borrar

`$ docker compose down`




