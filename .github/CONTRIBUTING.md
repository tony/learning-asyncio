# Contributing

Thanks for looking. Bug reports with a reproduction, and notes on where a
lesson's explanation or doctest misled you, are the most useful
contribution right now.

How this project writes prose — README, commit messages, docstrings, and
source comments — is set out separately in [WRITING.md](WRITING.md). Read
that before changing any of it. The constraints every change is held to,
and the map of what is where, are in [AGENTS.md](../AGENTS.md).

## Getting set up

```console
$ uv sync --all-extras --dev
```

## The gates

CI is the order of record; every gate it runs has to pass before a change
is done (`.github/workflows/tests.yml`).

Lint:

```console
$ uv run ruff check .
```

Format:

```console
$ uv run ruff format . --check
```

Type-check:

```console
$ uv run mypy .
```

Test:

```console
$ uv run pytest
```

Documentation is a gate, not a courtesy. Every lesson's doctests run as
part of `pytest` via `--doctest-modules`; there is no separate doctest
step, and a green `pytest` is the proof. Which blocks qualify, and the one
mistake that silently removes a test, are in
[WRITING.md](WRITING.md#documented-examples-that-run).

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption.

## Tests

There is no separate test directory: each file under `src/` is both the
lesson and its test, collected from its docstrings.

Run one lesson's doctests:

```console
$ uv run pytest src/007_task_groups.py
```

Re-run affected tests on save:

```console
$ uv run pytest-watcher
```

Run a lesson as a script, outside pytest:

```console
$ python src/001_intro.py
```

## Pull requests

One subject per pull request. Unrelated cleanup found along the way
belongs in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

Commit format is in [WRITING.md](WRITING.md#commits).

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of
  personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should
  always assume good intentions.
- Behaviour which can be reasonably considered harassment will not be
  tolerated.

Based on [Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).
