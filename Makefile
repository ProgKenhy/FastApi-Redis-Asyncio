THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs-app logs-redis ps login-redis login-app redis-shell test

help:
	@echo "Available targets:"
	@echo "  build          - Build the Docker images"
	@echo "  up             - Start the containers in detached mode"
	@echo "  start          - Start existing containers"
	@echo "  down           - Stop and remove containers and networks"
	@echo "  destroy        - Stop and remove containers, networks, images, and volumes"
	@echo "  stop           - Stop running containers"
	@echo "  restart        - Restart containers"
	@echo "  logs           - View all container logs (last 100 lines)"
	@echo "  logs-app       - View app container logs (last 100 lines)"
	@echo "  logs-redis     - View redis container logs (last 100 lines)"
	@echo "  ps             - List running containers"
	@echo "  login-redis    - Open a shell in the redis container"
	@echo "  login-app      - Open a shell in the app container"
	@echo "  redis-shell    - Open a Redis CLI shell"
	@echo "  test           - Run connection tests"

build:
	docker-compose -f docker-compose.yml build $(c)

up:
	docker-compose -f docker-compose.yml up -d $(c)

start:
	docker-compose -f docker-compose.yml start $(c)

down:
	docker-compose -f docker-compose.yml down $(c)
	docker network prune --force

destroy:
	docker-compose -f docker-compose.yml down -v --rmi all $(c)

stop:
	docker-compose -f docker-compose.yml stop $(c)

restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)

logs:
	docker-compose -f docker-compose.yml logs --tail=100 -f $(c)

logs-app:
	docker-compose -f docker-compose.yml logs --tail=100 -f app

logs-redis:
	docker-compose -f docker-compose.yml logs --tail=100 -f redis

ps:
	docker-compose -f docker-compose.yml ps

login-redis:
	docker-compose -f docker-compose.yml exec redis sh

login-app:
	docker-compose -f docker-compose.yml exec app sh

redis-shell:
	docker-compose -f docker-compose.yml exec redis redis-cli -a $${REDIS_PASSWORD}

test:
	@echo "Testing Redis connection..."
	docker-compose -f docker-compose.yml exec redis redis-cli -a $${REDIS_PASSWORD} ping
	@echo "Testing API connection..."
	curl -s http://localhost:8000/ | head -c 100
	@echo ""
	@echo "All tests passed!"

stats:
	docker stats task_redis task_app

network-info:
	docker network inspect app_network

volume-info:
	docker volume ls
	docker volume inspect task_redis_data

clean:
	docker system prune -f
	docker volume prune -f

rebuild:
	docker-compose -f docker-compose.yml up -d --build --force-recreate $(c)

follow-%:
	docker-compose -f docker-compose.yml logs --tail=100 -f $*