MAKEFLAGS = --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.DEFAULT_GOAL := help
ROOT := $(shell cd "$$(dirname "$(strip $(MAKEFILE_LIST))")" && pwd)

.PHONY: help install apply update cleanup
help: ## Display this help screen
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z._-]+:.*?## / {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' "$(strip $(MAKEFILE_LIST))"

install: ## Install prerequisites, packages, dotfiles, and settings
	"$(ROOT)/install"

apply: ## Reapply links and configured application settings
	"$(ROOT)/install" apply

update: ## Update the repository, packages, settings, and shell plugins
	"$(ROOT)/install" update

cleanup: ## Remove cached and unused package data
	"$(ROOT)/install" cleanup
