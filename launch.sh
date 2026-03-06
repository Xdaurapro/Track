docker compose -f docker-compose.yml down
docker compose -f docker-compose.yml build --no-cache unobot
docker compose -f docker-compose.yml up -d --force-recreate unobot
docker logs -f unobot