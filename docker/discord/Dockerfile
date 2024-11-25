# syntax=docker/dockerfile:1
FROM base
WORKDIR /app

# Copying project sources
COPY DiscordBot/ /app/DiscordBot
COPY xpt_utils/ /app/xpt_utils

# Copying environnement files
COPY docker/discord /app/DiscordBot/
COPY docker/discord/entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]