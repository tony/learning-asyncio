# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a structured learning repository for Python's asyncio module, consisting of 20 progressive lessons covering everything from basic async/await concepts to advanced event loop internals.

## Essential Commands

### Running Tests
```bash
uv run pytest                # Run all tests including doctests
uv run pytest-watcher        # Run tests in watch mode for continuous development
```

### Code Quality
```bash
uv run ruff check           # Run linter
uv run ruff format          # Format code
uv run mypy src/            # Type check source files
```

### Running Individual Lessons
```bash
python src/001_intro.py     # Run any lesson directly
```

## Architecture and Structure

### Lesson Organization
The codebase follows a strict lesson-based structure:
- **Part I (Lessons 1-5)**: Foundational async concepts
- **Part II (Lessons 6-11)**: Synchronization primitives (Lock, Semaphore, Queue, Event, Condition, Barrier)
- **Part III (Lessons 12-14)**: External integrations (Streams, Subprocess, Timeout)
- **Part IV (Lessons 15-20)**: Event loop internals and advanced techniques

### Lesson Template Structure
Each lesson strictly follows the template in `notes/lesson_template.py` with these sections:

1. **Module Docstring** with:
   - Clear title
   - Context section (concept, prerequisites, references)
   - Summary section (learning outcomes)
   - Doctest notes

2. **Standard imports** (only stdlib, primarily asyncio)

3. **`demonstrate_concept()` function**:
   - Core demonstration of the lesson's concept
   - Comprehensive docstring with Examples section
   - Minimal async sleep (0.001s) for testing speed
   - Returns demonstrable results

4. **`main()` function**:
   - Orchestrates the demonstration
   - Handles multiple tasks for concurrency lessons
   - Prints results for direct execution

5. **Executable entry point**: `if __name__ == "__main__"`

### Key Development Patterns
- **Doctests**: All functionality is verified through doctests which pytest runs automatically
- **Minimal delays**: Use 0.001s delays to keep tests fast
- **Deterministic output**: Ensure consistent output for reliable doctests
- **Type hints**: Strict mypy configuration requires comprehensive type annotations
- **Self-contained**: Each lesson is independent and demonstrates a single concept
- **Educational focus**: Comments explain tricky parts, no external dependencies

### Testing Strategy
- pytest is configured with `--doctest-modules` to run all doctests
- Tests are located within the lesson files themselves
- No separate test directory - lessons are both educational content and tests
- Use `# doctest: +ELLIPSIS` for non-deterministic output (concurrency)

### Doctests

**All functions and methods MUST have working doctests.** Doctests serve as both documentation and tests.

**CRITICAL RULES:**
- Doctests MUST actually execute - never comment out `asyncio.run()` or similar calls
- Doctests MUST NOT be converted to `.. code-block::` as a workaround (code-blocks don't run)
- If you cannot create a working doctest, **STOP and ask for help**

**Available tools for doctests:**
- Ellipsis for variable output: `# doctest: +ELLIPSIS`
- Minimal delays (0.001s) for async timing

**`# doctest: +SKIP` is NOT permitted** - it's just another workaround that doesn't test anything.

**Async doctest pattern:**
```python
>>> import asyncio
>>> async def example():
...     await asyncio.sleep(0.001)
...     return "result"
>>> asyncio.run(example())
'result'
```

**When concurrency order varies, use ellipsis:**
```python
>>> asyncio.run(concurrent_demo())  # doctest: +ELLIPSIS
'Task ... completed'
```

## Known Issues (from recommendations.md)

### File Naming
- Lesson 20 is `020_profiling_and_optimizing.py` (should be `020_performance_tuning.py`)

### Content Balance
- Over-emphasis on synchronization primitives (30% of content)
- Under-representation of practical I/O examples beyond basic streams
- Missing topics: file I/O, HTTP clients, testing async code, async context managers

## CPython Asyncio Internals Reference

For advanced lessons (15-20), key CPython internals to reference:

### Core Files in CPython
- `Lib/asyncio/base_events.py` - BaseEventLoop implementation
- `Lib/asyncio/events.py` - Abstract interfaces
- `Lib/asyncio/tasks.py` - Task implementation
- `Lib/asyncio/futures.py` - Future implementation
- `Modules/_asynciomodule.c` - C acceleration

### Key Concepts to Cover
- Event loop's `_run_once()` method and execution model
- Task state machine and `__step` mechanism
- Handle/TimerHandle callback system
- Selector-based I/O and platform differences
- Future/Task relationship and C optimization

## Important Notes
- This is a pure Python stdlib project - no external dependencies beyond asyncio
- Code style is enforced through extensive ruff rules including pydocstyle
- When modifying lessons, ensure doctests still pass and output remains deterministic
- Maintain educational value - each lesson should teach one concept clearly

## Git Commit Standards

Format commit messages as:

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

The blank line between the `why:` block and the `what:` block is
optional — useful when the `why:` body runs to multiple lines and the
two sections benefit from visual separation.

Common commit types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev Dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (CLAUDE.md)

Subjects are plain English. Never put curriculum codes or other
repo-internal shorthand in the subject line — a reader of
`git log --oneline` should understand every title cold.

Example:

```
src/022_file_io(feat[read_file_in_chunks]): Use thread pool for async file reading

why: Current implementation blocks event loop on large files.

what:
- Replace synchronous iteration with asyncio.to_thread()
- Update docstring to match actual behavior
- Add tests for concurrent file operations
```

For multi-line commits, use heredoc to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
Scope(type[detail]): concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

Guidelines:

- Subject line at most 50 characters; body lines at most 72
- Imperative mood ("Add", "Fix" — not "Added", "Fixed")
- One topic per commit; blank line between subject and body
- Mark breaking changes with `BREAKING:`

## Documentation Standards

### Code blocks are paste-and-run units

One command per triple-backtick block, so pasting a block runs exactly
one intended action. Don't blur multiple commands annotated by comments
into the same block — explanations belong in prose above the block. A
multi-step sequence may share a block only when explicitly chained with
`;` / `; \` (the chain *is* the single action). Command menus are
per-command blocks with prose lead-ins, not tables.

## AI Slop Prevention

Treat AI slop as **review-hostile noise**, not as proof that text or
code is wrong. The goal is to maximize information density by removing
artifacts that make the repository harder to trust or navigate.

### The Anti-Slop Rubric

Before committing, audit all AI-assisted changes for these noise
patterns:

- **AI Signatures:** Remove "Generated by", footers, conversational
  filler ("Certainly!", "Here is..."), unexplained emojis (🤖, ✨), and
  AI-tool metadata.
- **Brittle References:** Avoid hard-coded line numbers, fragile
  file/test counts, dated "as of" claims, bare SHAs, and local
  absolute paths unless they are strict evidentiary artifacts (e.g.,
  benchmark logs).
- **Diff Narration:** Do not restate what moved, was renamed, or was
  removed in artifacts the downstream reader holds: code, docstrings,
  README, CHANGES, PR descriptions, or release notes. The diff and
  commit message already carry this history.
- **Branch-Internal Narrative:** Do not mention intermediate branch
  states, abandoned approaches, or "no longer" behavior unless users
  of a published release actually experienced the old state (**The
  Published-Release Test**).
- **Low-Value Scaffolding:** Remove ownerless TODOs (`TODO: revisit`),
  unused future-proofing, debug artifacts, and defensive wrappers that
  do not protect a currently reachable failure mode.
- **Prose Inflation:** Replace generic AI "tells" like *comprehensive,
  robust, seamless, production-ready, leverage, delve, tapestry,* and
  *best practices* with concrete descriptions of behavior,
  constraints, or trade-offs.
- **Coded Labels:** Write rules, options, and findings as plain
  imperatives. Don't tag them with codes like `[R1]`, `A1`, or
  `Option B` in artifacts a human reads — the reader shouldn't have to
  decode an index. Internal agent bookkeeping may use ids; shipped text
  may not.

### Preservation & Context

**When unsure, leave the text in place and ask.** Subjective cleanup
must never be a reason to remove load-bearing rationale.

- **Preserve the "Why":** You MUST NOT delete comments that document
  invariants, protocol constraints, platform quirks, security
  boundaries, and upstream workarounds.
- **Evidence is Immune:** Preserve exact counts, dates, and SHAs when
  they serve as evidence in benchmark results, release notes, stack
  traces, or lockfiles.
- **Behavior Over Inventory:** A useful description explains what
  changed for the *system or user*; it does not provide an inventory
  of files or functions the diff already shows.

### The Published-Release Test

Long-running branches accumulate tactical decisions — renames,
refactors, attempts-then-reverts. When deciding what counts as
branch-internal, use trunk or the parent branch as the baseline — not
intermediate states inside the current branch. Ask:

> Did users of the most recently published release ever experience
> this old name, old behavior, or bug?

If the answer is **no**, it is branch-internal narrative. Move it to
the commit message and describe only the final state in the artifact.

**Keep in shipped artifacts:**

- Deprecations and migration guides for symbols that actually shipped.
- `### Fixes` entries for bugs that affected users of a published
  release.
- Comments explaining *why the current code looks this way*
  (invariants, platform quirks) that make sense to a reader who never
  saw the previous version.

### Cleanup in Hindsight

When applying these rules retroactively from inside a feature branch,
first establish scope by diffing against the parent branch (or trunk)
to identify which commits this branch actually introduced. Then:

- **In-branch commits:** Prompt the user with two options: `fixup!`
  commits with `git rebase --autosquash` to address each causal commit
  at its source, or a single cleanup commit at branch tip.
- **Trunk/Parent commits:** Default to leaving them alone. Act only on
  explicit user instruction. If the user opts in, fold the cleanup
  into a single commit at branch tip; do not rewrite shared history.
- **Scope guard:** If cleaning prior slop would touch a colleague's
  work or expand the branch beyond its stated goal, stay in lane:
  protect the current goal and leave prior slop alone.

### Change Discipline

- Make the smallest coherent change that solves the verified problem;
  keep unrelated cleanup out of it.
- Reuse an existing file, component, helper, API, or test before adding
  a new one. Modify in place when the change fits the file's
  responsibility.
- Keep new APIs private until a caller outside the module needs them.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized high-touch module — not
  for a single-use helper or a one-line re-export.

### Keep Instructions Lean

Treat this file like code and prune it.

- Delete a line whose removal would not cause a mistake.
- Move multi-step procedures into skills, path-specific rules into
  nested AGENTS.md files, and hard limits into hooks or CI.
- Keep only non-obvious, broadly applicable defaults here. Anything a
  reader can infer from the code, a manifest, or a linter does not
  belong.
