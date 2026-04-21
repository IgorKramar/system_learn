# Vault system_learn — вспомогательные цели (cwd = корень vault)
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PY := python3

.PHONY: help literature-backlog check-wikilinks

help:
	@echo "Targets:"
	@echo "  make literature-backlog  — пересчитать таблицу stub в System/literature-backlog.md"
	@echo "  make check-wikilinks      — проверить разрешимость wikilink-целей по vault"

literature-backlog:
	$(PY) "$(ROOT)Scripts/literature_backlog.py" --write

check-wikilinks:
	$(PY) "$(ROOT)Scripts/check_wikilinks.py"
