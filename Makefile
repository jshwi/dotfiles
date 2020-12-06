CYAN		:= $(shell printf '\033[36m')
RESET		:= $(shell printf '\033[m')
REPO 		:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
NAME		:= $(shell basename $(REPO))
SETUP 		:= $(REPO)/setup.py
MAKEFILE	:= $(REPO)/lib/makefile
BASH		:= /bin/bash
PYTHON		:= /bin/python3
NAME		:= $(shell $(PYTHON) $(SETUP) --name)
VERSION 	:= $(shell $(PYTHON) $(SETUP) --version)


.PHONY: help
help:  ## Show this help message and exit
	@echo "$(CYAN)$(BOLD)$(NAME) v$(VERSION)$(RESET)"
	@echo "$(CYAN).$(RESET) usage:         make [TARGET]"
	@echo "$(CYAN).$(RESET) requirements:  make,python3.8,pipenv"
	@echo "$(CYAN)----------------------------------------------------$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk \
	'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'


.PHONY: which
which:  ## Check that pipenv is installed
	@$(BASH) -c "$(MAKEFILE)/which"


.PHONY: install
install: which  ## Install bin executable
	@$(BASH) -c "$(MAKEFILE)/install"


.PHONY: docs
docs: which  ## Compile documentation
	@$(BASH) -c "$(MAKEFILE)/html"


.PHONY: tests
tests: which  ## Run unittests
	@$(BASH) -c "$(MAKEFILE)/tests"


.PHONY: clean
clean:  ## Remove all untracked dirs and files
	@$(BASH) -c "$(MAKEFILE)/clean"


.PHONY: uninstall
uninstall: which  ## Uninstall binary
	@$(BASH) -c "$(MAKEFILE)/uninstall"


.PHONY: format
format: which  ## Format all .py project files
	@$(BASH) -c "$(MAKEFILE)/format"


.PHONY: lint
lint: which  ## Show possible .py file corrections
	@$(BASH) -c "$(MAKEFILE)/lint"


.PHONY: coverage
coverage: which  ## Run unittests with coverage
	@$(BASH) -c "$(MAKEFILE)/coverage"


.PHONY: typecheck
typecheck: which  ## Inspect files for type errors
	@$(BASH) -c "$(MAKEFILE)/typecheck"


.PHONY: unused
unused: which  ## Inspect files for unused attributes
	@$(BASH) -c "$(MAKEFILE)/unused"


.PHONY: whitelist
whitelist: which  ## Update whitelist.py
	@$(BASH) -c "$(MAKEFILE)/whitelist"


.PHONY: toc
toc: which  ## Update docs/<PACKAGENAME>.rst
	@$(BASH) -c "$(MAKEFILE)/toc"


.PHONY: requirements
requirements: which  ## Pipfile.lock -> requirements.txt
	@$(BASH) -c "$(MAKEFILE)/requirements"


.PHONY: files
files: which  ## Requirements, toc and whitelist
	@$(BASH) -c "$(MAKEFILE)/files"


.PHONY: deploy-docs
deploy-docs: which  ## Deploy Sphinx docs to gh-pages
	@$(BASH) -c "$(MAKEFILE)/deploy-docs"


.PHONY: deploy-cov
deploy-cov: which  ## Deploy code coverage to Codecov
	@$(BASH) -c "$(MAKEFILE)/deploy-cov"


.PHONY: build
build: which  ## Run all checks, install and deploy
	@$(BASH) -c "$(MAKEFILE)/build"
