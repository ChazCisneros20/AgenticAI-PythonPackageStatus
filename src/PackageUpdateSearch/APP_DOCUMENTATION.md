# PackageUpdateSearch CLI Documentation

## Overview

`app.py` is an interactive command-line interface (CLI) wrapper around the `example.py` module. It provides a user-friendly way to interact with the package update searching functionality without needing to write Python code directly. The CLI operates in an **interactive loop**, allowing multiple commands in a single session.

## Architecture

The CLI uses Python's `argparse` library to parse commands and arguments. It creates a parser for each user input to avoid state pollution between commands.

### Key Components

#### 1. **`create_parser()`**
- Creates and returns an `ArgumentParser` instance with `add_help=False` to prevent conflicts with the interactive help command
- Sets up all available subcommands and their arguments using `add_subparsers(dest='command', required=False)`
- Defines command groups:
  - `package-update` - Main command to fetch Reddit posts
  - `get-request` - Generic HTTP GET utility
  - `capstone` - Greeting message
  - `help` - Display help text
  - `exit` - Quit the CLI

**Why separated into a function:** Allows the parser to be recreated for each user input in the interactive loop, preventing state pollution between commands.

#### 2. **`handle_command(parser, command_line)`**
- Accepts a string of user input (e.g., `"package-update --q Python"`)
- Splits the string into arguments and parses them using the provided parser
- Executes the corresponding command from `example.py`
- Catches `SystemExit` exceptions (raised by argparse on errors) to prevent program termination
- Returns `True` to continue the loop, `False` to exit

**Error Handling:** Generic exceptions are caught and printed, allowing the user to correct their input and try again.

#### 3. **`print_help()`**
- Displays all available commands and their descriptions
- Called on startup and when user types `help`
- Provides a user-friendly alternative to argparse's auto-generated help

#### 4. **`main()`**
- Entry point for the CLI
- Initializes the parser once
- Enters an infinite loop that:
  1. Displays `> ` prompt
  2. Reads user input with `input("> ").strip()`
  3. Ignores empty input
  4. Passes input to `handle_command()`
  5. Continues until user types `exit` or presses Ctrl+C
- Gracefully handles `KeyboardInterrupt` (Ctrl+C) with a "Goodbye!" message

## Code Flow

```
main()
├── Create parser with create_parser()
├── Print welcome message and help
└── Loop until exit:
    ├── Display prompt ">"
    ├── Read and strip user input
    ├── If input empty: continue
    ├── Call handle_command(parser, input)
    │   ├── Split input into command_parts
    │   ├── Parse with parser.parse_args(command_parts)
    │   ├── Execute corresponding function from example.py
    │   └── Return True (continue) or False (exit)
    └── Return to prompt
```

## Command Reference

### `package-update`
Fetches Reddit posts from the ReleaseTrain API filtered by subreddit, score, and comment count.

**Arguments:**
- `--q` (default: `'programming,technology'`) - Comma-separated subreddit names to query
- `--min-score` (default: `50`) - Minimum post score
- `--min-comments` (default: `10`) - Minimum comment count
- `--limit` (default: `25`) - Maximum posts to return
- `--page` (default: `2`) - Page number for pagination
- `--fields` (default: `'url,score,tag,title,subreddit,author_description'`) - Requested fields
- `--ascending` (flag) - Sort score ascending (default is descending)

**Example:**
```
> package-update --q Python --min-score 30 --limit 10
```

### `get-request`
Sends a generic HTTP GET request to any URL.

**Arguments:**
- `url` (required) - The full URL to request

**Example:**
```
> get-request https://api.example.com/data
```

### `capstone`
Prints the capstone project greeting message.

**Example:**
```
> capstone
Hello World
This is the start of my Senior Capstone project !
```

### `help`
Displays all available commands.

**Example:**
```
> help
```

### `exit`
Gracefully exits the CLI.

**Example:**
```
> exit
Goodbye!
```

## How It Differs from Traditional CLI

**Traditional CLI (command-line arguments):**
```bash
python app.py package-update --q Python --min-score 50
```
- Command and arguments must be on the same line
- Program exits after one command executes

**Interactive CLI (this implementation):**
```bash
python app.py
> package-update --q Python --min-score 50
> package-update --q technology
> exit
```
- Run once, then enter interactive session
- Multiple commands in one session
- More user-friendly for repeated operations

## Error Handling

1. **Empty Input** - Silently ignored; prompt redisplays
2. **Invalid Arguments** - argparse prints error; user gets another chance
3. **API Errors** - Caught and printed; prompt redisplays
4. **Ctrl+C** - Catches `KeyboardInterrupt`, displays "Goodbye!", exits gracefully

## Integration with `example.py`

The CLI is a thin wrapper around the `example` class methods:

| CLI Command | Corresponding Function | Module |
|---|---|---|
| `package-update` | `example.package_update(...)` | `example.py` |
| `get-request` | `example.get_request(...)` | `example.py` |
| `capstone` | `example.capstone()` | `example.py` |

All business logic remains in `example.py`; `app.py` only handles user interaction and argument parsing.

## Usage Example

```
$ python -m PackageUpdateSearch.app
Welcome to the PackageUpdateSearch CLI!

Available commands:
  package-update  - Fetch and format ReleaseTrain Reddit posts
  get-request     - Send a GET request to a URL
  capstone        - Print the capstone greeting
  help            - Show this help message
  exit            - Exit the CLI

> package-update --q Python
[API response with formatted posts]
> capstone
Hello World
This is the start of my Senior Capstone project !
> exit
Goodbye!
```

## Running the App

From the project root:
```bash
cd src
python -m PackageUpdateSearch.app
```

Or:
```bash
python src/PackageUpdateSearch/app.py
```