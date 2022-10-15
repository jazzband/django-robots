WATCH_FILES= find . -type f -not -path '*/\.*' | grep -i '.*[.]py$$' 2> /dev/null
PY_FILES= find . -type f -not -path '*/\.*' -and -not -path '*/settings\/*' -and -not -path '*/migrations\/*' | grep -i '.*[.]py$$'
SHELL := /bin/bash


entr_warn:
	@echo "----------------------------------------------------------"
	@echo "     ! File watching functionality non-operational !      "
	@echo "                                                          "
	@echo "Install entr(1) to automatically run tasks on file change."
	@echo "See http://entrproject.org/                               "
	@echo "----------------------------------------------------------"

build_docs:
	pushd docs; $(MAKE) html; popd

watch_docs:
	pushd docs; $(MAKE) watch_docs; popd

start:
	$(MAKE) test; poetry run ptw .

test:
	poetry run py.test $(test)

watch_test:
	if command -v entr > /dev/null; then ${WATCH_FILES} | entr -c $(MAKE) test; else $(MAKE) test entr_warn; fi

start_docs:
	$(MAKE) -C docs start

design_docs:
	$(MAKE) -C docs design

black:
	poetry run black `${PY_FILES}`

isort:
	poetry run isort `${PY_FILES}`

flake8:
	poetry run flake8

watch_flake8:
	if command -v entr > /dev/null; then ${WATCH_FILES} | entr -c $(MAKE) flake8; else $(MAKE) flake8 entr_warn; fi

mypy:
	poetry run mypy `${PY_FILES}`

watch_mypy:
	if command -v entr > /dev/null; then ${PY_FILES} | entr -c $(MAKE) mypy; else $(MAKE) mypy entr_warn; fi

format_markdown:
	prettier --parser=markdown -w *.md docs/*.md docs/**/*.md CHANGES
