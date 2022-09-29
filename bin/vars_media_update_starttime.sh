
#!/usr/bin/env bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$( dirname "${MY_DIR}/../.." )" && pwd )"

source "$BASE_DIR/bin/docker-env.sh"
python "$BASE_DIR/bin/etc/python/vars_media_update_starttime.py" "$@"