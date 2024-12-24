DOCKER_DB_CONTAINER="backend_db"
DB_NAME=$(grep 'db_name' django.conf | sed -E 's/.*=[[:space:]]*"([^"]+)".*/\1/')
DB_USER=${DB_NAME}_admin
DB_PASSWORD=$(grep 'db_password' django.conf | sed -E 's/.*=[[:space:]]*"([^"]+)".*/\1/')
BACKUP_DIR="$(pwd)/db_backup"
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_backup.sql"

read -p "Do you really want to flush the DB ? (y/N) " response
if [[ "$response" != "y" ]]; then
    exit 0
fi
docker compose down -v

docker compose up -d ${DOCKER_DB_CONTAINER}
sleep 3
docker cp -L ${BACKUP_FILE} $(docker compose ps -q ${DOCKER_DB_CONTAINER}):/tmp/backup.sql
sleep 3
docker compose exec ${DOCKER_DB_CONTAINER} bash -c "PGPASSWORD='${DB_PASSWORD}' psql -U ${DB_USER} -d ${DB_NAME} < /tmp/backup.sql"