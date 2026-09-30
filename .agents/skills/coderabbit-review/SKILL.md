---
name: coderabbit-review
description: >-
  Perform in-depth, automated code quality and security reviews simulating CodeRabbit standards. Use whenever the user asks to review changes, audit code, inspect PR diffs, or verify code quality before commits.
---

# CodeRabbit-Style Automated Code Review

Provide a structured, rigorous code review covering correctness, security, performance, and best practices.

## Review Dimensions

When reviewing changes or files, evaluate the following criteria:

### 1. Correctness & Edge Cases
- Logical correctness and potential off-by-one errors.
- Unhandled `None`, `null`, empty collections, or boundary conditions.
- Error handling: ensure exceptions are caught appropriately without swallow/masking.
- Race conditions or state inconsistency in async/concurrent routines.

### 2. Security & Data Protection
- Secrets or credentials hardcoded in files.
- Injection vectors (SQL, command, path traversal).
- Unvalidated user inputs or insecure deserialization.

### 3. Performance & Resource Management
- Inefficient queries or algorithms ($O(N^2)$ loops, N+1 patterns).
- Memory leaks, unclosed file descriptors, sockets, or database connections.
- Unnecessary re-computation or un-cached expensive calls.

### 4. Code Health & Maintainability
- Type safety and clarity of function signatures.
- Adherence to project architecture and existing abstractions.
- Preservation of existing documentation and relevant comments.

## Review Output Format

Structure the review using the following sections:

1. **Executive Summary**: Brief 2–3 sentence overview of changes and overall health score.
2. **Key Findings / Action Items**:
   - `[CRITICAL]` / `[MAJOR]`: Defects that can cause crashes, data corruption, or security risks.
   - `[MINOR]`: Refactorings, performance optimizations, or style deviations.
   - `[NIT]`: Minor polish or docstring improvements.
3. **Suggested Fixes**: Provide concrete replacement code blocks for each finding.
4. **Conclusion / PR Status**: `Approved`, `Approved with minor suggestions`, or `Changes Requested`.
