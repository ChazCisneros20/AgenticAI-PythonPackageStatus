# PackageUpdateSearch

Python package with an interactive CLI around **`PackageUpdateSearch.RT`** (ReleaseTrain Reddit fetch) and **`PackageUpdateSearch.agenticRT`** (Ollama agent with `package_update` as a tool).

## Overview

- **`app.py`** — Interactive REPL: `argparse` subcommands (`package-update`, `agent-update`, `help`, `exit`, etc.).
- **`RT.py`** — `Update.package_update()` calls `https://releasetrain.io/api/reddit/by-subreddit` and formats plain-text post blocks (`[URL: ]`, `[TITLE: ]`, …).
- **`agenticRT.py`** — `AgentUpdate.agent_update_conversation()` runs Ollama (`llama3.2:3b`), executes tool calls via `TOOL_REGISTRY`, prints fetched Reddit URLs from the latest tool message, then prints the model reply.

## Requirements

- Python **3.9+**
- **Ollama** running locally; pull the chat model: `ollama pull llama3.2:3b`
- Python deps (see **`pyproject.toml`**): **`requests`**, **`ollama`**

## Installation

```bash
pip install -e .
```

Optional dev/tests:

```bash
pip install -e ".[test]"
```

## Running the CLI

After install:

```bash
python -m PackageUpdateSearch.app
```

From the repo (package must resolve as `PackageUpdateSearch`; installing editable is easiest):

```bash
cd src
python -m PackageUpdateSearch.app
```

## CLI commands

| Command | Behavior |
|--------|----------|
| `package-update ...` | Runs `RT.Update.package_update` with flags (`--q`, `--min-score`, …). |
| `agent-update` | Starts `AgentUpdate.agent_update_conversation()`. |
| `help` | Lists commands (see `print_help()`). |
| `exit` | Quits the REPL. |

**`-v` / `--version`** on the root parser: e.g. `python -m PackageUpdateSearch.app --version`.

The subparsers **`get-request`** and **`capstone`** exist for `--help`, but **`handle_command`** in **`app.py`** does not run them yet—only **`package-update`**, **`agent-update`**, **`help`**, **`exit`**, and a legacy **`elif`** for `-v` as a fake command.

### `package-update`

Targets `https://releasetrain.io/api/reddit/by-subreddit`.

Typical flags: `--q` (default `programming,technology`), `--min-score`, `--min-comments`, `--limit`, `--page`, `--fields`, `--ascending`.

Example:

```text
> package-update --q Python --min-score 30 --limit 10
```

## Package API (library)

```python
from PackageUpdateSearch.RT import Update

text = Update.package_update(q="programming,technology", limit=10)
# Update.help()  # prints usage text
```

Agent entry:

```python
from PackageUpdateSearch.agenticRT import SYSTEM_PROMPT, TOOL_REGISTRY, AgentUpdate

AgentUpdate.agent_update_conversation(SYSTEM_PROMPT, TOOL_REGISTRY)
```

## Tests

```bash
pytest tests/
```
