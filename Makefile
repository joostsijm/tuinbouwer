-include .env
export

main: build

.PHONY: init
init:
	cp example.env .env

.PHONY: build
build:
	poetry build

.PHONY: install
install: build
	pip install dist/*.whl

.PHONY: reinstall
reinstall: build
	pip install dist/*.whl --force-reinstall

.PHONY: start
start: install
	poetry run flask run

.PHONY: docker-build
docker-build:
	docker build \
		-t $(DOCKER_ORGANIZATION)/$(DOCKER_APP_IMAGE) .

.PHONY: docker-start
docker-start:
	docker run \
		--name $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE) \
		$(DOCKER_ORGANIZATION)/$(DOCKER_APP_IMAGE)

.PHONY: docker-logs
docker-logs:
	docker logs $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

.PHONY: docker-stop
docker-stop:
	docker stop $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

.PHONY: docker-remove
docker-remove: docker-stop
	docker rm $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

.PHONY: docker-restart
docker-restart: docker-build docker-stop docker-remove docker-start
