
NAME = interpreters
VERSION = $(shell python3 -c "import $(NAME); print($(NAME).__version__)")
TARBALL = $(CURDIR)/dist/$(NAME)-$(VERSION).tar.gz

$(CURDIR)/build:
	@echo "building"
	python3 $(CURDIR)/setup.py build

$(TARBALL): $(CURDIR)/build
	@echo "generating tarball: $(TARBALL)"
	python3 $(CURDIR)/setup.py sdist
	#python3 $(CURDIR)/setup.py bdist
	#python3 $(CURDIR)/setup.py bdist_wheel

.PHONY: deps
deps:
	python3 -m pip install flake8

.PHONY: build
build: $(CURDIR)/build

.PHONY: dist
dist: $(TARBALL)

.PHONY: install
install: $(TARBALL)
	@echo "installing "
	python3 $(CURDIR)/setup.py install

.PHONY: publish
publish: $(TARBALL)
	@echo "uploading to the cheeseshop"
	@echo "not implemented yet"
	#python3 $(CURDIR)/setup.py register
	#python3 $(CURDIR)/setup.py upload

.PHONY: lint
lint:
	@echo "linting the project"
	python3 $(CURDIR)/setup.py check
	python3 -m flake8 --ignore=E121,E123,E126,E226,E24,E704,E265 $(CURDIR)

.PHONY: 
test: lint
	@echo "running unit tests"
	python3 -m unittest discover -t $(CURDIR) -s $(CURDIR)/tests

.PHONY: clean
clean:
	@echo "cleaning up the project"
	-find $(CURDIR) -name __pycache__ -type d -exec rm -rf "{}" \;
	-rm -f $(CURDIR)/MANIFEST
	-rm -rf $(CURDIR)/build
	-rm -rf $(CURDIR)/dist
	-python3 $(CURDIR)/setup.py clean
