#!/usr/bin/env bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <source JDBC URL> <source database user> <target JDBC URL> <target database user>"
  exit 1
fi

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../.." )" && pwd )"

export SRC_URL=$1
export SRC_USER=$2
export DEST_URL=$3
export DEST_USER=$4

echo "WARNING! This script will migrate the following databases:
1. vampire-squid: $SRC_URL to $DEST_URL

Be sure that the database tables at $DEST_URL are empty. Hit [ctrl]+[c] to cancel this script.
"

read -s -p "Password for $SRC_USER @ $SRC_URL: " SRC_PWD
echo ""
read -s -p "Password for $DEST_USER @ $DEST_URL: " DEST_PWD

export SRC_PWD="$SRC_PWD"
export DEST_PWD="$DEST_PWD"

"$BASE_DIR/bin/etc/scala/MigrateVampireSquid.sc" \
  "$SRC_URL" "$SRC_USER" \
  "$DEST_URL" "$DEST_USER"