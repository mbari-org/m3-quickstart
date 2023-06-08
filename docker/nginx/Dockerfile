FROM ubuntu:23.04

ENV NGINX_VERSION 1.25.0
ENV SRC_ROOT /usr/local/src
ENV NGINX_HOME=/usr/local/nginx

# WARNING: This makes an image that's about 385MB
# Thanks to the following references for their contributions and insights:
# https://gist.github.com/xdamman/e4f713c8cd1a389a5917
# https://github.com/nginxinc/docker-nginx
# https://github.com/arut/nginx-rtmp-module
# https://registry.hub.docker.com/u/voxxit/nginx-rtmp/
# https://docs.docker.com/articles/basics/

# RUN echo "deb http://archive.ubuntu.com/ubuntu/ impish multiverse" >> /etc/apt/sources.list \
#     && echo "deb http://archive.ubuntu.com/ubuntu/ impish-updates multiverse" >> /etc/apt/sources.list \
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y ca-certificates wget build-essential git-core libssl-dev libpcre3-dev zlib1g-dev libcap2-bin \
    && cd ${SRC_ROOT} \
    && wget -qO- http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz | tar -xz \
    && cd nginx-${NGINX_VERSION} \
    && ./configure --prefix=${NGINX_HOME} \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_ssl_module \
        --with-http_v2_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
    && make \
    && make install \
    && apt-get -y remove --purge wget build-essential git-core pkg-config checkinstall \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/* /var/tmp/* ${SRC_ROOT}/* \
    && setcap 'cap_net_bind_service=+ep' ${NGINX_HOME}/sbin/nginx

VOLUME ["/var/cache/nginx"]

COPY ./conf/nginx.conf ${NGINX_HOME}/conf/nginx.conf

COPY ./html/index.html ${NGINX_HOME}/html/index.html

COPY ./html ${NGINX_HOME}/html

EXPOSE 80 443

CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]