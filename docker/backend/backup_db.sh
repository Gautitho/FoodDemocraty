DOCKER_DB_CONTAINER="db"
DB_NAME=$(grep 'db_name' docker/conf.toml | sed -E 's/.*=[[:space:]]*"([^"]+)".*/\1/')
DB_USER=${DB_NAME}_admin
DB_PASSWORD=$(grep 'db_password' docker/conf.toml | sed -E 's/.*=[[:space:]]*"([^"]+)".*/\1/')
DATE=$(date +%Y%m%d)
BACKUP_DIR="$(pwd)/db_backup"
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_backup_${DATE}.sql"
SYMLINK="${BACKUP_DIR}/${DB_NAME}_backup.sql"
LOG_FILE="$(pwd)/backup_db.log"

set -e

mkdir -p $BACKUP_DIR > $LOG_FILE 2>&1

docker compose up -d ${DOCKER_DB_CONTAINER}
sleep 3
docker compose exec ${DOCKER_DB_CONTAINER} bash -c "PGPASSWORD='${DB_PASSWORD}' pg_dump -U ${DB_USER} -d ${DB_NAME} > /var/lib/postgresql/data/backup.sql"
sleep 3
docker cp $(docker compose ps -q ${DOCKER_DB_CONTAINER}):/var/lib/postgresql/data/backup.sql ${BACKUP_FILE}
ln -sfn $BACKUP_FILE $SYMLINK >> $LOG_FILE 2>&1

# Removing old backups
backup_files=$(find ${BACKUP_DIR} -type f -name "${DB_NAME}_backup_*.sql")
backup_count=$(echo "${backup_files}" | wc -l)
if [ ${backup_count} -gt 3 ]; then
  find ${BACKUP_DIR} -type f -name "${DB_NAME}_backup_*.sql" -mtime +90 -exec rm {} \; >> ${LOG_FILE} 2>&1
  echo "Old backups deleted."
else
  echo "Not enough backup too delete oldest."
fi