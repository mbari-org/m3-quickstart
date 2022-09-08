FROM mcr.microsoft.com/azure-sql-edge:latest

ENV ACCEPT_EULA Y
ENV MSSQL_PID Express

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN chmod +x /usr/src/app/run-initialization.sh

CMD /bin/bash ./entrypoint.sh
