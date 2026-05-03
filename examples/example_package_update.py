"""
Fetch Reddit-style update text via the installed package (ReleaseTrain API).

Prerequisite:
    pip install PackageUpdateSearch
    (or: pip install -e . from the repo root)

Run:
    python examples/example_package_update.py
"""

from PackageUpdateSearch.RT import Update


def main() -> None:
    text = Update.package_update(
        q="python,programming",
        minScore=50,
        minComments=10,
        limit=5,
        page=1,
        fields="url,score,tag,title,subreddit,author_description",
        ascending=0,
    )
    print(text)


if __name__ == "__main__":
    main()
