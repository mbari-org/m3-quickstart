#!/usr/bin/env bash

set -e
pushd $(pwd)

# first arg is the env file
export ENV_FILE="$1"

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../../.." )" && pwd )"
 
"$BASE_DIR/etc/apps/vars-kb/build.sh" "$BASE_DIR/.env"
"$BASE_DIR/etc/apps/vars-query/build.sh" "$BASE_DIR/.env"

popd
