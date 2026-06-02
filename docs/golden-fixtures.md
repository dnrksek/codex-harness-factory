# Golden Fixtures

Golden fixtures are tracked expected outputs for deterministic harness generation. They are distinct from live generated output and runtime workspace intermediates.

## Ownership

- `generated/` is ignored live output produced by local factory runs.
- `tests/fixtures/*` is tracked expected output used by verification.
- `_workspace/` is ignored runtime metadata, validation, and quality-report output.
- Normal verification compares live output against tracked golden fixtures.
- Normal verification must not mutate golden fixtures.

Current fixtures:

| Fixture | Request | Live output | Golden fixture |
| --- | --- | --- | --- |
| `writeup-crud` | `examples/writeup-crud.request.md` | `generated/writeup-crud-harness` | `tests/fixtures/writeup-crud-harness` |
| `python-debug` | `examples/python-debug.request.md` | `generated/python-debug-harness` | `tests/fixtures/python-debug-harness` |
| `paper-summary` | `examples/paper-summary.request.md` | `generated/paper-summary-harness` | `tests/fixtures/paper-summary-harness` |

## Intentional update workflow

Use the update helper only when a generated harness change is intentional and the expected output should change:

```bash
./scripts/update-golden.sh writeup-crud
./scripts/update-golden.sh python-debug
./scripts/update-golden.sh paper-summary
```

The script:

1. rejects unknown fixture names.
2. maps the fixture name to a fixed request/output/golden path.
3. runs the factory command for that fixture.
4. confirms the live generated output exists.
5. confirms the golden target is under `tests/fixtures/`.
6. replaces only the selected fixture's golden directory.
7. runs `./scripts/verify.sh` after updating.
8. prints the changed fixture path and reminds the user to inspect `git diff`.

## Review requirement

Before committing a golden fixture update, inspect the fixture diff:

```bash
git diff -- tests/fixtures/<fixture>-harness
```

Also confirm runtime outputs remain untracked:

```bash
git ls-files generated _workspace .omx
```

The command should print no tracked runtime files.
