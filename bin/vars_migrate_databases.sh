#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../.." )" && pwd )"

source "$BASE_DIR/bin/docker-env.sh"

export SRC_URL_VAMPIRESQUID="$VAMPIRESQUID_DATABASE_URL_FOR_APPS"
export SRC_USER_VAMPIRESQUID="$VAMPIRESQUID_DATABASE_USER"
export SRC_PWD_VAMPIRESQUID="$VAMPIRESQUID_DATABASE_PASSWORD"

export SRC_URL_ANNOSAURUS="$ANNOSAURUS_DATABASE_URL_FOR_APPS"
export SRC_USER_ANNOSAURUS="$ANNOSAURUS_DATABASE_USER"
export SRC_PWD_ANNOSAURUS="$ANNOSAURUS_DATABASE_PASSWORD"

export SRC_URL_KB="$VARS_KB_DATABASE_URL_FOR_APPS"
export SRC_USER_KB="$VARS_KB_DATABASE_USER"
export SRC_PWD_KB="$VARS_KB_DATABASE_PASSWORD"

echo "WARNING! This script will migrate the following databases:
1. vampire-squid: $SRC_URL_VAMPIRESQUID to $DEST_URL
2. annosaurus: $SRC_URL_ANNOSAURUS to $DEST_URL
3. vars-kb-server and vars-user-server: $SRC_URL_KB to $DEST_URL

Be sure that the database tables at $DEST_URL are empty. Hit [ctrl]+[c] to cancel this script.
"

export DEST_URL=$1
export DEST_USER=$2
read -s -p "Password for $DEST_USER: " DEST_PWD

export SRC_PWD="$SRC_PWD_VAMPIRESQUID"
"$BASE_DIR/bin/etc/scala/MigrateVampireSquid.sc" \
  "$SRC_URL_VAMPIRESQUID" "$SRC_USER_VAMPIRESQUID" \
  "$DEST_URL" "$DEST_USER"

export SRC_PWD="$SRC_PWD_ANNOSAURUS"
"$BASE_DIR/bin/etc/scala/MigrateAnnosaurus.sc" \
  "$SRC_URL_ANNOSAURUS" "$SRC_USER_ANNOSAURUS" \
  "$DEST_URL" "$DEST_USER"

export SRC_PWD="$SRC_PWD_KB"
"$BASE_DIR/bin/etc/scala/MigrateKnowledgebase.sc" \
  "$SRC_URL_KB" "$SRC_USER_KB" \
  "$DEST_URL" "$DEST_USER"


 
