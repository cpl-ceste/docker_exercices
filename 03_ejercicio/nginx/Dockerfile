FROM nginx

RUN apt-get update && apt-get install -y curl && apt-get clean

COPY nginx-conf/nginx.conf /etc/nginx/nginx.conf 
COPY static-site /usr/share/nginx/html
