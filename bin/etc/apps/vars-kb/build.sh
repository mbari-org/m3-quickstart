#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../../../.." )" && pwd )"
echo $BASE_DIR

# The first argument should be the env file that defines the env vars
source "$1" 

export DATABASE_ENVIRONMENT=production
export DATABASE_LOGLEVEL=INFO
export ANNOTATION_SERVICE_URL="${M3_HOST_NAME}:${ANNOSAURUS_PORT}${ANNOSAURUS_HTTP_CONTEXT_PATH}/v1"
export ANNOTATION_SERVICE_TIMEOUT=30seconds
export ANNOTATION_SERVICE_CLIENT_SECRET="${ANNOSAURUS_CLIENT_SECRET}"
export ORG_MBARI_VARS_KNOWLEDGEBASE_PRODUCTION_DRIVER=${VAMPIRESQUID_DATABASE_DRIVER}
export ORG_MBARI_VARS_KNOWLEDGEBASE_PRODUCTION_PASSWORD="${VARS_KB_DATABASE_PASSWORD}"
export ORG_MBARI_VARS_KNOWLEDGEBASE_PRODUCTION_URL="${VARS_KB_DATABASE_URL_FOR_APPS}"
export ORG_MBARI_VARS_KNOWLEDGEBASE_PRODUCTION_USER="${VARS_KB_DATABASE_USER}"
export ORG_MBARI_VARS_KNOWLEDGEBASE_PRODUCTION_NAME="${VARS_KB_DATABASE_NAME}"

# -- Create directory to clone source into
REPO_DIR="$BASE_DIR/temp/repos"
mkdir -p "$REPO_DIR"
cd "$REPO_DIR"

# -- Delete existing source code if it exists so we start fresh
APP_DIR="$REPO_DIR/vars-kb"
if [ -e "$APP_DIR" ]
then
  echo "Deleting existing repo at $APP_DIR"
  rm -rf "$APP_DIR"
fi

# -- Clone and build
export APP_TARGET="${BASE_DIR}/temp/apps"
echo "Building vars-kb in ${APP_DIR}"
cd "$REPO_DIR" && \
  git clone https://github.com/mbari-media-management/vars-kb && \
  cd "$APP_DIR" && \
  gradlew jpackage && \
  mkdir -p "${APP_TARGET}" && \
  cp -af "${APP_DIR}/org.mbari.kb.ui/build/jpackage/." "${APP_TARGET}/" && \
  echo "--- The 'VARS Knowledgebase' application is in  ${APP_TARGET}"

