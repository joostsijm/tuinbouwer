-include .env
export

build:
	poetry build

init:
	cp example.env .env

install-deps:
	poetry install

install: build
	pip install dist/*.whl

reinstall: build
	pip install dist/*.whl --force-reinstall

start: install
	poetry run flask run

test: install
	poetry run pytest

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

container-build:
	docker build \
		-t $(DOCKER_ORGANIZATION)/$(DOCKER_APP_IMAGE) .

container-save:
	docker save \
		$(DOCKER_ORGANIZATION)/$(DOCKER_APP_IMAGE) -o container.tar

container-start:
	docker run \
		-dp 8000:8000 \
		--name $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE) \
		$(DOCKER_ORGANIZATION)/$(DOCKER_APP_IMAGE)

container-logs:
	docker logs $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

container-stop:
	docker stop $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

container-remove: container-stop
	docker rm $(DOCKER_ORGANIZATION)_$(DOCKER_APP_IMAGE)

container-restart: container-build container-stop container-remove container-start
