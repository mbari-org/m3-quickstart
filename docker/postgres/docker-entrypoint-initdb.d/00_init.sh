!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

  CREATE ROLE postgres;
  GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO postgres;
  ALTER ROLE postgres WITH LOGIN PASSWORD '$POSTGRES_PASSWORD';
EOSQL