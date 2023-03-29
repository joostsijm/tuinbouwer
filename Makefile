-include .env
export

main: build

.PHONY: init
init:
	cp example.env .env

.PHONY: install-deps
install-deps:
	poetry install

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

.PHONY: test
test: install
	poetry run pytest

.PHONY: container-build
container-build:
	docker build \
		-t $(DOCKER_ORGANIZATION)/$(DOCKER_APP_IMAGE) .

.PHONY: container-start
container-start:
	docker run \
		-dp 8000:8000 \
		--name $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE) \
		$(DOCKER_ORGANIZATION)/$(DOCKER_APP_IMAGE)

.PHONY: container-logs
container-logs:
	docker logs $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

.PHONY: container-stop
container-stop:
	docker stop $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

.PHONY: container-remove
container-remove: container-stop
	docker rm $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

.PHONY: container-restart
container-restart: container-build container-stop container-remove container-start
