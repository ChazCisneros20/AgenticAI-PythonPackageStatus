# PackageUpdateSearch Documentation

## Overview

PackageUpdateSearch is an installable Python package (Hatchling / PEP 621) that:

- Fetches Reddit posts via the ReleaseTrain HTTP API (`Update.package_update`).
- Exposes an **interactive CLI** (`PackageUpdateSearch.app`) built on `argparse` subcommands.
- Adds an optional **agentic flow** powered by **Ollama**, using **`llama3.2:3b`** as the chat model with native **`tools`** so the runtime executes only functions listed in **`TOOL_REGISTRY`**.

The repo layout is **`src/PackageUpdateSearch/`** (`RT.py`, `app.py`, `agenticRT.py`). There is no top-level **`cli.py`**; the CLI is the `app` module.

---

## Installation and dependencies

Runtime dependencies are declared in **`pyproject.toml`** under **`[project.dependencies]`**:

- `requests` — HTTP requests to ReleaseTrain and the Ollama health check.
- `ollama` — Python client for the local Ollama server.

Optional test dependencies:

```text
pip install ".[test]"
```

(which pulls `pytest` for the `tests/` suite).

Standard editable install:

```text
pip install -e .
```

**Python:** `>=3.9` per `pyproject.toml`.

---

## Running the CLI

After installation, preferred entry:

```bash
python -m PackageUpdateSearch.app
```

From the repository root without installing, ensure `PYTHONPATH` includes `src` or run from layouts your environment supports so `PackageUpdateSearch` resolves as a package (see project `README.md`).

The CLI prints a welcome message and a short help banner, then reads lines like **`> package-update ...`** in a loop until **`exit`** or Ctrl+C.

**Version:** `-v` / `--version` is registered on the root parser—use **`python -m PackageUpdateSearch.app --version`** when invoking argparse directly. Inside the interactive `>` loop, parsing is line-based (e.g. `package-update --limit 5`).

---

## Available commands (`app.py`)

| Command | Purpose |
|---------|---------|
| `package-update` | Call `RT.Update.package_update(...)` with CLI flags |
| `get-request <url>` | Declared as a subparser (`get-request --help` works) — **interactive `handle_command` has no dispatch branch yet**, so parsing succeeds but nothing runs until wired up |
| `capstone` | Declared as a subparser — **same as above**: no **`handle_command`** branch yet |
| `agent-update` | Start **`AgentUpdate.agent_update_conversation(SYSTEM_PROMPT, TOOL_REGISTRY)`** |
| `help` | Show the in-app command list (`print_help`) |
| `exit` | Leave the CLI loop |

The **`print_help()`** banner lists **`package-update`**, **`help`**, **`-v`**, **`agent-update`**, **`exit`**; use e.g. **`get-request --help`** for parsers not listed there.

**Implementation note:** In **`app.py`**, **`args.ascending`** is a boolean from **`store_true`**; **`Update.package_update`** accepts **`ascending`** as `0`/`1` and coerces appropriately.

---

## `package-update`

Calls **`PackageUpdateSearch.RT.Update.package_update`** with parameters from argparse.

**CLI defaults** (`app.py`; may differ from the RT method defaults when omitted in Python-only calls):

| Flag | Meaning | CLI default |
|------|---------|---------------|
| `--q` | Comma-separated subreddit query | `programming,technology` |
| `--min-score` | Minimum post score | `50` |
| `--min-comments` | Minimum comment count | `10` |
| `--limit` | Max posts | `25` |
| `--page` | Page index | `2` |
| `--fields` | Comma-separated API fields | `url,score,tag,title,subreddit,author_description` |
| `--ascending` | If present, sort scores ascending (`store_true`); otherwise descending | omitted (descending) |

**Example** (interactive prompt):

```text
> package-update --q programming,technology --limit 10
```

**Python:**

```python
from PackageUpdateSearch.RT import Update

text = Update.package_update(
    q="programming,technology",
    minScore=50,
    minComments=10,
    limit=10,
    page=2,
    fields="url,score,tag,title,subreddit,author_description",
    ascending=1,
)
```

`Update.package_update` validates **`ascending`** as `0` or `1` (then uses a boolean internally). On non-200 responses it returns an error string including the HTTP status.

---

## `Update.help()`

Static helper that **`print`**s a prose description of `package_update` (parameters and example usage).

```python
from PackageUpdateSearch.RT import Update
Update.help()
```

---

## API layer — ReleaseTrain

- **Endpoint:** `https://releasetrain.io/api/reddit/by-subreddit`
- **Behavior:** Parses JSON **`data`** list; sorts locally by **`score`** per **`ascending`**; formats plain-text blocks.

**Typical fields in output:**

- `[URL:]`, `[SCORE:]`, `[TAG(s):]`, `[TITLE:]`, `[SUBREEDDIT:]` *(label spelling matches current formatter)*  
- `[AUTHOR_DESCRIPTION:]` when present  

---

## AI agent (`agenticRT.py`)

### Role

Runs a multi-turn CLI conversation backed by **`ollama.Client().chat`** with **`tools=[Update.package_update]`**. When the assistant returns **`tool_calls`**, Python invokes **`TOOL_REGISTRY[function_name](**arguments)`**. Only **`package_update`** is registered; unknown tools get an error string appended as a **`tool`** message.

### Prerequisites

1. **Ollama** running locally (default **`http://localhost:11434`** — used by **`is_ollama_running()`**, which probes **`GET /api/tags`**).
2. **`ollama pull`** the model referenced in code: **`llama3.2:3b`**.

*(If startup messages mention a different pull target, align them with the model string in `AgentUpdate.agent_update_conversation`; the codebase uses **`model='llama3.2:3b'`**.)*

### Entry points

Interactive agent from CLI:

```text
> agent-update
```

Programmatic:

```python
from PackageUpdateSearch.agenticRT import SYSTEM_PROMPT, TOOL_REGISTRY, AgentUpdate

AgentUpdate.agent_update_conversation(SYSTEM_PROMPT, TOOL_REGISTRY)
```

**`agent_update_conversation`** accepts **`reset_each_query`** (`True` by default): when `True`, after each assistant turn the message list resets to **`[system, user]`** with only the latest user prompt, so older tool/results do not bleed into the next query.

Helpers:

```python
from PackageUpdateSearch.agenticRT import is_ollama_running
```

```python
from PackageUpdateSearch.agenticRT import AgentUpdate  # AgentUpdate.show_reddit_fetch_tool(messages)
```

### **`SYSTEM_PROMPT`** and modes

The long **`SYSTEM_PROMPT`** constrains behavior (tool-first workflow, strict summarization schema after **`role: tool`**, anti-hallucination and Reddit-only URL rules, cycle-reset narrative). Implementation-wise, **mode selection** is enforced by **`ollama`** tool calling + your loop: assistant → optional **`tool`** messages → next assistant **`content`**.

---

## Tool registry

```python
TOOL_REGISTRY = {
    "package_update": Update.package_update,
}
```

This is the authorization layer: executable tools are only those keyed here.

---

## Agent conversation loop (simplified)

1. Check **`is_ollama_running()`**; if False, print guidance and return.
2. Read user message ( **`exit`** to quit ).
3. **`client.chat`** with **`model='llama3.2:3b'`**, **`messages`**, **`tools=[Update.package_update]`**.
4. Append assistant message.
5. If **`tool_calls`**: run **`TOOL_REGISTRY`**, append **`role: tool`** content, **`continue`** (same turn can process multiple calls).
6. Else print **`response.message.content`** (summary / reply).
7. Prompt again; optionally reset **`messages`** if **`reset_each_query`**.

---

## Design philosophy

- The LLM does not execute arbitrary Python; only **`TOOL_REGISTRY`** entries run.
- Reddit access is mediated by **`Update.package_update`** and the ReleaseTrain endpoint.
- The agent relies on **Ollama** as a separate service; **`ollama`** on PyPI is only the HTTP client library.

---

## Summary

PackageUpdateSearch combines declarative **`pyproject.toml`** dependencies**, a ReleaseTrain-backed **`RT.Update`** helper, an **`argparse`** REPL **`app`**, and an **Ollama**-driven **`AgentUpdate`** path with **`llama3.2:3b`** and a minimal **tool registry** for bounded agent behavior.
