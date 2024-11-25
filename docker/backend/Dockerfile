# syntax=docker/dockerfile:1
FROM base
WORKDIR /app

# Copying project sources
COPY backend/ /app/backend
COPY xpt_utils/ /app/xpt_utils
COPY deploy.sh /app/
RUN chmod +x /app/deploy.sh

# Copying environnement files
COPY docker/backend/django.conf /app/backend/
COPY docker/backend/entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"] 