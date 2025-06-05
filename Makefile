latest: 1.0

all: 1.0

1.0-LANGS := $(shell cd 4.0 && git status --porcelain | sed 's/[ A-Z?]\+ \"\?4.0\///g' | sed 's/\/.*//g' | sed -n '/^\(ar\|de\|en\|es\|fr\|pt\|ru\|zh-cn\)/p' | tr '\n' ' ')

1.0: docker
	docker run --rm --user $(id -u):$(id -g) -v "`pwd`/5.0:/data" -v "`pwd`/docker:/scripts" -e "TARGET=5.0" -e "FORMATS=$(FORMATS)" ghcr.io/owasp/asvs/documentbuilder:latest
1.0-clean: docker
	docker run --rm --user $(id -u):$(id -g) -v "`pwd`/5.0:/data" -v "`pwd`/docker:/scripts" -e "TARGET=clean" -e "FORMATS=$(FORMATS)" ghcr.io/owasp/asvs/documentbuilder:latest

.PHONY: 1.0 1.0-clean
docker:
	docker pull ghcr.io/owasp/asvs/documentbuilder:latest || docker build --pull --tag ghcr.io/owasp/asvs/documentbuilder:latest --network host docker
