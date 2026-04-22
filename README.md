# system_learn

Obsidian-vault: PKM, обучение, литкарточки (`Literature/` с префиксом **Бn**), атомы в `Notes/`, определения в `Definitions/`, служебные реестры в `System/`.

## Клонирование

```bash
git clone <url> system_learn
cd system_learn
```

## Каталог `Sources/`

Папка предназначена для **локальных** PDF и других бинарников; в репозитории закреплён только `Sources/.gitkeep`, содержимое по `.gitignore` не коммитится.

## Obsidian (`.obsidian/`)

В git попадают **манифесты и настройки** (например `app.json`, `appearance.json`, списки плагинов, `manifest.json` плагинов). Не коммитятся: `workspace.json`, бандлы плагинов (`main.js`, стили, `data.json` и т.д.), CSS тем — чтобы не раздувать диффы и не фиксировать машинно-зависимое.

## Скрипты и Makefile

Из корня vault:

| Команда | Назначение |
|--------|------------|
| `make help` | Краткая справка |
| `make literature-backlog` | Пересчитать таблицу stub в `System/literature-backlog.md` |
| `make check-wikilinks` | Проверить, что все цели wikilink разрешаются в существующие `.md` |

Скрипты: `Scripts/literature_backlog.py`, `Scripts/check_wikilinks.py` (Python 3, только стандартная библиотека).

## Правила для агента Cursor

- `.cursor/rules/system_learn-vault.mdc` — соглашения vault (YAML, `card_id`, голос, ссылки).
- `.cursor/rules/system_learn-sources.mdc` — workflow разбора источников и оформления литкарточек.
- `.cursor/rules/system_learn-insights.mdc` — поиск инсайтов, неожиданных связей и кандидатов в новые заметки/кластеры.
