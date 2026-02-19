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

Y hay más razones. Entonces, es mejor ejecutar una aplicación que tiene diferentes componentes en varios contenedores, uno para cada componente.

Para levantar una aplicación con multiples contenedores podemos ejecutarlos individualmente y conectarlos o utilizar Docker Compose.

### Ejecutar una aplicacion web con base de datos

Tenemos una aplicacion web que se ejecuta en Node.js y tiene una configuracion interna en la que si queremos puede conectarse a una base de datos.

![image](https://docs.docker.com/get-started/workshop/images/multi-container.webp?w=350h=250)

Ejecutaremos primero a aplicacion sola y luego, la ejecutaremos conectandola a otro contenedor MySQL

1) Navegamos hasta el dir `/app` y ejecutamos un contenedor con Node.js en el que mapeamos nuestro volumen con la aplicacion web y la construimos con `yarn`

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


## Levantar una aplicacion de web IA con multiples contenedores

En el area de IA han surgido modelos de lenguaje muy potentes (Large Language Models - LLMs) que nos permiten crear interfaces de usuario cognitivas, es decir que soportan unas funcionalidades de lenguaje inteligentes y pueden chatear, entender el audio y el texto que los usuarios utilizan para comunicarse con la aplicacion.

Vamos a desplegar una aplicacion web que nos permite crear chatbots inteligentes e interactuar con ellos por texto o voz. Para ello utilizaremos dos aplicaciones que descargaremos como contenedores y ejecutaremos con docker-compose. Una de ellas es el motor de ejecucion de los LLMs y la otra es la interfaz web que nos permite trabajar con este motor.

Utilizaremos:

1- **Ollama**: [Ollama](https://ollama.com/) es una herramienta que permite ejecutar modelos grandes de lenguaje (LLMs) de inteligencia artificial de forma local en tu ordenador, sin necesidad de conexión a internet. Esto garantiza que todos los datos y procesos se mantengan en tu dispositivo, ofreciendo mayor privacidad y control. Ollama facilita la instalación y uso de diversos modelos open-source de IA  (LLAMA-3, DeepSeek-R1, Gemma 3, etc).

2- **WebUI**: [​Open WebUI](https://openwebui.com/) es una plataforma de inteligencia artificial autoalojada, extensible y fácil de usar, diseñada para operar completamente sin conexión a internet. Permite a los usuarios ejecutar y gestionar modelos de lenguaje de gran tamaño (LLMs) localmente a través de una interfaz web intuitiva. Permite integrarse con Ollama y APIs compatibles de modelos (i.e. OpenAI), puede ejecutarse sobre CPU y GPU (cuda) y tiene otras muchas funcionalidades (motor para RAG, etc.)

1)  Navegamos al directorio `/web-ai` y abrimos el fichero `docker-compose.yaml` o el fichero `docker-compose-cpu-based.yml`

Analizamos las partes del fichero, vemos los servicios que esta utilizando, los puertos y los volumenes que mapea en nuestro entorno local.

Analizamos las imagenes que usa cada uno de los servicios. Una de las imagenes vamos a crearla utilizando el `Dockerfile` que tenemos en el directorio. Analizamos el `Dockerfile` para entender la imagen que estamos creando. Vemos que hay un fichero `entrypoint.sh` que estamos utilizando para arrancar y lo  ¿que similitudes y diferencias observamos?

2) Levantamos la aplicacion en modo dettached, indicando que debe de construir la imagen en el despliegue y el fichero `yaml` que describe el despleigue.

Ejecutamos el comando para desplegarlo para que corra sobre GPU `$ docker compose -f docker-compose.yml up -d --build`

Analizamos como se ha construido la imagen e inspeccionamos los contenedores

4) Probamos la aplicación y vemos que es un entorno web de Chatbots de IA totalmente configurable para el despliegue de diferentes modelos de LLM

5) Podemos instalar más modelos para nuestro ChatBot. Navegamos a la web de Ollama para ver los modelos que soporta [Ollama](https://ollama.com/search) e instalamos alguno de ellos. 

Para instalarlo podemos abrir una terminal en el contenedor de `ollamadeepseek` y ejecutar un comando `ollama run gemma3:1b ` para bajarnos un modelo pequeñito, que será mas rapido.

Estos cambios desapareceran si borramos el contenedor y para hacerlos persistentes en realidad podemos incluirlos en el `Dockerfile`o en el fichero `entrypoint.sh`, pero para verlo de forma rápida modificando el contenedor nos bastará.

Probamos nuestra aplicación web (si no reconoce el nuevo modelo de forma dinamica podemos reiniciarla) y vemos que podemos abrir varios chats con cada modelo.

6) Probamos otros comandos de docker compose donde podemos trabajar con los contenedores individuales, identificados por el nombre del `service` que hemos definido en el fichero `compose.yaml`:

`$ docker compose ps`

`$ docker compose stop <service>`

`$ docker compose start <service>`

`$ docker compose logs <service>`

7) Ejecutamos el comando para borrar los contenedores y borramos redes y volumenes que queden sin borrar

`$ docker compose down`


