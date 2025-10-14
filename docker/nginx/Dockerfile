FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY html /usr/share/nginx/html