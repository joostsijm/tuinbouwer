-include .env
export

main: build

.PHONY: install-deps
install-deps:
	npm install

.PHONY: build
build: install-deps
	export NODE_OPTIONS=--openssl-legacy-provider; npm run build

.PHONY: start
start:
	export NODE_OPTIONS=--openssl-legacy-provider; npm run serve
