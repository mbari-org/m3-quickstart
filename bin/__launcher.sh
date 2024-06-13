#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../.." )" && pwd )"

SCRIPT_NAME=$(basename -- "$1")
SCRIPT_EXTENSION="${SCRIPT_NAME##*.}"

if [ "$SCRIPT_EXTENSION" = "py" ]; then
    source "$BASE_DIR/bin/docker-env.sh"
    python "$BASE_DIR/bin/etc/python/$1" "${@:2}"
    exit
elif [ "$SCRIPT_EXTENSION" = "sc" ]; then
    source "$BASE_DIR/bin/docker-env.sh"
    export VARS_PWD="$VARS_KB_DATABASE_PASSWORD"
    "$BASE_DIR/bin/etc/scala/$1" "${@:2}"
    exit
fi
