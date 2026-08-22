# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, commit messages, docstrings, and source comments — every
reader-facing surface this repository has.

For environment setup, the gates, and how to run the suite, see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Voice

A docstring says what a caller may rely on; prose says what happens. Both
are present tense, lead with the thing being described, and stop. Why it
was built that way belongs in the commit message, which is timestamped and
attached to the diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks.
Prefer short declarative sentences, one operational fact each. Do not
explain Python to Python developers; do explain what asyncio does here.

Type annotations describe shape. Documentation describes meaning. A
sentence that restates a signature has said nothing.

| Instead of                       | Prefer                            |
| --------------------------------- | ---------------------------------- |
| "powerful", "seamless"           | state the capability              |
| "easily", "simply", "just"       | omit                              |
| "simple", "obvious", "intuitive" | omit                              |
| "robust"                         | name the failure that is handled  |
| "under the hood"                 | omit unless observable            |
| "please note that", "note that"  | state the fact                    |
| "leverage", "utilize"            | "use"                             |
| "delve into"                     | "read", or omit                   |
| "in order to"                    | "to"                              |

## Documented examples that run

Examples in this repository are tests. This section is the contract for
writing one the suite can actually see.

**Only a `>>> ` prompt executes.** A docstring `Examples` section without
prompts is prose that looks like a test — nothing collects it, and it can
be wrong for years. When editing a lesson, count the prompts before and
after.

**Where examples run.** `pytest` is configured with `--doctest-modules` and
`testpaths = ["src"]`. That collects every docstring example under `src/`;
`README.md` is not in `testpaths` and is never executed by `pytest`. There
is no `conftest.py` and no `doctest_namespace` fixture — nothing is
pre-imported. Every example imports what it uses, typically `import
asyncio`.

`notes/libs/cpython-asyncio-doctest.md` is a separate reference: its
examples use `pycon` fences and are run by hand through `gp-libs` (see the
README's Notes section for the command). `pytest` never collects it — it is
not under `testpaths`, and this repository has no plugin that reads
doctests out of Markdown.

**`# doctest: +SKIP` is not permitted.** It is a workaround that tests
nothing. If an example cannot pass, fix the example or fix the code.

**Do not downgrade a doctest to a non-executed block to make it pass.** A
`.. code-block::` or an unprompted fence does not run.

**Option flags.** `ELLIPSIS` and `NORMALIZE_WHITESPACE` are enabled
globally (`doctest_optionflags` in `pyproject.toml`), so `...` elides
variable output and whitespace differences do not fail a comparison.

**Docstring examples** use the NumPy `Examples` section:

    Examples
    --------
    >>> asyncio.run(demonstrate_concept())
    'Expected Result'

### Async examples

A doctest cannot use a bare top-level `await`, so every example drives the
coroutine through `asyncio.run()` instead. Keep `asyncio.sleep()` calls at
0.001 seconds — long enough to demonstrate suspension, short enough that
the full suite still runs in under a couple of seconds. Mark output whose
ordering varies between runs — concurrent tasks racing to print — with an
inline `# doctest: +ELLIPSIS`, even though the flag is already enabled
globally; it tells the reader the order is not guaranteed.

## Docstrings

The prime directive: never restate the type. The annotation is the source
of truth; the docstring carries what the annotation cannot.

Document the dimensions the type system cannot encode:

- **Mutation.** What it changes in place.
- **Ordering.** Whether results come back in a guaranteed order.
- **Timing.** What has finished by the time the awaitable resolves.
- **Failure.** Which exceptions are raised and what triggers each.
- **Concurrency.** Whether calls are coalesced, queued, or independent.
- **Boundary behaviour.** What zero, empty, and the maximum do.

**Classes with fields** — `NamedTuple`, dataclasses — document every field
in an `Attributes` section:

```python
class TaskRow(NamedTuple):
    """One row of the task introspection table.

    Attributes
    ----------
    task_name : str
        Name the task was created with.
    coroutine_stack : str
        Frames the task is currently suspended in.
    """
```

A type says how a field is shaped, not what it holds. Describing each one
keeps that meaning next to the code, and anything that renders the class —
autodoc, a REPL, an editor tooltip — has a description to show instead of a
bare name.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. One docstring dialect (NumPy,
via `ruff`'s `pydocstyle` convention) applies across the repository,
enforced by the linter rather than relitigated in review.

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real
time rediscovering intent, an invariant, a constraint, or a failure mode
the code and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write
this comment, at this length? Those projects state the constraint and
stop. They do not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that
hand-syncs a value the code owns — a count, an offset, a duplicated
constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several
facts, in which case split it, or arguing, in which case cut it to the
fact.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, and concurrency requirements that
  types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not
  reintroduce the bug.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- History version control already holds, including commented-out code.
- Ticket and issue numbers. They say nothing to a reader without tracker
  access, and they rot when the tracker moves. Unfinished work goes in the
  tracker, not the source.
- Transient observations — "currently", "for now" — that go stale with no
  nearby edit.

Bad (Delete):

```python
# There are 321 tests to complete for servers.
```

Good (Keep):

```python
# CPython < 3.11 has no ExceptionGroup, so this branch stays.
```

### Documentation exception

Doctests, minimal usage examples, and param, return, and raises lines on
public API are exempt from the loss gate — they serve the caller, not the
maintainer. They are exempt from nothing else. Ceiling: a good man page
entry.

NumPy-style `Parameters`, `Returns`, and `Attributes` sections and
executable doctests fall under this exception — autodoc ships every field
whether or not you describe it, and a doctest that runs is also a test.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action. Doctests and other executed examples are exempt — the
test suite runs them, nobody pastes them.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is
  then one logical command.
- **Explanations go in prose above the block**, never as `#` comments
  inside it.
- **Shell commands use the `console` tag with a `$ ` prefix.** This
  separates interactive commands from scripts and enables prompt-aware
  copy.
- **Split long commands with `\`** — one flag or flag+value pair per
  indented continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing `(#NN)`
pull request reference, and wrap body lines at 72. The blank line between
the `why:` and `what:` blocks is optional — useful when `why:` runs to
multiple lines.

Subjects are plain English. Never put a lesson number or other
repo-internal shorthand in the subject line — a reader of `git log
--oneline` should understand every title cold.

Common types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (`CLAUDE.md`)

Mark a breaking change with `BREAKING:` in the body.

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```
