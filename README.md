# codex-harness-factory

`codex-harness-factory` is a deterministic, Python-first meta-harness that generates reusable Codex harnesses from natural-language markdown requests.

MVP contract:

```bash
python -m codex_harness_factory examples/writeup-crud.request.md --out generated/writeup-crud-harness
```

The MVP keeps live outputs in ignored directories (`generated/` and `_workspace/`) and verifies generated content against tracked golden fixtures.

Run the repository verification gate before handoff:

```bash
./scripts/verify.sh
```
