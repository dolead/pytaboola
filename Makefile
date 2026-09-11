# Generic Makefile for Poetry-managed Python libraries
# Version: 2.0.0
#
# Managed by skel/pylib — do not edit in place.
# Update via: cd <skel>/pylib && make sync REPO=<this repo>
#
# Usage:
#   make test              - run test suite via pytest
#   make test-cov          - run tests with coverage report
#   make format            - auto-format code with isort and black
#   make lint              - run all linters (isort, black, flake8, pycodestyle, pylint, mypy)
#   make build             - clean, lint, test, then build distribution
#   make release           - prompt for bump type, commit, and git tag
#   make publish           - build and publish to the configured PyPI repository
#
# Project-specific configuration lives in .vars.mk — the only file
# that changes per project (see skel/pylib/templates/vars.mk).

include .vars.mk

# ──────────────────────────────────────────────
# Defaults for optional .vars.mk variables
# ──────────────────────────────────────────────

TEST_CMD ?= poetry run pytest
TYPE_CODE ?= $(CODE)
TAG_PREFIX ?=
PUBLISH_REPOSITORY ?=

# Optional --repository flag for `poetry publish`; empty means public PyPI
PUBLISH_ARGS = $(if $(PUBLISH_REPOSITORY),--repository $(PUBLISH_REPOSITORY),)

# ──────────────────────────────────────────────
# Targets
# ──────────────────────────────────────────────

.PHONY: clean test test-cov lint format build publish release

clean:
	rm -rf build dist .coverage htmlcov .mypy_cache .pytest_cache *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true

test:
	$(TEST_CMD)

test-cov:
	$(TEST_CMD) --cov --cov-report=html --cov-report=term-missing

# Format: auto-fix import order and code style
format:
	poetry run isort $(CODE)
	poetry run black $(CODE)

# Lint: every linter runs on every project; each must pass before the next.
# PYCODESTYLE_IGNORE / PYLINT_DISABLE only relax rules, they never skip a linter.
lint:
	poetry check
	poetry run isort --check-only --diff $(CODE)
	poetry run black --check --verbose $(CODE)
	poetry run flake8 $(CODE)
	poetry run pycodestyle $(if $(PYCODESTYLE_IGNORE),--ignore=$(PYCODESTYLE_IGNORE),) $(CODE)
	poetry run pylint $(CODE) $(if $(PYLINT_DISABLE),-d $(PYLINT_DISABLE),)
	poetry run mypy --ignore-missing-imports $(TYPE_CODE)

build: clean lint test
	poetry build

# Publish: build then push to the configured PyPI repository.
# PUBLISH_REPOSITORY (in .vars.mk) selects the target; empty means public PyPI.
publish: build
	poetry publish $(PUBLISH_ARGS)

# ──────────────────────────────────────────────
# Release: bump version, commit, and tag
# ──────────────────────────────────────────────
# Bumps the version in pyproject.toml via poetry, commits the change,
# and creates a git tag ($(TAG_PREFIX)X.Y.Z). Does NOT push — push
# manually or let CI handle it.

release:
	@echo "Current version: $$(poetry version -s)"
	@printf "Bump type [patch/minor/major]: " && read BUMP && \
	case "$$BUMP" in \
		patch|minor|major) ;; \
		*) echo "Invalid bump type: $$BUMP"; exit 1 ;; \
	esac && \
	poetry version "$$BUMP" && \
	TAG="$(TAG_PREFIX)$$(poetry version -s)" && \
	git add pyproject.toml && \
	git commit -m "release $$TAG" && \
	git tag "$$TAG" && \
	echo "Release $$TAG ready. Run 'git push && git push --tags' then 'make publish' to deploy."
