#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../.." )" && pwd )"

source "$BASE_DIR/bin/docker-env.sh"
export VARS_PWD="$VARS_KB_DATABASE_PASSWORD"
"$BASE_DIR/bin/etc/scala/CreateUser.sc" "$VARS_KB_DATABASE_URL_FOR_APPS" "$VARS_KB_DATABASE_USER" "$1"