# AGENTS.md

A personal, progressive study of Python's `asyncio`: numbered lesson
scripts under `src/`, each a self-contained, doctested demonstration of
one concept, from a first coroutine to event-loop internals.

Follow the conventions already in the tree, and keep a change scoped to
what was asked for.

## What is here

| Path | What it is |
| ---- | ---------- |
| `src/NNN_topic.py` | One numbered, self-contained lesson; its docstring doctests are the tests. |
| `notes/lesson_template.py` | Template a new lesson starts from. |
| `notes/progression.md` | The curriculum plan the lessons were built against. |
| `notes/recommendations.md` | Content-balance review notes. |
| `notes/libs/cpython-asyncio-doctest.md` | Doctest patterns from CPython; run by hand via `gp-libs`, not by pytest. |
| `notes/cpython-asyncio-internals.md` | CPython source files and concepts backing lessons 15-20. |
| `.github/workflows/tests.yml` | CI: ruff, mypy, pytest. |
| `README.md` | Lesson map and quick start. |

## Which policy applies

- Documentation, user-facing text, commit messages, docstrings, and source
  comments: [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, and pull requests:
  [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a
  single-use helper or a one-line re-export.
- Add a test for every user-visible behaviour change.
- A passing gate is evidence only once it has been shown capable of
  failing. Pair a new test with a deliberate break that proves it bites.

There is no `conftest.py` and no `doctest_namespace` fixture: every
doctest imports what it uses, typically `import asyncio`. A lesson never
imports another lesson — each file is self-contained. Keep
`asyncio.sleep()` calls in doctests at 0.001 seconds; slower sleeps slow
the whole suite for no realism gained.

## References

- [Python `asyncio` docs](https://docs.python.org/3/library/asyncio.html)
- [What's New in Python 3.14 — asyncio introspection](https://docs.python.org/3/whatsnew/3.14.html#asyncio-introspection-capabilities),
  used by lessons 24-26
- `notes/libs/cpython-asyncio-doctest.md` — doctest pattern reference
