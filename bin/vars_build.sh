#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../.." )" && pwd )"

ENV_FILE="$BASE_DIR/bin/docker-env.sh"
 
"$BASE_DIR/bin/etc/apps/vars-kb/build.sh" "$ENV_FILE"
"$BASE_DIR/bin/etc/apps/vars-query/build.sh" "$ENV_FILE"
