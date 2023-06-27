BLACK ?= \033[0;30m
RED ?= \033[0;31m
GREEN ?= \033[0;32m
YELLOW ?= \033[0;33m
BLUE ?= \033[0;34m
PURPLE ?= \033[0;35m
CYAN ?= \033[0;36m
GRAY ?= \033[0;37m
WHITE ?= \033[1;37m
COFF ?= \033[0m

.PHONY: all shell build build-node coverage-node coverage-django coverage docker help load_initial_data migrate quality setup superuser test-node test-django test install-npm-dependencies runserver makemigrations eslint eslint-fix lint-django lint-django-fix format

all: help

help:
	@echo -e "\n$(WHITE)Available commands:$(COFF)"
	@echo -e "$(CYAN)make setup$(COFF)            - Sets up the project in your local machine."
	@echo -e "                        This includes building Docker containers and running migrations."
	@echo -e "$(CYAN)make runserver$(COFF)        - Runs the django app in the container, available at http://127.0.0.1:8000"
	@echo -e "$(CYAN)make migrate$(COFF)          - Runs django's migrate command in the container"
	@echo -e "$(CYAN)make makemigrations$(COFF)   - Runs django's makemigrations command in the container"
	@echo -e "$(CYAN)make superuser$(COFF)        - Runs django's createsuperuser command in the container"
	@echo -e "$(CYAN)make shell$(COFF)            - Starts a Linux shell (bash) in the django container"
	@echo -e "$(CYAN)make test$(COFF)             - Runs automatic tests on your python code"
	@echo -e "$(CYAN)make coverage$(COFF)         - Runs code test coverage calculation"
	@echo -e "$(CYAN)make quality$(COFF)          - Runs code quality tests on your code"
	@echo -e "$(CYAN)make format$(COFF)           - Runs code formatters on your code"


shell:
	@echo -e "$(CYAN)Starting Bash in the django container:$(COFF)"
	@docker-compose run --rm django bash

build:
	@echo -e "$(CYAN)Creating Docker images:$(COFF)"
	@docker-compose build


runserver:
	@echo -e "$(CYAN)Starting Docker container with the app.$(COFF)"
	@docker-compose up
	@echo -e "$(CYAN)App ready and listening at http://127.0.0.1:8000.$(COFF)"

setup: build install-npm-dependencies build-node migrate
	@echo -e "$(GREEN)===================================================================="
	@echo "SETUP SUCCEEDED"
	@echo -e "Run 'make runserver' to start the Django development server and the node server.$(COFF)"

test-django:
	@echo -e "$(CYAN)Running automatic django tests:$(COFF)"
	@docker-compose run --rm django py.test

test: test-node test-django
	@echo -e "$(GREEN)All tests passed.$(COFF)"

coverage-node:
	@echo -e "$(CYAN)Running automatic code coverage check for JavaScript:$(COFF)"
	@docker-compose run --rm node npm run test --coverage

coverage-django:
	@echo -e "$(CYAN)Running automatic code coverage check for Python:$(COFF)"
	@docker-compose run --rm django sh -c "coverage run -m py.test && coverage html && coverage report"

coverage: coverage-django
	@echo -e "$(GREEN)Coverage reports generated:"
	@echo "- Python coverage: projement/coverage_html/"

makemigrations:
	@echo -e "$(CYAN)Running django makemigrations:$(COFF)"
	@docker-compose run --rm django ./manage.py makemigrations $(cmd)

migrate:
	@echo -e "$(CYAN)Running django migrations:$(COFF)"
	@docker-compose run --rm django ./manage.py migrate $(cmd)

superuser:
	@echo -e "$(CYAN)Creating Docker images:$(COFF)"
	@docker-compose run --rm django ./manage.py createsuperuser
