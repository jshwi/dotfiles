CYAN	:= $(shell printf '\033[36m')
RESET	:= $(shell printf '\033[m')
REPO 	:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
NAME	:= $(shell basename $(REPO))
SETUP 	:= $(REPO)/setup.py
BIN 	:= $(REPO)/bin
LIBSH	:= $(REPO)/lib
DOTSH	:= $(LIBSH)/dotsh
LIBSH 	:= $(DOTSH)/lib.sh
BASH	:= /bin/bash
PYTHON	:= /bin/python3
NAME	:= $(shell $(PYTHON) $(SETUP) --name)
VERSION := $(shell $(PYTHON) $(SETUP) --version)


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
	@$(BASH) -c "$(BIN)/which-pipenv"


.PHONY: install
install: which  ## Install bin executable
	@$(BASH) -c "source $(LIBSH); install"


.PHONY: docs
docs: which  ## Compile documentation
	@$(BASH) -c "source $(LIBSH); make_html"


.PHONY: tests
tests: which  ## Run unittests
	@$(BASH) -c "source $(LIBSH); run_tests"


.PHONY: clean
clean:  ## Remove all untracked dirs and files
	@$(BASH) -c "source $(LIBSH) --no-install; clean_repo"


.PHONY: uninstall
uninstall: which  ## Uninstall binary
	@$(BASH) -c "source $(LIBSH) --no-install; uninstall"


.PHONY: format
format: which  ## Format all .py project files
	@$(BASH) -c "source $(LIBSH); format_py"


.PHONY: lint
lint: which  ## Show possible .py file corrections
	@$(BASH) -c "source $(LIBSH); lint_files"


.PHONY: coverage
coverage: which  ## Run unittests with coverage
	@$(BASH) -c "source $(LIBSH); run_test_cov"


.PHONY: typecheck
typecheck: which  ## Inspect files for type errors
	@$(BASH) -c "source $(LIBSH); inspect_types"


.PHONY: unused
unused: which  ## Inspect files for unused attributes
	@$(BASH) -c "source $(LIBSH); vulture"


.PHONY: whitelist
whitelist: which  ## Update whitelist.py
	@$(BASH) -c "source $(LIBSH); whitelist"


.PHONY: toc
toc: which  ## Update docs/<PACKAGENAME>.rst
	@$(BASH) -c "source $(LIBSH); make_toc"


.PHONY: requirements
requirements: which  ## Pipfile.lock -> requirements.txt
	@$(BASH) -c "source $(LIBSH); pipfile_to_requirements"


.PHONY: files
files: which  ## Requirements, toc and whitelist
	@$(BASH) -c "source $(LIBSH); make_files"


.PHONY: deploy-docs
deploy-docs: which  ## Deploy Sphinx docs to gh-pages
	@$(BASH) -c "source $(LIBSH); deploy_cov"


.PHONY: deploy-cov
deploy-cov: which  ## Deploy code coverage to Codecov
	@$(BASH) -c "source $(LIBSH); deploy_cov"


.PHONY: build
build: which  ## Run all checks, install and deploy
	@$(BASH) -c "$(BIN)/build-repo"
