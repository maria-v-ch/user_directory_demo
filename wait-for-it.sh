#!/bin/sh
# wait-for-it.sh

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for PostgreSQL to become available..."
echo "DB_USER: $DB_USER"
echo "DB_NAME: $DB_NAME"
echo "DB_HOST: $host"
echo "DB_PORT: $port"

until PGPASSWORD=$DB_PASSWORD psql -h "$host" -p "$port" -U "$DB_USER" -d "$DB_NAME" -c '\l'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 10
done

>&2 echo "PostgreSQL is up - executing command"
exec $cmd
