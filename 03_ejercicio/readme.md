# EJERCICIO 3 - IMAGENES

Documentacion de referencia [Docker Docs](https://docs.docker.com/)

## Crear imagenes

Podemos crear una imagen a partir:

- de un contendor que se este ejecutando o que este parado
  
- de un Dockerfile

### Crear una imagen a partir de un contendor

Tenemos una aplicacion web creada con nginx y la modificamos al ejecutarla en un contendor con nuestro codigo.

Crearemos una imagen a partir de este contenedor. veremos que para ello se usa el comando de Docker `commit`.

0) Navegamos al directorio `nginx`

1) Ejecutamos el contenedor de nginx sin mapear los contenidos de nuestro codigo web y configuracion del servidor

`$ docker run -dp 8080:80 --name my-web nginx`

2) Copiamos los ficheros de nuestra web y de configuracion al contenedor

`$ docker cp ./static-site/index.html my-web:/usr/share/nginx/html/index.html`
`$ docker cp ./static-site/images/ my-web:/usr/share/nginx/html/images`

`$ docker cp ./static-site/images/foto.jpg my-web:/usr/share/nginx/html/images/foto.jpg`

`$ docker cp ./nginx-conf/nginx.conf my-web:/etc/nginx/nginx.conf`

3) Vemos la pagina web y los logs de la aplicacion

4) Vemos que la nueva configuracion de los logs no ha tenido efecto. Hay que hacer un restart de nginx para que coja el nuevo formato. Para ello podemos entrar al contendor y hacer un restart del servicio, o tambien podemos parar y rearrancar el contenedor que es mas sencillo.

4) Crear una imagen a partir de este contendor

`$ docker commit my-web my-web-app:v0`

Puede ser conveniente parar el contenedor para construir la imagen para evitar cualquier modificacion en el momento de la creacion. No obstante esta es la accion por defecto del comando `commit`, puesto que al crear la imagen el contenedor se para momentaneamente (a no ser que se especifique lo contrario en la instruccion `docker commit`)

5) Comprobamos que tenemos una nueva imagen en nuestra coleccion de imagenes locales, en Docker Desktop o VStudio Code

6) Paramos y eliminamos el contendor anterior y ejecutamos ahora uno nuevo a partir de la imagen que hemos creado.

`$ docker run -dp 8081:80 --name my-web1 my-web-app:v0`

7) Vemos la pagina web y los logs de la aplicacion y comprobamos que son los de nuestra aplicacion web

8) Paramos y borramos los contenedores y las imagenes creadas

Es importante tener en cuenta que **los commits no incluyen ningún dato contenido en volúmenes montados**. Solo incluyen los cambios hechos dentro del sistema de ficheros interno del contenedor o cualquier cambio en la configuracion del mismo.

Si intentamos crear una nueva imagen desde un contenedor en ejecución y hemos montado volúmenes en ese contenedor, los cambios realizados dentro de esos volúmenes no se capturarán mediante el comando `commit`. El comando `docker commit` solo captura los cambios en el sistema de archivos realizados dentro del propio contenedor, no los cambios realizados en los volúmenes montados.

Los cambios realizados con `docker cp` se consideran parte del sistema de archivos del contenedor y se capturan mediante `docker commit`. De forma que si se copiamos archivos en un volumen montado, esos cambios se propagan a los volumenes montados y se incluyen en el la nueva imagen.

Vamos a probarlo:

0) Navegamos al directorio `nginx`

1) Ejecutar el contenedor de nginx mapeando los contenidos de nuestro codigo web y configuracion del servidor

`$ docker run -dp 8080:80 --name my-web -v $(pwd)/static-site:/usr/share/nginx/html -v $(pwd)/nginx-conf/nginx.conf:/etc/nginx/nginx.conf nginx`

2) `docker commit` no incluye los volumenes montados. Hacemos un `commit` y creamos una nueva imagen

`$ docker commit my-web my-web-app:v1`

3) Comprobamos que tenemos una nueva imagen en nuestra coleccion de imagenes locales, en Docker Desktop o VStudio Code

4) No eliminamos el contendor anterior de momento y ejecutamos ahora uno nuevo en otro puerto a partir de la imagen que hemos creado.

`$ docker run -dp 8081:80 --name my-web1 my-web-app:v1`

5) Vemos la pagina web en el navegador y los logs de la aplicacion y comprobamos que son los de la aplicacion por defecto del contenedor de nginx. Comprobamos los ficheros del contendor y vemos que no esta nuestra pagina web

6) Copiamos en el contendor original los ficheros en los volumentes mapeados

`$ docker cp ./static-site/index.html my-web1:/usr/share/nginx/html/index.html`

`$ docker cp ./static-site/images/ my-web1:/usr/share/nginx/html/images`

`$ docker cp ./static-site/images/foto.jpg my-web1:/usr/share/nginx/html/images/foto.jpg`

`$ docker cp ./nginx-conf/nginx.conf my-web1:/etc/nginx/nginx.conf`

El posible que se necesite parar el contendor para copiar el fichero de configuracion.

7) Comprobamos que el conendor tiene copiados los ficheros internamente, navegando a la web y viendo los logs

7) `docker commit` no incluye los volumenes montados, pero si se han copiado en el sistema de ficheros dentro del contenedor, si lo hara. Hacemos un commit del primer contenedor y creamos una nueva imagen

`$ docker commit my-web1 my-web-app:v2`

8) Arrancamos un nuevo contenedor con la imagen que hemos creado

`$ docker run -dp 8082:80 --name my-web2 my-web-app:v2`

9) Vemos la pagina web en el navegador y los logs de la aplicacion y comprobamos que son los de nuestra aplicacion web. Comprobamos los ficheros del contendor y vemos que son los de esta nuestra pagina web

6) Paramos y eliminamos los contenedores e imagenes creadas

### Crear una imagen a partir de un Dockerfile

Para controlar mejor los cambios que se hacen en una imagen para crear una nueva, se utiliza un fichero `Dockerfile`.

Los cambios se recogen como comandos y es mas facil mantener y extender imagenes existentes.

El archivo Dockerfile es una plantilla de especificacion para la construccion de una imagen. El un tipo de creacion de infraeetructura con codigo IaaC.

Creamos una aplicacion web lavantando una imagen de NGINX con un `Dockerfile` que copia los ficheros de nuestra aplicacion web y de configuracion del servidor.

0) Navegamos al directorio `ngnix`

1) Abrimos el `Dockerfile` y vemos como vamos a construir la nueva imagen y la contruimos

`$ docker build -t my-web-app:v03.`

2) Ejecutamos un nuevo contenedor creado a partir de esta imagen

`$ docker run -dp 8082:80 --name my-web3 my-web-app:v3`

3) Vemos la pagina web en el navegador y los logs de la aplicacion y comprobamos que son los de nuestra aplicacion web. Comprobamos los ficheros del contendor y vemos que no esta nuestra pagina web


### Otros comandos para trabajar con imágenes

Probamos los comandos mas habituales para trabajar con imagenes

`$ docker image pull name:latest`

`$ docker image ls (-a)`

`$ docker image rmi (name:tag or <image id>)`

`$ docker image push name:tag`
