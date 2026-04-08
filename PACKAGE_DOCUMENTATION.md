# PackageUpdateSearch Python Package Documentation

## Package Overview

`PackageUpdateSearch` is a small Python package that provides utilities for fetching Reddit posts from the ReleaseTrain API, making generic HTTP GET requests, and printing a capstone greeting.

## Package Metadata

- Name: `PackageUpdateSearch`
- Version: `0.0.4`
- Python requirement: `>=3.9`
- License: `MIT`
- Build backend: `hatchling.build`
- Readme: `README.md`

## Installation

Install the package locally from the project root:

```bash
pip install -e .
```

## Package Structure

```
packaging_tutorial/
├── LICENSE
├── PACKAGE_DOCUMENTATION.md
├── README.md
├── pyproject.toml
├── src/
│   └── PackageUpdateSearch/
│       ├── __init__.py
│       ├── APP_DOCUMENTATION.md
│       ├── app.py
│       ├── example.py
│       └── testing.py
└── tests/
```

## Package Modules

### `PackageUpdateSearch.example`

Contains the main utility class `example` with the following static methods:

- `example.package_update(q, minScore, minComments, limit, page, fields, ascending)`
  - Queries `https://releasetrain.io/api/reddit/by-subreddit`.
  - Accepts filter parameters for subreddit search, score, comments, pagination, and fields.
  - Returns a formatted string of Reddit posts when the request succeeds.
  - Returns an error message when the response status is not 200.

- `example.get_request(URL)`
  - Sends a generic HTTP GET request using `requests.get`.
  - Prints the returned `requests.Response` object.

- `example.capstone()`
  - Prints a capstone greeting message.

- `example.help()`
  - Prints usage information for the `package_update` method.

### `PackageUpdateSearch.app`

Implements an interactive CLI wrapper around `PackageUpdateSearch.example`.

- Creates an `argparse` parser for subcommands.
- Supports interactive commands such as `package-update`, `get-request`, `capstone`, `help`, and `exit`.
- Handles invalid input and keeps the CLI running until the user exits.

## Usage Example

### Importing the package

```python
from PackageUpdateSearch.example import example

result = example.package_update(
    q='programming,technology',
    minScore=50,
    minComments=10,
    limit=10,
    page=1,
    fields='url,score,tag,title,subreddit,author_description',
    ascending=False,
)
print(result)

example.capstone()
```

### Running as a module

From the `src` directory:

```bash
python -m PackageUpdateSearch.app
```

## Notes

- This package relies on the external `requests` library.
- The package is currently published as a local editable installable project.
- The CLI implementation is separate from the core `example` utilities, so the package can be imported and used directly in Python code.
