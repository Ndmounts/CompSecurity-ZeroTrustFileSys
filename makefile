PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

reqs = \
	cryptography \
	pyopenssl
build:
	$(PIP) install --upgrade pip
	$(PIP) install $(reqs)
	./generate-certs.sh
