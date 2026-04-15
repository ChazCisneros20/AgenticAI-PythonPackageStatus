# PackageUpdateSearch

A small Python package that provides an interactive CLI wrapper for the `PackageUpdateSearch.example` utilities.

## Overview

`PackageUpdateSearch` includes:

- `app.py`: an interactive CLI loop that accepts commands and arguments.
- `example.py`: business logic for fetching ReleaseTrain Reddit posts, making generic GET requests, and printing a capstone greeting.

## Requirements

- Python 3.9+
- `requests`

## Installation

From the project root, install the package locally:

```bash
pip install -e .
```

## Running the CLI

From the `src` directory:

```bash
cd src
python -m PackageUpdateSearch.app
```

Or from the project root using the file path:

```bash
python src/PackageUpdateSearch/app.py
```

## CLI Commands

The interactive CLI supports the following commands:

- `package-update` - Fetch and format Reddit posts from the ReleaseTrain API.
- `get-request` - Send a generic HTTP GET request to a URL.
- `capstone` - Print the capstone greeting message.
- `help` - Show available commands.
- `exit` - Exit the interactive session.

### `package-update`

Fetches Reddit posts from `https://releasetrain.io/api/reddit/by-subreddit`.

Arguments:

- `--q` (default: `programming,technology`) - comma-separated subreddit names.
- `--min-score` (default: `50`) - minimum post score.
- `--min-comments` (default: `10`) - minimum number of comments.
- `--limit` (default: `25`) - maximum number of posts to return.
- `--page` (default: `2`) - pagination page number.
- `--fields` (default: `url,score,tag,title,subreddit,author_description`) - comma-separated requested fields.
- `--ascending` - sort score ascending (default is descending).

Example:

```text
> package-update --q Python --min-score 30 --limit 10
```

### `get-request`

Sends a simple HTTP GET request and prints the response object.

Example:

```text
> get-request https://api.example.com/data
```

### `capstone`

Prints the capstone greeting message.

Example:

```text
> capstone
```

## Package API

The package also exposes the `example` class in `src/PackageUpdateSearch/example.py`.

Available methods:

- `example.package_update(...)`
- `example.get_request(URL)`
- `example.capstone()`
- `example.help()`

## Notes

- The CLI is a thin wrapper around `example.py`.
- `example.package_update()` returns a formatted string of Reddit posts.
- `example.get_request()` prints the raw `requests.Response` object.

