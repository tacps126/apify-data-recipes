# Contributing

Each recipe is one short, runnable script that calls one Actor through `recipes/_apify.py` and turns
its results into something useful (a CSV, an alert, a ranked list).

## Rules for a recipe

- One file, standard library plus `requests`. Python 3.10+.
- The docstring says what it does, what it costs, and how to run it (`Usage:`).
- Read the Apify token from `APIFY_TOKEN` only; never hard-code keys or print them.
- Keep runs small by default (`maxItems`, a few companies or queries), so trying a recipe costs cents.
- Add a row for it in `README.md`.

## Checks (CI runs the same; no token needed)

```bash
uvx ruff check .
uvx ruff format --check .
python3 -m py_compile recipes/*.py
```
