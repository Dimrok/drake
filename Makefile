# Helpers.
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(notdir $(patsubst %/,%,$(dir $(MKFILE_PATH))))

# Project name.
NAME := $(CURRENT_DIR)

requirements:
	pip3 install --requirement requirements-dev.txt 1>/dev/null

# -include requirements

check:
	cd _build && ./drake //check
	# flake8 --max-complexity 10 --ignore E111,E251 src/drake

pylint:
	pylint --rcfile .pylintrc src
	pylint --rcfile .pylintrc tests

typecheck:
	mypy --ignore-missing-imports src/$(NAME)

tests:
	py.test -v $(TESTS)

coverage:
	py.test --cov $(NAME) --cov-report term-missing $(TESTS)

htmlcov:
	py.test --cov $(NAME) --cov-report html $(TESTS)
	rm -rf /tmp/htmlcov && mv htmlcov /tmp/
	open /tmp/htmlcov/index.html

doccheck:
	doc8 docs/source
	$(MAKE) -C docs linkcheck
	$(MAKE) -C docs html

prcheck: check pylint coverage doccheck typecheck

cleanup:
	@rm -rf .coverage
	@rm -rf .pytest_cache

all: check
