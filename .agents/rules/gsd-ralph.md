# GSD (Get Stuff Done) & Ralph Loop Protocol

## 1. GSD (Get Stuff Done) Workflow

Whenever executing tasks or building features, adhere to the strict 3-phase execution model:

### Phase 1: Spec & Plan (Before writing code)
- **Identify exact goals & scope**: Determine what needs to be changed and what must remain untouched.
- **Enumerate touched files**: List specific files to inspect and edit before modifying them.
- **Define acceptance criteria**: State the exact conditions required for the task to be considered complete (e.g. passing test suite, valid API response, clean build).
- Avoid fluff, speculative changes, or unnecessary refactoring.

### Phase 2: Atomic Execution
- Keep edits focused, minimal, and surgical.
- Maintain existing architecture, style conventions, and docstrings.
- Ensure all imports, types, and dependencies are properly resolved.
- Don't leave placeholder comments (e.g., `# TODO: implement this`).

### Phase 3: Verification & Closure
- Run tests and linters using available execution tools.
- Verify that changes satisfy every acceptance criterion defined in Phase 1.
- Ensure no unintended side-effects or regressions in neighboring modules.

---

## 2. Ralph Loop (Autonomous Feedback & Self-Correction)

When working towards a goal or debugging issues, operate in an autonomous Ralph Loop:

1. **Implement**: Apply targeted modifications.
2. **Execute / Test**: Run the relevant command or test immediately.
3. **Inspect Output**: Read error traces, exit codes, and output logs directly.
4. **Self-Correct**: If an error occurs, do not halt and ask for obvious fixes—analyze root cause and patch immediately.
5. **Iterate**: Repeat steps 1–4 until the feature works and all tests pass cleanly.
6. **Clean State**: Never leave the repository in a broken intermediate state.
