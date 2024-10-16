#!/bin/sh
# wait-for-it.sh

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for PostgreSQL to become available..."
until PGPASSWORD=$DB_PASSWORD psql -h "$host" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 10
done

>&2 echo "PostgreSQL is up - executing command"
exec $cmd
