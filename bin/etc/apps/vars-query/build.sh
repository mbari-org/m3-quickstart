#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../../../.." )" && pwd )"
echo $BASE_DIR

# -- Set environment variables needed for jpackage
source "$1"

# -- Remap env vars to those expected in teh `application.conf` file
export ANNOSAURUS_JDBC_DRIVER=$ANNOSAURUS_DATABASE_DRIVER
export ANNOSAURUS_JDBC_PASSWORD=$ANNOSAURUS_DATABASE_PASSWORD
export ANNOSAURUS_JDBC_USER=$ANNOSAURUS_DATABASE_USER
export ANNOSAURUS_JDBC_URL="$ANNOSAURUS_DATABASE_URL_FOR_APPS"
export CONCEPT_SERVICE_URL="${M3_HOST_NAME}:${VARS_KBSERVER_PORT}${VARS_KBSERVER_HTTP_CONTEXT_PATH}/v1"
export CONCEPT_SERVICE_TIMEOUT=60seconds
export SHARKTOPODA_PORT=8800
export VARS_ANNOTATION_START_DATE="1982-01-01T00:00:00Z"
export VARS_QUERY_RESULTS_COALESCE_KEY="index_elapsed_time_millis"

# -- Create directory to clone source into
REPO_DIR="$BASE_DIR/temp/repos"
mkdir -p "$REPO_DIR"
cd "$REPO_DIR"

# -- Delete existing source code if it exists so we start fresh
APP_DIR="$REPO_DIR/vars-query"
if [ -e "$APP_DIR" ]
then
  echo "Deleting existing repo at $APP_DIR"
  rm -rf "$APP_DIR"
fi

# -- Clone and build
export APP_TARGET="${BASE_DIR}/temp/apps"
echo "Building vars-query in ${APP_DIR}"
cd "$REPO_DIR" && \
  git clone https://github.com/mbari-media-management/vars-query && \
  cd "$APP_DIR" && \
  gradlew jpackage && \
  mkdir -p "${APP_TARGET}" && \
  cp -af "${APP_DIR}/build/jpackage/." "${APP_TARGET}/" && \
  echo "--- The 'VARS Query' application is in  ${APP_TARGET}"

