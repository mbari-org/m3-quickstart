#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../.." )" && pwd )"

ENV_FILE="$BASE_DIR/bin/docker-env.sh"

if [ -z "${GITHUB_TOKEN}" ]; then
  echo "GITHUB_TOKEN environment variable is not set. Please follow the instructions at https://github.com/mbari-org/maven#gradle to set it."
  echo "You can add the GITHUB_TOKEN to your .bashrc file or the bin/docker-env.sh file."
  exit 1
fi

if [ -z "${GITHUB_USERNAME}" ]; then
  echo "GITHUB_USERNAME environment variable is not set. Please follow the instructions at https://github.com/mbari-org/maven#gradle to set it."
  echo "You can add the GITHUB_USERNAME to your .bashrc file or the bin/docker-env.sh file."
  exit 1
fi
 
"$BASE_DIR/bin/etc/apps/vars-kb/build.sh" "$ENV_FILE"
"$BASE_DIR/bin/etc/apps/vars-query/build.sh" "$ENV_FILE"
