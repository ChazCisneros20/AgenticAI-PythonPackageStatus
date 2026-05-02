# PackageUpdateSearch Documentation

## Overview

PackageUpdateSearch is an installable Python package (Hatchling / PEP 621) that:

- Fetches Reddit posts via the ReleaseTrain HTTP API (`Update.package_update` in **`RT.py`**).
- Exposes an **interactive CLI** (`PackageUpdateSearch.app`) built on **`argparse`** subcommands.
- Optionally runs an **Ollama** agent (**`agenticRT.py`**) with **`llama3.2:3b`** and native **`tools=[Update.package_update]`**, with **`TOOL_REGISTRY`** restricting which Python callables run.

Layout: **`src/PackageUpdateSearch/`** (`RT.py`, `app.py`, `agenticRT.py`). There is no top-level **`cli.py`**; the CLI is the **`app`** module.

---

## Installation and dependencies

Declared in **`pyproject.toml`**:

- **`[project.dependencies]`:** `requests`, `ollama`
- **`[project.optional-dependencies].test`:** `pytest`
- **`requires-python`:** `>=3.9`

```text
pip install -e .
pip install -e ".[test]"   # optional, for tests
```

---

## Running the CLI

```bash
python -m PackageUpdateSearch.app
```

The REPL prints a welcome line and **`print_help()`**, then reads lines like **`> package-update ...`** until **`exit`** or Ctrl+C.

**Version:** root parser defines **`-v` / `--version`** (e.g. `python -m PackageUpdateSearch.app --version`). Inside the **`>`** loop, input is split and parsed as a single line (e.g. `package-update --limit 5`).

---

## Available commands (`app.py`)

| Command | Purpose |
|---------|---------|
| `package-update` | Calls **`RT.Update.package_update(...)`** with CLI flags. |
| `agent-update` | Runs **`AgentUpdate.agent_update_conversation(SYSTEM_PROMPT, TOOL_REGISTRY)`**. |
| `help` | **`print_help()`** command list. |
| `exit` | Ends the session. |

**Subparsers `get-request` and `capstone`** are registered (so **`get-request --help`** works) but **`handle_command`** does not implement those branches yet—they parse but perform no action.

**`print_help()`** advertises **`package-update`**, **`help`**, **`-v`**, **`agent-update`**, **`exit`** (not **`get-request`** / **`capstone`**).

**`package-update`:** **`--ascending`** is **`store_true`**; **`Update.package_update`** expects **`ascending`** **`0`** or **`1`**. The CLI passes a **boolean**; **`int(bool)`** inside **`package_update`** maps it.

---

## `package-update` / `Update.package_update`

**CLI defaults** (`app.py`):

| Flag | CLI default |
|------|----------------|
| `--q` | `programming,technology` |
| `--min-score` | `50` |
| `--min-comments` | `10` |
| `--limit` | `25` |
| `--page` | `2` |
| `--fields` | `url,score,tag,title,subreddit,author_description` |
| `--ascending` | omitted → descending sort |

**Python API** method defaults in **`RT.py`** may differ (e.g. **`q`**, **`page`**) when calling **`Update.package_update`** directly.

### HTTP 200 with no rows

If **`data`** is **`null`**, **`[]`**, or missing in a way that yields no list items, **`package_update`** returns an advisory string such as:

- `Currently unable to search updates <Response data is None:> ...`
- `Currently unable to search updates <Response data is empty:> ...`

(not formatted post blocks). ReleaseTrain can return **`200`** with **`data: []`** when nothing is indexed for the query (e.g. casing / subreddit not in index).

### Non-200

Returns a string including **`Response code not 200:`** and the status code.

### Successful posts

Plain-text blocks with lines **`[URL: ]`**, **`[SCORE: ]`**, **`[TITLE: ]`**, **`[SUBREEDDIT: ]`**, etc. (see **`RT.py`**).

---

## `Update.help()`

Prints a static description of **`package_update`** to stdout.

---

## AI agent (`agenticRT.py`)

### Behavior

- **`ollama.Client().chat`** with **`model='llama3.2:3b'`**, **`tools=[Update.package_update]`**.
- On **`tool_calls`**, Python runs **`TOOL_REGISTRY[function_name](**args)`** and appends **`role: tool`** messages.
- On an assistant turn **without** **`tool_calls`**:
  1. **`AgentUpdate.extract_urls_from_tool_result(messages)`** scans the **latest** **`tool`** message in **`messages`** for lines starting with **`[URL: ]`**, collects URLs.
  2. If any: prints **`--- All Fetched Links ---`**, bullet URLs, **`--- End of Links ---`** (or a short message when none).
  3. Prints **`response.message.content`** (model summary).

So **links are listed from the tool payload before the model text** (current implementation order).

### Prerequisites

- **Ollama** at **`http://localhost:11434`** (**`is_ollama_running()`** checks **`GET /api/tags`**).
- **`ollama pull llama3.2:3b`** to match **`model=`** in **`client.chat`**.

### `reset_each_query`

Default **`True`**. After each completed loop iteration, when the user types the next line, **`messages`** is reset to **`[system, user]`** with the new input so prior tool/assistant context does not carry over. Pass **`reset_each_query=False`** to keep full **`messages`** history (advanced).

### Entry points

```text
> agent-update
```

```python
from PackageUpdateSearch.agenticRT import SYSTEM_PROMPT, TOOL_REGISTRY, AgentUpdate

AgentUpdate.agent_update_conversation(SYSTEM_PROMPT, TOOL_REGISTRY)
```

### `SYSTEM_PROMPT`

Defines Mode 1 (tool calling) vs Mode 2 (summarization after **`tool`**), empty-result handling for ReleaseTrain advisory strings, anti-hallucination / Reddit URL rules, etc.

### Tool registry

```python
TOOL_REGISTRY = {
    "package_update": Update.package_update,
}
```

---

## Agent loop (simplified)

1. **`is_ollama_running()`** — else print help and return.
2. **`client.chat`** → append assistant message.
3. If **`tool_calls`**: execute tools, append **`tool`** contents, **`continue`**.
4. Else: **`extract_urls_from_tool_result(messages)`** → print link block if present → **`print(response.message.content)`**.
5. Read next user line; if **`reset_each_query`**, rebuild **`messages`**; else **`append`** user.

---

## Design notes

- Only **`TOOL_REGISTRY`** functions run as tools.
- **`extract_urls_from_tool_result`** only parses **`[URL: ]`** lines; it does not fetch URLs.

---

## Summary

**`pyproject.toml`** dependencies, **`RT.Update`** + ReleaseTrain, **`app`** REPL, **`AgentUpdate`** + Ollama **`llama3.2:3b`**, optional link listing from the last tool message before the model reply.
