# EJERCICIO 4 - REGISTRO DE IMAGENES

Documentacion de referencia [Docker Docs](https://docs.docker.com/)

## Publicar imágenes

Las imágenes creadas se almacenan en local y podemos publicarlas en un registro publico o privado para compartirlas dentro de nuestra organizacion.

Trabajaremos con una aplicación web que desarrollamos en Docker y la publicaremos en diferentes registros.

### Publicar imagenes en un registro publico

Crearemos un contenedor con la imagen de la aplicacion welcome-to-docker.
El codigo de la aplicación web esta disponible en la carpeta `welcome-to-docker` (obtenido de `git clone https://github.com/docker/welcome-to-docker`)

0) Navegar al dir `04_ejercicio`. Copiar la carpeta `nginx` del ejercicio anterior donde tenemos nuestra web-app

`$ cp -r ../03_ejercicio/nginx ./nginx`
`$ cd nginx`

1) Desde el dir `nginx` construimos una imagen con nuestra aplicacion si no tenemos ninguna. Examinamos el `Dockerfile` y vemos que se copiaran en la nueva imagen los ficheros fuente y de configuracion que hemos creado para nuestra aplicación.

`$ docker build -t my-web-app:latest .`

2) Corremos el contenedor para verla

`$ docker run --name my-web --rm -dp 8080:80 my-web-app:latest`

Notese que lo arrancamos en background y mapeamos los puertos con el flag `-dp` y que configuramos la instruccion `--rm` para que se borre el contenedor al pararlo

3) Paramos el contendor y se borra por haberlo lanzado con la instruccion `--rm`

4) Vamos a publicar la imagen en el Registro público de DockerHub. Hacemos login en DockerHub, si no estamos conectados:

`$ docker login`

5) Nombramos la imagen de nuestro sistema local `image_name:tag` y la etiquetamos la imagen con los nombres que queremos utilizar en DockerHub ``new_image_name:tag`. El nombre de la nueva imagen creará un nuevo repositorio para nuestro usuario de DockerHub y la etiqueta recogerá la version de la imagen en ese repositorio.

`$ docker tag image_name:tag USER_NAME/new_image_name:tag`

En nuestro caso la imagen local es `my-web-app:latest` podemos publicarla como `web-app:v0`.
La etquetamos y la publicamos sustituyendo ÙSERNAME`por nuestro nombre de usuario en DockerHub:

`$ docker tag my-web-app:latest USER_NAME/web-app:v0`
`$ docker push USER_NAME/web-app:v0`

8) Comprobamos que en DockerHub se ha creado un nuevo repositorio de imagenes en nuestro usuario y tenemos una imagen en el que es la aplicacion en su version v0. Publica ahora una version latest y comprueba como puedes recoger en el repo diferentes versiones de las imagenes de tu aplicacion

`$ docker tag my-web-app:latest USER_NAME/web-app:latest`
`$ docker push USER_NAME/web-app:latest`

9) Ejecuta un contendor de otro compañero para ver la aplicacion web que ha publicado

`$ docker run --name other-web-app --rm -dp 8081:80 OTHER_USER_NAME/web-app:latest`

10) Para el contendor, que se borrara autmomaticamente


### Levantar un registro privado

Ademas de utilizar el registro publico de DockerHub pordemos tener un registro privado, que desplegamos en una maquina y administramos nosotros mismos para nuestra organizacion.

Levantaremos un registro en nuestra maquina `localhost` y podremos acceder a el para descargar y publicar imagenes.

1) En DockerHub vemos que hay una imagen llamada `registry` que permite levantar registros de Docker

2) Ejecutamos el registro de docker en un contenedor para levantar el registro

`$ docker run -d -p 5000:5000 --restart always --name registry registry:2`

3) Podemos ver el catalogo de repositorios en un registro con el siguiente comando al API del registro

`$ curl -X GET http://localhost:5000/v2/_catalog`

4) Publicamos nuestra imagen en nuestro registro privado:

`$ docker tag my-web-app:latest localhost:5000/web-app:latest`
`$ docker push localhost:5000/web-app:latest`

5) Comprobamos que hay un nuevo repositorio y listamos las imagenes de ese repositorio

`$ curl -X GET http://localhost:5000/v2/_catalog`
`$ docker image ls localhost:5000/web-app`

6) Paramos el contenedor del registro y podemos borrar la imagen `registry`


### Publicar imagenes en un registro privado

Si instalamos el registro en una maquina donde abrimos el puerto 5000 a otros usuarios, estos podrán conectarse y trabajar con el registro.

Para ello hemos levantado un registro en una maquina en Amazon a la que podemos acceder por su `DIRECCION_IP`

1) Listamos los repositorios del registro:

`$ curl -X GET http://DIRECCION_IP:5000/v2/_catalog`


4) Publicamos nuestra imagen en nuestro registro privado, poner como nombre de la imagen vuestro nombre de usuario en minusculas `user`:

`$ docker tag my-web-app:latest DIRECCION_IP:5000/user/web-app:latest`
`$ docker push DIRECCION_IP:5000/user/web-app:latest`

5) Listamos los repositorios del registro tras haber subido nuestra imagen:

`$ curl -X GET http://DIRECCION_IP:5000/v2/_catalog`

6) Bajamos nuestra imagen o la de un compañero o corremos un contenedor con una imagen del registro privado

`$ docker run -dp 8082:80 --name my-web2 DIRECCION_IP:5000/user/web-app:latest`

