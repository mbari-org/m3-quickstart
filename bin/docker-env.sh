#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export BASE_DIR="$( cd "$( dirname "${MY_DIR}/../.." )" && pwd )"

# export HOST_IP=$(curl -4 ifconfig.co)
# export HOST_IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -1)
export HOST_IP="localhost"
export IMAGE_COPYRIGHT_OWNER="Creative Commons (CC)"
export JWT_ISSUER=http://www.mbari.org
export DATABASE_NAME=M3_VARS

# ---------------------------------------------------------------------
# Shared variables
export LOGBACK_LEVEL=DEBUG 
export M3_HOST_DIR="${BASE_DIR}/temp"
export M3_HOST_NAME="http://${HOST_IP}"
export M3_JDBC_BASE_URL="jdbc:postgresql://postgres:5432"
export M3_JDBC_DRIVER="org.postgresql.Driver"
export M3_JDBC_NAME=PostgreSQL
export M3_JDBC_PWD=vars0sourceforge
# export M3_JDBC_PWD=sumptuous_code
export M3_JDBC_URL_FOR_APPS="jdbc:postgresql://${HOST_IP}:5432/${DATABASE_NAME}?sslmode=disable&stringType=unspecified"
export M3_JDBC_URL="${M3_JDBC_BASE_URL}/${DATABASE_NAME}?sslmode=disable&stringType=unspecified"
export M3_JDBC_USER=m3

# ---------------------------------------------------------------------
# Application specific variables
# *_INTERNAL_URL is a services endpoint on the docker network
# *_URL is a services public endpoint URL

# Annosaurus - annotation service
export ANNOSAURUS_CLIENT_SECRET=foo
export ANNOSAURUS_DATABASE_DRIVER=${M3_JDBC_DRIVER}
export ANNOSAURUS_DATABASE_NAME=${M3_JDBC_NAME}
export ANNOSAURUS_DATABASE_PASSWORD=${M3_JDBC_PWD}
export ANNOSAURUS_DATABASE_URL_FOR_APPS="${M3_JDBC_URL_FOR_APPS}"
export ANNOSAURUS_DATABASE_URL="${M3_JDBC_URL}"
export ANNOSAURUS_DATABASE_USER="${M3_JDBC_USER}"
export ANNOSAURUS_INTERNAL_URL="http://annosaurus:8080/v1"
export ANNOSAURUS_PORT=8082
export ANNOSAURUS_SIGNING_SECRET=bar
export ANNOSAURUS_TIMEOUT="60 seconds"
export ANNOSAURUS_URL="http://${HOST_IP}:${ANNOSAURUS_PORT}/v1"
export ANNOSAURUS_ZEROMQ_ENABLE=true
export ANNOSAURUS_ZEROMQ_PORT=5563
export ANNOSAURUS_ZEROMQ_TOPIC=vars

# Beholder - extract frame from video service
export BEHOLDER_API_KEY=foo
export BEHOLDER_CACHE_FREEPCT=0.20
export BEHOLDER_CACHE_SIZE=1000
export BEHOLDER_INTERNAL_URL="http://beholder:8080"
export BEHOLDER_PORT=8088
export BEHOLDER_TIMEOUT="10 seconds"
export BEHOLDER_URL="http://${HOST_IP}:${BEHOLDER_PORT}"

# Oni - knowledgebase and user accounts service
export ONI_CLIENT_SECRET=foo
export ONI_DATABASE_DRIVER=${M3_JDBC_DRIVER}
export ONI_DATABASE_PASSWORD=${M3_JDBC_PWD}
export ONI_DATABASE_URL="${M3_JDBC_URL}"
export ONI_DATABASE_USER="${M3_JDBC_USER}"
export ONI_INTERNAL_URL="http://oni:8080/v1"
export ONI_PORT=8083
export ONI_SIGNING_SECRET=bar
export ONI_URL="http://${HOST_IP}:${ONI_PORT}/v1"
export ONI_URL_FOR_APPS="${M3_JDBC_URL_FOR_APPS}"

# Panoptes - image archiving service
# PANOPTES_ROOT_DIRECTORY is where framegrags are stored inside 
# the docker container. Map an external volume to this dir.
#
# PANOPTES_ROOT_URL is the URL that maps PANOPTES_ROOT_DIRECTORY as a
# public accessible URL.
export PANOPTES_CLIENT_SECRET=foo
export PANOPTES_FILE_ARCHIVER="org.mbari.m3.panoptes.services.OldStyleMbariDiskArchiver"
export PANOPTES_HTTP_CONTEXT_PATH=/panoptes
export PANOPTES_INTERNAL_URL="http://panoptes:8080${PANOPTES_HTTP_CONTEXT_PATH}/v1"
export PANOPTES_PORT=8085
export PANOPTES_ROOT_DIRECTORY=/framegrabs
export PANOPTES_ROOT_URL="${M3_HOST_NAME}/framegrabs"
export PANOPTES_SIGNING_SECRET=bar
export PANOPTES_URL="http://${HOST_IP}:${PANOPTES_PORT}${PANOPTES_HTTP_CONTEXT_PATH}/v1"

# Pythia - machine learnign service
# export PYTHIA_PORT=8888
# export PYTHIA_MODEL_DIRECTORY="/export/maxarray2/vars/applications/m3-quickstart/temp/pythia"
# export MODEL_NAME="fathomnet_meg_detector"
# export YOLO_VERSION=8
# export YOLO_RESOLUTION=640

# Raziel - VARS Service configuration server
export RAZIEL_HTTP_CONTEXT=config
export RAZIEL_JWT_SIGNING_SECRET=foo
export RAZIEL_MASTER_KEY=inflatable_ducks
export RAZIEL_PORT=8400

# Vampire squid - video asset manager service
export VAMPIRESQUID_CLIENT_SECRET=foo
export VAMPIRESQUID_DATABASE_DRIVER=${M3_JDBC_DRIVER}
export VAMPIRESQUID_DATABASE_NAME=${M3_JDBC_NAME}
export VAMPIRESQUID_DATABASE_PASSWORD=${M3_JDBC_PWD}
export VAMPIRESQUID_DATABASE_URL_FOR_APPS="${M3_JDBC_URL_FOR_APPS}"
export VAMPIRESQUID_DATABASE_URL="${M3_JDBC_URL}"
export VAMPIRESQUID_DATABASE_USER="${M3_JDBC_USER}"
export VAMPIRESQUID_PORT=8084
export VAMPIRESQUID_SIGNING_SECRET=bar
export VAMPIRE_SQUID_INTERNAL_URL="http://vampire-squid:8080/v1"
export VAMPIRE_SQUID_URL="http://${HOST_IP}:${VAMPIRESQUID_PORT}/v1"

# Miscellaneous
export VARS_KB_SERVER_URL="${ONI_URL}"
export VARS_QUERY_FRAME_TITLE="VARS Query"
export VARS_KB_SERVER_INTERNAL_URL="${ONI_INTERNAL_URL}"
export VARS_USER_SERVER_INTERNAL_URL="${ONI_INTERNAL_URL}"
export VARS_USER_SERVER_URL="${ONI_URL}"

# Charybdis - specialized query service
export CHARYBDIS_ANNOSAURUS_TIMEOUT=PT20S
export CHARYBDIS_ANNOSAURUS_URL="${ANNOSAURUS_INTERNAL_URL}"
export CHARYBDIS_INTERNAL_URL="http://charybdis:8080"
export CHARYBDIS_PORT=8086
export CHARYBDIS_URL="http://${HOST_IP}:${CHARYBDIS_PORT}"
export CHARYBDIS_VAMPIRESQUID_TIMEOUT=PT20S
export CHARYBDIS_VAMPIRESQUID_URL="${VAMPIRE_SQUID_INTERNAL_URL}"

# --- NOTES
#
# BASE_DIR should be defined before you source this file
#
# M3_JDBC_NAME indicates the SQL dialect used by JPA apps. Acceptable 
# values are:
# Auto, Oracle, Oracle11, Oracle10g, Oracle9i, Oracle8i, Attunity, 
# Cloudscape, Database, DB2, DB2MainFrame, DBase, Derby, HANA, HSQL,
# Informix, Informix11, JavaDB, MaxDB, MySQL4, MySQL, PointBase,
# PostgreSQL, SQLServer, Sybase, Symfoware, timesTen
#
# For Hikari test see # https://stackoverflow.com/questions/3668506/efficient-sql-test-query-or-validation-query-that-will-work-across-all-or-most
#
# vars-user-service and vars-kb-service generally run against the same 
# database. We use `VARS_KB_` env vars to store values that are shared 
# by both of these databases.
#
# PANOPTES_ROOT_DIRECTORY is where framegrags are stored relative to 
# the docker container. Map an external volume to this dir.
#
# PANOPTES_ROOT_URL is the URL that maps PANOPTES_ROOT_DIRECTORY as a
# URL.