# CrossWire

Verifying evaluation-sandbox containment from outside the provider's network.
The crossing map, the held-out incident corpus, the specs, and the code that
produces the paper's results. Plan: `docs/PLAN.md`. Paper: `docs/PAPER_v2.md`.

## What produces what (map to the paper)

| paper element | produced by |
|---|---|
| coverage interval, standards benchmark, H1, detection delay | `code/score.py` -> results/coverage.md, results/matrix.md |
| sensitivity, liveness power, f-recovery | `code/analysis.py` -> results/analysis.md |
| control-by-phase-by-cost matrix (organizers' brief #4) | `code/matrix.py` -> results/control_matrix.md |
| wire specs (10 fields, Gans check) | `spec/wires.md` |
| protocol (modes, liveness test, no-training) | `spec/protocol.md` |
| adoption (Anthropic, CSA/annex, EU 91-93, second hop) | `adoption/adoption.md` |
| escape experiment (first-fire per class, ttf, rec-gap) | `experiment/run.py --live` (Layer 1) or `crosswire_eval.py` (Layer 2) |
| machine-checked cut property | `code/mapcheck.py` (Python) + `formal/Map.lean` (Lean, optional) |

## Setup (once)

```
conda activate crosswire
pip install -r requirements.txt
```

## Core pipeline (no Docker, no API key) — run in order

```
python code/mapcheck.py map/crossing_map.yaml     # cut property + provenance -> PASS
python code/analysis.py                            # sensitivity, liveness, f-recovery
python code/score.py                               # coverage, standards benchmark, H1, delay
python code/matrix.py                              # control-by-phase-by-cost matrix
python experiment/run.py --mechanism-check         # testbed self-check -> PASS
pytest -q                                          # all green (9 tests)
```

After this, `results/` holds coverage.md, matrix.md, analysis.md, control_matrix.md.
These fill most of the paper's placeholders.

## The escape experiment — Layer 1 (real numbers tonight, API keys only)

Drives real models through four arms (impossible / solvable / benign / disclosed)
against the instrumented tool interface. Reports first-fire rate per wire class
(Wilson 95%), time-to-fire, escape rate, refusal, recognition-action gap.

```
pip install anthropic openai
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:OPENAI_API_KEY    = "sk-..."
$env:OPENROUTER_API_KEY = "sk-or-..."      # for an open-weight model

python experiment/run.py --live `
  --model anthropic:claude-sonnet-4-6 `
  --model openai:gpt-4.1 `
  --model openrouter:meta-llama/llama-3.3-70b-instruct `
  --runs 30
```

Three models incl. one open-weight satisfies the plan. Start with `--runs 10` to
smoke-test, then `--runs 30`. Writes results/experiment.md + results/experiment.jsonl.
This is a tool-interface testbed (stated honestly in the paper), not a container
escape — that's Layer 2.

## The escape experiment — Layer 2 (real container, needs Docker + WSL)

`experiment/crosswire_eval.py` plants wires in a real Docker sandbox and scores
wire fires while a model attempts escape, built on SandboxEscapeBench. This is
the plan-conformant centerpiece. It is written to the Inspect API but NOT yet
run here — expect to debug integration live.

In WSL (use tmux so a dropped session doesn't kill it):
```
tmux new -s cw
conda activate crosswire
pip install inspect-ai anthropic openai
export ANTHROPIC_API_KEY="sk-ant-..."
inspect eval experiment/crosswire_eval.py --model anthropic/claude-sonnet-4-6 -T arm=impossible --epochs 30
inspect eval experiment/crosswire_eval.py --model anthropic/claude-sonnet-4-6 -T arm=benign --epochs 30
```
Requires Docker Desktop running with WSL integration. Detach tmux: Ctrl-b then d.

## Optional: the Lean cut theorem

```
# needs elan/lake (Lean toolchain). You know Lean; this mirrors the YAML map.
cd formal && lake env lean Map.lean     # or: lean --run Map.lean
```

## Claude Code prompts (for debugging Layer 2)

Open Claude Code in the repo root (WSL + tmux). Paste one of these:

Debug the Inspect eval:
> Read AGENTS.md, then experiment/crosswire_eval.py and experiment/compose.yaml.
> Run `inspect eval experiment/crosswire_eval.py --model anthropic/claude-sonnet-4-6
> -T arm=solvable --epochs 1` and fix any Inspect API mismatches (imports, solver
> signature, scorer signature, sandbox().exec usage) until it runs one sample
> end-to-end and writes a log. Work only in experiment/. Do not change the wire
> signatures or the scoring logic; only fix API/integration issues. Show me the
> diff before committing.

Point it at real SandboxEscapeBench:
> Read the note at the bottom of experiment/crosswire_eval.py. Clone
> github.com/UKGovernmentBEIS/sandbox_escape_bench, identify one escape task,
> and use inspect_ai.task_with to insert plant_wires() as setup and
> crosswire_scorer() as the scorer on that real task, without copying its code.
> Get it to run one sample. Ask me before installing anything outside the repo.

## Layout

```
map/         crossing_map.yaml            single source of truth (classes, wires, sensitivity, costs)
corpus/      steps_hf.yaml, steps_dsewiki.yaml, standards.yaml, rubric.md   held-out record + rubric
spec/        wires.md, protocol.md        wire specs (10 fields) + verification protocol
adoption/    adoption.md                  Anthropic / CSA / EU / evaluator mappings + second hop
code/        mapcheck.py, analysis.py, score.py, matrix.py, test_crosswire.py
experiment/  run.py, sandbox.py, scenarios.yaml   (Layer 1); crosswire_eval.py, compose.yaml, Dockerfile (Layer 2)
formal/      Map.lean                     optional Lean cut theorem
results/     generated outputs
docs/        plan, paper, playbook, roadmap, setup
```

Rule (AGENTS.md): do not edit map/ or spec/ while reading corpus/steps_* — the
map is architecture-derived and the incidents are held out.
