# PackageUpdateSearch CLI Documentation

## Overview

`app.py` is an interactive command-line interface (CLI) wrapper around the `example.py` module. It provides a user-friendly way to execute the package update search utility, fetch generic HTTP GET responses, and print a capstone greeting without needing to write Python code directly.

The CLI runs in an interactive loop, accepting commands until the user exits.

## Architecture

The CLI uses Python's `argparse` library to parse commands and arguments. It creates a parser once and reuses it during the interactive session.

### Key Components

#### 1. `create_parser()`
- Creates and returns an `ArgumentParser` instance with `add_help=False`.
- Defines subcommands using `add_subparsers(dest='command', required=False)`.
- Registers these commands:
  - `package-update` - Fetch ReleaseTrain Reddit posts.
  - `get-request` - Send a generic HTTP GET request.
  - `capstone` - Print the capstone greeting message.
  - `help` - Display available commands.
  - `exit` - Quit the CLI.

#### 2. `handle_command(parser, command_line)`
- Parses the user's input string.
- Runs the corresponding function from `example.py`.
- Catches `SystemExit` from argparse to keep the CLI running after parse errors.
- Returns `True` to continue or `False` to exit.

#### 3. `print_help()`
- Prints the list of available commands and their descriptions.
- Called at startup and when the user enters `help`.

#### 4. `main()`
- Entry point for the CLI.
- Creates the parser once.
- Prints a welcome message and command list.
- Enters a loop that reads input and dispatches it to `handle_command()`.
- Handles `KeyboardInterrupt` by printing `Goodbye!` and exiting.

## Command Reference

### `package-update`
Fetches Reddit posts from the ReleaseTrain API endpoint `https://releasetrain.io/api/reddit/by-subreddit`.

Arguments:
- `--q` (default: `programming,technology`) - comma-separated subreddit names.
- `--min-score` (default: `50`) - minimum post score.
- `--min-comments` (default: `10`) - minimum number of comments.
- `--limit` (default: `25`) - maximum number of posts to return.
- `--page` (default: `2`) - page number for pagination.
- `--fields` (default: `url,score,tag,title,subreddit,author_description`) - comma-separated requested fields.
- `--ascending` - sort posts by score in ascending order. The default is descending.

Example:
```
> package-update --q Python --min-score 30 --limit 10
```

### `get-request`
Sends a generic HTTP GET request and prints the `requests.Response` object.

Arguments:
- `url` (required) - the full URL to request.

Example:
```
> get-request https://api.example.com/data
```

### `capstone`
Prints the capstone greeting message.

Example:
```
> capstone
```

### `help`
Displays available commands.

Example:
```
> help
```

### `exit`
Exits the CLI session.

Example:
```
> exit
Goodbye!
```

## Error Handling

- Empty input is ignored and the prompt redisplays.
- Invalid arguments trigger argparse errors but keep the CLI open.
- API request failures return a status message instead of crashing.
- `Ctrl+C` is handled gracefully with a `Goodbye!` message.

## Integration with `example.py`

The CLI delegates business logic to `example.py`:

| CLI Command | Function | Module |
|---|---|---|
| `package-update` | `example.package_update(...)` | `example.py` |
| `get-request` | `example.get_request(...)` | `example.py` |
| `capstone` | `example.capstone()` | `example.py` |

The CLI handles input parsing and output display, while `example.py` performs the request handling and formatting.

## Usage Example

```
$ cd src
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

Or directly from the repository root:

```bash
python src/PackageUpdateSearch/app.py
```
