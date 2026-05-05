# PackageUpdateSearch CLI (`app.py`)

## Overview

`app.py` is an interactive CLI built with **`argparse`**. It dispatches to:

- **`RT.Update.package_update`** for **`package-update`**
- **`AgentUpdate.agent_update_conversation`** (from **`agenticRT`**) for **`agent-update`**

The session runs until **`exit`** or Ctrl+C.

## Architecture

### `create_parser()`

Builds one **`ArgumentParser`** and subparsers: **`package-update`**, **`get-request`**, **`capstone`**, **`agent-update`**, **`help`**, **`exit`**, plus root **`-v` / `--version`**.

### `handle_command(parser, command_line)`

Splits the user line, **`parse_args`**, and branches on **`args.command`**. Catches **`SystemExit`** from argparse so a bad line does not kill the CLI session. Returns **`False`** only for **`exit`**.

**Implemented in `handle_command` today:** **`package-update`**, **`agent-update`**, **`help`**, and a **`elif args.command == '-v'`** branch. Subparsers **`get-request`** and **`capstone`** are registered but **not** handled—those commands parse successfully and currently do nothing.

### `print_help()`

Startup banner commands match this list (**no** **`get-request`** / **`capstone`** in the banner):

- **`package-update`**, **`help`**, **`-v`**, **`agent-update`**, **`exit`**

### `main()`

Creates the parser, prints the welcome line and **`print_help()`**, loops on **`input("> ")`** → **`handle_command`**.

## Command reference

### `package-update`

Calls **`RT.Update.package_update`** with the parsed flags. Same ReleaseTrain endpoint as the library.

See **`README.md`** / **`PACKAGE_DOCUMENTATION.md`** for flags.

### `agent-update`

Runs **`AgentUpdate.agent_update_conversation(SYSTEM_PROMPT, TOOL_REGISTRY)`**. When that returns, prints **`Agent conversation ended.`** and **`print_help()`** again.

### `help` / `exit`

As described in **`print_help()`** and **`handle_command`**.

### `get-request` / `capstone` (limited)

Subcommands exist for **`--help`**. Until **`handle_command`** gains branches, interactive use has **no effect**.

## Error handling

- Empty **`>`** input is skipped.
- **`SystemExit`** from argparse is swallowed inside **`handle_command`**.
- **`RT.package_update`** returns error/advisory strings instead of raising for HTTP issues (see **`RT.py`**).
- **`KeyboardInterrupt`** → **`Goodbye!`** and exit loop.

## Integration (actual wiring)

| CLI command | Implementation |
|-------------|----------------|
| `package-update` | **`RT.Update.package_update`** |
| `agent-update` | **`agenticRT.AgentUpdate.agent_update_conversation`** |
| `help` / `exit` | **`print_help`** / loop exit |

## Running

```bash
pip install -e .
python -m PackageUpdateSearch.app
```

From repo **`src`** with **`PYTHONPATH`** set if needed:

```bash
cd src
python -m PackageUpdateSearch.app
```

**Note:** Running **`python app.py`** directly inside the package folder can fail imports; prefer **`python -m PackageUpdateSearch.app`** from an environment where the package is installed.
