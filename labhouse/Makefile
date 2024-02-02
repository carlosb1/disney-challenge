# Makefile for Django project

# Set the default target to runserver
.DEFAULT_GOAL := runserver


SHELL := /bin/bash

# Variables
VIRT := venv
PYTHON := python
PIP := pip
MANAGE := ./manage.py
SETTINGS := labhouse.settings

#TODO check settings configuration

create_virtual:
	python3 -m venv ../$(VIRT)
setup_virtual:
	source ../$(VIRT)/bin/activate
# Install project dependencies
install: setup_virtual
	$(PIP) install -r requirements.txt
# Create database tables
migrate: install
	$(PYTHON) $(MANAGE) makemigrations
	$(PYTHON) $(MANAGE) migrate --settings=$(SETTINGS)
# Run development server
runserver: setup_virtual
	$(PYTHON) $(MANAGE) runserver --settings=$(SETTINGS)
# Run tests
test: setup_virtual
	$(PYTHON) $(MANAGE) test --settings=$(SETTINGS)
	$(PYTHON) $(MANAGE) test core/ --settings=$(SETTINGS)

start_docker:
	docker build -t app-labhouse .
	docker run -p 8000:8000 app-labhouse

# Clean up pycache files
clean:
	find . -name "__pycache__" -exec rm -rf {} \;
	find . -name "*.pyc" -exec rm -f {} \;
