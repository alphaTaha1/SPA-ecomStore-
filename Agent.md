### Article I — The Three Core Laws

**LAW-TDD-001 — No production code without a failing test.**
You may not write a single line of production code unless it is needed to make a currently failing test pass.

**LAW-TDD-002 — Write only enough test to fail.**
Stop writing the test as soon as it fails. A compile/import error counts as failing.

**LAW-TDD-003 — Write only enough code to pass.**
Write the *minimum* production code that makes the failing test pass. Nothing speculative.
*LAW-TDD-004 — One behavior per cycle.**
Each cycle adds exactly one new test describing exactly one behavior. Two new behaviors = two cycles.
**LAW-TDD-004 — One behavior per cycle.**
Each cycle adds exactly one new test describing exactly one behavior. Two new behaviors = two cycles.
**LAW-TDD-005 — Fail for the right reason.**
A RED test must fail because the *behavior is missing*, not because of a typo, a wrong import path,
or a broken fixture. Read the failure message and say why it failed.

**LAW-TDD-006 — Refactor only on green.**
Structural changes (renaming, extracting, removing duplication) happen only while **all** tests pass,
and must not change behavior. If a test goes red during refactor, undo the last change.

**LAW-TDD-007 — Never weaken a test to make it pass.**
Changing an assertion, deleting a test, or adding `skip` to get to green is forbidden.
If a test is genuinely wrong, say so explicitly, fix the test in its own step, and re-run RED.

**LAW-TDD-008 — Tests describe behavior, not implementation.**
Test names read like a sentence about what the user/caller observes:
`test_returns_zero_for_empty_cart`, not `test_loop_works`.
Tests use Arrange–Act–Assert and do not reach into private internals.

**LAW-TDD-009 — The whole suite stays green.**
At the end of every GREEN and REFACTOR phase, run the **entire** suite, not just the new test.

**LAW-TDD-010 — Show the evidence.**
Every gate is passed by pasting the real test output (or its key lines). No evidence → gate not passed.

---
## 2. The Gates

```
   ┌──────────┐   RED gate    ┌──────────┐  GREEN gate   ┌────────────┐  REFACTOR gate
   │  PLAN    │ ────────────▶ │   RED    │ ────────────▶ │   GREEN    │ ──────────────▶ next cycle
   │ (1 test) │               │ (failing)│               │ (passing)  │   (clean + green)
   └──────────┘               └──────────┘               └────────────┘
```

### Gate 0 — PLAN (before writing anything)
- [ ] The next behavior is stated in one sentence.
- [ ] It is the **smallest** behavior not yet covered.
- [ ] A test-name is chosen that describes it (`LAW-TDD-008`).

### Gate 1 — RED
- [ ] Exactly one new test was added (`LAW-TDD-004`).
- [ ] No production code was changed in this step (`LAW-TDD-001`).
- [ ] The test runner shows it **failing** (`LAW-TDD-010`).
- [ ] The failure reason is stated and is the *right* reason (`LAW-TDD-005`).

### Gate 2 — GREEN
- [ ] Only production code changed; the test is untouched (`LAW-TDD-007`).
- [ ] The change is the minimum needed (`LAW-TDD-003`).
- [ ] The **full** suite passes (`LAW-TDD-009`) — evidence shown.

### Gate 3 — REFACTOR
- [ ] Duplication / unclear names reviewed (it is fine to decide "nothing to refactor").
- [ ] Any change was structural only — no new behavior (`LAW-TDD-006`).
- [ ] Full suite still green — evidence shown.

---

## 3. Agent Protocol

When asked to build anything, the agent follows this loop and **pauses at each gate**:

1. **Restate the goal** and break it into a short, ordered list of behaviors (simplest first).
2. For each behavior, run one cycle: PLAN → RED → GREEN → REFACTOR.
3. After each phase, print a **Cycle Report** (format below).
4. Never batch several cycles into one big code drop.
5. Never commit or mark "done" while any test is red.

### Required Cycle Report format