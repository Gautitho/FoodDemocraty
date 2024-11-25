#!/bin/bash

# Before running this script :
# - create conf.toml

# Execute this script as su

# Exit when any command fails
set -e

# Inputs of the script
DEPLOY_MODE=${1:-0} # 3 modes allowed : 0 (DEV) (default) / 1 (PROD) / 2 (DOCKER)
INIT_DB=${2:-0} # 2 modes allowed : 0 (default) / 1 (flush DB and apply fixtures)
CLEAN_ENV=${3:-0} # 2 modes allowed : 0 (default) / 1 (Remove env and rebuild it)
MAC_ENV=${4:-0} # 2 modes allowed : 0 (Linux) (default) / 1 (Mac)

# Text colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ $MAC_ENV = 0 ]; then
    USER=$(whoami)
fi

echo -e "${BLUE}### Source environnement${NC}"
if [ $CLEAN_ENV = 1 ]; then
    rm -rf .env
    python -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
else
    source .env/bin/activate
fi

if [ "$DEPLOY_MODE" -lt 2 ]; then
    echo -e "${BLUE}### Starting Postgresql (DB)${NC}"
    if [ $MAC_ENV = 1 ]; then
        if ! brew services list | grep -q "postgresql"; then
            # Start PostgreSQL service if not started
            brew services start postgresql
        else
            echo "PostgreSQL service is already started."
        fi
    else
        sudo service postgresql start   # Starting database
    fi

    # Flushing and recreating DB
    if [ $INIT_DB = 1 ]; then
        # Create postgres user if not exist
        if [ $MAC_ENV = 0 ]; then
            sudo -iu postgres dropdb --if-exists ${USER}    # Workaround for a postgres bug
            sudo -iu postgres createdb ${USER}              # Workaround for a postgres bug
            echo "CREATE USER ${USER} WITH PASSWORD '0000';" | sudo -iu postgres psql
            echo "ALTER USER ${USER} SUPERUSER CREATEDB CREATEROLE LOGIN;" | sudo -iu postgres psql
        fi

        DB_NAME=$(grep 'db_name' backend/conf.toml | sed -E 's/.*=[[:space:]]*"([^"]+)".*/\1/')
        DB_PASSWORD=$(grep 'db_password' backend/conf.toml | sed -E 's/.*=[[:space:]]*"([^"]+)".*/\1/')
        if [ -z "${DB_NAME}" ]; then
            echo -e "${RED}DB_NAME does not exist.${NC}"
            exit 1
        fi
        if [ -z "${DB_PASSWORD}" ]; then
            echo -e "${RED}DB_PASSWORD does not exist.${NC}"
            exit 1
        fi

        set +e # Disabling error exit because grep trigger an error if no match
        DB_EXISTS=$(psql -lqt | cut -d \| -f 1 | grep -qw ${DB_NAME})
        set -e
        if [ "$DEPLOY_MODE" -gt 0 ] && [ "$DB_EXISTS" ]; then
            echo -e "${YELLOW}!!! WARNING !!!${NC}"
            read -p "Do you really want to flush the DB in production ? (y/N) " response
            if [[ "$response" != "y" ]]; then
                exit 1
            fi
            echo -e "${BLUE}### Preparing a data base back_up ${NC}"
            sudo -iu ${USER} pg_dump -h localhost -p 5432 -d ${DB_NAME} -F c -b -f $(pwd)/${DB_NAME}_backup.db_bk
            # To restore :
            # sudo -iu ${USER} createdb -h localhost -p 5432 ${DB_NAME}
            # sudo -iu ${USER} pg_restore -h localhost -p 5432 -d ${DB_NAME} -v ${DB_NAME}_backup.db_bk
        fi

        echo -e "${BLUE}### Flushing data base${NC}"
        rm -f backend/FoodDemocraty/migrations/000*

        if [ $MAC_ENV = 1 ]; then
            sudo -u $USER dropdb --if-exists ${DB_NAME}
            sudo -u $USER createdb ${DB_NAME}
            sudo -u $USER dropuser --if-exists ${DB_NAME}_admin
            echo "CREATE ROLE ${DB_NAME}_admin PASSWORD '${DB_PASSWORD}' SUPERUSER CREATEDB CREATEROLE LOGIN;" | sudo -u $USER psql -d ${DB_NAME}
        else
            dropdb --if-exists ${DB_NAME}
            createdb ${DB_NAME}
            dropuser --if-exists ${DB_NAME}_admin
            echo "CREATE ROLE ${DB_NAME}_admin PASSWORD '${DB_PASSWORD}' SUPERUSER CREATEDB CREATEROLE LOGIN;" | psql -d ${DB_NAME}
        fi
    fi
fi

echo -e "${BLUE}### Migrating data base${NC}"
python backend/manage.py makemigrations
python backend/manage.py migrate

if [ $INIT_DB = 1 ]
then
    # echo -e "${BLUE}### Initialize data base${NC}"
    # if [ "$DEPLOY_MODE" -gt 0 ]; then
    #     python backend/manage.py loaddata */fixtures/prod/*
    # else
    #     python backend/manage.py loaddata */fixtures/dev/*
    # fi

    echo -e "${BLUE}### Creating admin user${NC}"
    if [ "$DEPLOY_MODE" -gt 1 ]; then
        export DJANGO_SUPERUSER_PASSWORD="0000"
        python backend/manage.py createsuperuser --username=admin --noinput --email=admin@mail.com
    else
        python backend/manage.py createsuperuser --username=admin
    fi
fi

echo -e "${BLUE}### Updating static files${NC}"
python backend/manage.py collectstatic --no-input --clear

echo -e "${GREEN}##################################${NC}"
echo -e "${GREEN}### Deployement successful !!! ###${NC}"
echo -e "${GREEN}##################################${NC}"