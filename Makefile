APP_NAME=news
DC_FILE = docker-compose.yaml

dc-build::
	docker-compose -f $(DC_FILE) build 
dc-up::
	docker-compose -f $(DC_FILE) up -d
dc-down::
	docker-compose -f $(DC_FILE) down
dc-clean::
	docker-compose -f $(DC_FILE) down -v
