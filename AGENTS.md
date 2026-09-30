# Project Development Standards: GSD, Ralph Loop & CodeRabbit Protocol

This repository adheres to high-velocity, autonomous, spec-driven development standards.

## 1. GSD (Get Stuff Done) Execution
- **Spec First**: Always clarify scope and touch-points before modifying files.
- **Minimal Diffs**: Keep changes focused and atomic; avoid rewriting functional code.
- **Verification**: Verify implementation against concrete criteria (tests, runs, builds) before closing tasks.

## 2. Ralph Loop (Autonomous Persistence)
- Follow an iterative loop: **Code $\to$ Test $\to$ Inspect Error $\to$ Self-Correct $\to$ Re-test**.
- Do not stop upon encountering a test failure or syntax error; autonomously resolve the root cause until the entire suite passes.

## 3. CodeRabbit Quality Gate
- Before committing or submitting code, ensure it meets CodeRabbit review standards:
  - Robust handling of edge cases, empty values, and exceptions.
  - No exposed secrets or hardcoded credentials.
  - Clean separation of concerns matching the project's layered architecture.
