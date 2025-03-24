# EJERCICIO 2 - CONTENEDORES: VOLUMENES Y RED

Documentacion de referencia [Docker Docs](https://docs.docker.com/)

## Contenedores: mapeo de volumenes

Docker permite que cuando se ejecuta un contenedor se puedan mapear volumenes de datos en los que el contenedor persiste los datos para que esten disponibles si se ejecuta de nuevo [Volumenes](https://docs.docker.com/storage/volumes/)

Creamos una aplicacion web lavantando una imagen de NGINX.

0) Navegamos al directorio `ngnix`

1) Conectarse a DockerHub desde Docker Desktop y VStudio Code

`$ docker run --name web-site -d -p 8080:80 nginx`

2) Abrir el navegador para ver la aplicacion

3) Para personalizar la aplicacion web, hay dos ficheros importantes: el index.html de nuestra aplicacion y el fichero de configuracion del servidor. Vamos a inspeccionarlos en los directorios del contenedor:
- /usr/share/nginx/html
- /etc/nginx/nginx.conf 

### Volumenes sin nombre

Creamos una aplicacion web lavantando una imagen de NGINX.

1) Conectarse a DockerHub desde Docker Desktop y VStudio Code

`$ docker run -dp 8080:80 -v /usr/share/nginx/html nginx`

2) Inspeccionamos el volumen y vemos que se han mapeado todos los contenidos del directorio del contenedor al volumen en nuestro host. Ver en Docker Desktop o en VStudio Code donde se ha creado el volumen y ver los ficheros. Podemos copiarlos o exportarlos a otro directorio

3) En los ficheros del contenedor sobre-escribir el `index.html` por defecto de nginx, con el nuevo `index.html` que viene en el dir `static-site2` de este ejercicio y comprobar en la web que se ha actualizado

4) Borrar el contenedor y vemos que el volumen hay que borrarlo manualmente. En VStudio pueden borrarse todos los volumenes sin nombre no asociados a ningun contenedor. En DockerDesktop pueden borrarse y exportarse los volumenes.

5) Arrancamos de nuevo el contendor y vemos que se crea otro volumen sin nombre diferente, los datos han persistido en el volumen anterior pero no estan en el nuevo. Observamos que en este caso la opcion --rm borra volumenes sin nombre (volumenes orfanos)

`$docker run --rm -dp 8080:80 -v /usr/share/nginx/html nginx`

6) Parar contenedor, vemos que se borra el contenedor y el volumen

### Volumenes con nombre

1) Conectarse a DockerHub desde Docker Desktop y VStudio Code

`$ docker run -dp 8080:80 -v my-vol:/usr/share/nginx/html nginx`

2) Inspeccionamos el volumen y vemos que se han mapeado todos los contenidos del directorio del contenedor al volumen en nuestro host. Ver en Docker Desktop o en VStudio Code donde se ha creado el volumen y ver los ficheros. Podemos copiarlos o exportarlos a otro directorio

3) En los ficheros del contenedor sobre-escribir el `index.html` por defecto de nginx, con el nuevo `index.html` que viene en el dir `static-site2` de este ejercicio y comprobar en la web que se ha actualizado

4) Borrar el contenedor y vemos que el volumen hay que borrarlo manualmente. En VStudio pueden borrarse manualmente los volumenes con nombre. En Docker Desktop pueden borrarse y exportarse los volumenes.

5) Arrancamos de nuevo el contendor y vemos que se utiliza el volumen con nombre, los datos han persistido y la web esta actualizada. Observamos que en este caso la opcion --rm no borra volumenes con nombre

`$docker run --rm -dp 8080:80 -v my-vol:/usr/share/nginx/html nginx`

6) Parar contenedor, vemos que se borra el contenedor pero no el volumen. Hay que borrarlo manualmente


### Mapeo de volumenes a directorios especificos del sistema (bind mounts)

Creamos una aplicacion web lavantando una imagen de NGINX.

1) Levantamos la aplicacion web mapeando un volumen en la ruta `static-site1` que es un directorio vacio. Creamos primero el directorio `static-site1`

`$ docker run -dp 8080:80 -v ./static-site1:/usr/share/nginx/html nginx`

NOTA IMPORTANTE: si le damos por equivocacion el nombre de un dir en el host o en el contenedor que no existen los creara vacios y no dara error. No despistarse, porque a veces nos equivocamos al escribir la rutas y los contenidos mapeados no coinciden con lo que pensamos. El comando `mount` no crea automaticamente estos directorios y por seguridad simplemente da un error.

2) en este caso vemos que no hay volumenes en DOCKER. Inspeccionamos el volumen y vemos que no se han mapeado todos los contenidos del directorio del contenedor al volumen en nuestro host. 

3) Navegamos a la aplicacion web y vemos que no hay `index.html` para mostrar por defecto. Vemos en los logs del contenedor un `403 forbidden` y en el dir del contenedor `/usr/share/nginx/html` se ha mapeado el directorio vacio de nuestro host

4) Borramos el contenedor y levantamos de nuevo la aplicacion web mapeando un volumen en la ruta `static-site2` que es el directorio con nuestra aplicacion web

`$ docker run -dp 8080:80 -v $(pwd)/static-site2:/usr/share/nginx/html nginx`

3) En los ficheros del contenedor vemos que se ha sobre-escribito el `index.html` por defecto de nginx, con el nuevo `index.html` que viene en el dir `static-site2` de este ejercicio y comprobar en la web que se ha actualizado

4) Navegamos a la pagina web y observamos los logs del servidor web en el contenedor

4) Borrar el contenedor y lo levantamos mapeando varios volumenes:

`$ docker run -dp 8080:80 -v $(pwd)/static-site2:/usr/share/nginx/html -v $(pwd)/nginx-conf/nginx.conf:/etc/nginx/nginx.conf nginx`

5) Observamos los logs del conendor y la pagina web de navegacion, ahora controlamos la configuracion del servidor y los contenidos de la web con los ficheros de nuestro directorio local. Podemos trabajar en desarrollo web.

6) Borramos el contenedor

7) Levantamos de nuevo la aplicacion web mapeando un volumen en la ruta `static-site2` que es el directorio con nuestra aplicacion web

`$ docker run -dp 8080:80 -v $(pwd)/static-site2:/usr/share/nginx/html nginx`

8) Entramos en los ficheros del contendor y modificamos el fichero `index.html`. Vemos que el contenido del directorio mapeado del contenedor esta sincronizado con el contenido del dir de nuestro host `static-site2` y los cambios hechos dentro del contenedor se reflejan en el fichero `index.html`del host. los dos directorios estan sincronizados

9) Borramos el contenedor

10) Para evitar que procesos internos del contenedor modifiquen los ficheros de los volumenes mapeados y por ende los ficheros del host podemos mapear los volumenes en modo `readonly`. Levantamos de nuevo la aplicacion web mapeando un volumen en modo `readonly`en la ruta `static-site2` que es el directorio con nuestra aplicacion web

`$ docker run -dp 8080:80 -v $(pwd)/static-site2:/usr/share/nginx/html:ro nginx`

11) Entramos en los ficheros del contendor y modificamos el fichero `index.html` vemos que esta en modo readonly y no podemos grabar los cambios.

12) Borramos el contenedor

### Mapeo de volumenes con un usuario especifico

En ocasiones el contenedor corre con un usuario que es diferente del usuario del host y es posible que no tenga permisos para utilizar el sistema de ficheros del sistema local. Podemos especificar que el usuario que corre en el contenedor sea el mismo que el usuario local para solucionar este problema

Crearemos un contenedor con DBMS de MySQL.

0) Crear un directorio `mysql`y en el, otros dos directorios vacios `dbms1`y `dbms2`

1) Navegamos al dir `mysql` creamos un dir `dbms1`, vemos el usuario propietario y nos vamos a el

`$ mkdir dbms1`

`$ ls -lnd dbms1`

`$ cd dbms1`

3) Corremos un contendor de MySQL con un mapeo de volumen, de forma que los datos de la base de datos se guarden en un dir local `data`. No hace falta que creemos el dir local, lo creara el contenedor cuando haga el mapeo.

`$ docker run -v $(pwd)/data:/var/lib/mysql -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=1234 -d mysql`

3) Vemos que el contenedor no logra arrancar, vemos los logs. Hay un problema de permisos para crear la base de datos en el dir local

4) Creamos otro dir nuevo en el raiz `02_ejercicio/mysql/dbms2` y nos vamos a el.

`$ cd ..`

`$ mkdir dbms2`

`$ cd dbms2`

5) Corremos el contenedor especificando que se ejecute con nuestro UID

`$ docker run -v $(pwd)/data:/var/lib/mysql -u 1000:1000 -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=1234 -d mysql`

6) Comprobamos si el contenedor arranca y le atachamos un shell para comprobar el id de usuario con el que ha arrancado

`$ id`

7) Nos conectamos a la base de datos con un cliente mysql y comprobamos que funciona


## Contenedores: Redes

Docker crea en los contenedores interfaces de red y les asigna una direccion IP. Si no se especifica la red en la quiere que se levanten cuando arrancan, se conectarán a la red predeterminada.

Tambien puede crearse una red y conectarlos a ella. Varios contenedores conectados a la misma red pueden comunicarse entre si.
Cuando se crea una red, se tiene un servicio de nombres de dominio para los contenedores y pueden direccionarse por el nombre del contenedor.

### Comunicacion entre contenedores en la red default

Cuando levantamos un contenedor y no especificamos en que red se levanta, lo hará en la red default
Levantaremos con un servidor DBMS de MySQL y otro con un cliente de MySQL.

Nos conectaremos al servidor desde el cliente, como ambos estan en la misma red el cliente puede comunicarse con el 


1) En el directorio `dbms1` levantamos el contenedor del servidor de MySQL con el nombre `some-server`

`$ docker run -v $(pwd)/data:/var/lib/mysql -u 1000:1000 -p 3306:3306 --name some-server -e MYSQL_ROOT_PASSWORD=1234 -d mysql`

3) Vemos las redes que hay en Docker con VStudio Code o Docker Desktop. Vemos la red con driver `bridge` y que el contenedor se ha levantado en ella. Puede verse si inspeccionamos la red.

Podemos ver la direccion IP del contenedor con el comando:

`$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' some-server`

4) Levantamos otro contenedor de MySQL que ejecuta el comando de cliente `mysql` para conectarse al contenedor servidor.

- prueba que puedes conectarte con la direccion IP en `<poner la IP>`

`$ docker run -it --rm mysql mysql -h <poner la IP> -uroot -p`

Una vez conectados ejecutamos algun comando para comprobar su funcionamiento:

`SHOW DATABASES;`
`EXIT`

5) Borramos el contenedor y vemos que la red por defecto se mantiene

### Comunicacion entre contenedores en una red con nombre

Crearemos una red y levantamos un contenedor con un servidor DBMS de MySQL y otro con un cliente de MySQL.

Nos conectaremos al servidor desde el cliente, como ambos estan en la misma red el cliente pueden encontrarse y nos conectaremos a el con un contenedor cliente

1) Creamos una red

`$ docker network create -d bridge my-net`

2) En el directorio `dbms1` levantamos el contenedor del servidor de MySQL con el nombre `some-server` en esta red

`$ docker run -v $(pwd)/data:/var/lib/mysql --network=my-net -u 1000:1000 -p 3306:3306 --name some-server -e MYSQL_ROOT_PASSWORD=1234 -d mysql`

3) Vemos las redes que hay en Docker con VStudio Code o Docker Desktop. Vemos la red `my-net` y que el contenedor se ha levantado en ella.

Puede verse si inspeccionamos la red. La red tiene driver `bridge`.

Podemos ver la direccion IP del contenedor con el comando:

`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' some-server`

4) Levantamos otro contenedor de MySQL que ejecuta el comando de cliente `mysql` para conectarse al contenedor servidor.

- prueba que puedes conectarte con la direccion IP

`docker run -it --network my-net --rm mysql mysql -h <IP> -uroot -p`

- prueba que puedes conectarte con el nombre del contenedor

`docker run -it --network my-net --rm mysql mysql -hsome-server -uroot -p`

Una vez conectados ejecutamos algun comando para comprobar su funcionamiento:

`SHOW DATABASES;`
`EXIT`

5) Borramos el contenedor y vemos que la red hay que borrarla de forma manual
