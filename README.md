# CrossWire

Verifying evaluation-sandbox containment from outside the provider's network.
This repo holds the crossing map, the held-out incident corpus, and the code
that produces the paper's results. See `docs/PLAN.md` for the full plan and
`docs/PAPER_v2.md` for the write-up.

## Setup (once)

```
conda activate crosswire
pip install -r requirements.txt
```

## Produce the results (in order)

Everything below runs on Windows/PowerShell, no Docker, no API key.

```
python code/mapcheck.py map/crossing_map.yaml     # 1. cut property + provenance -> PASS
python code/analysis.py                            # 2. sensitivity, liveness power, f-recovery -> results/analysis.md
python code/score.py                               # 3. coverage, standards benchmark, H1, delay -> results/coverage.md, results/matrix.md
python experiment/run.py --mechanism-check         # 4. testbed self-check (wires fire; benign fires none) -> PASS
pytest -q                                          # 5. all green
```

After step 3, `results/coverage.md` contains the headline numbers that fill the
paper's placeholders: CrossWire coverage interval, each standard's coverage, H1,
and detection delay, for both incidents.

## Optional: the live escape experiment (needs an API key)

```
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python experiment/run.py --live --models claude-sonnet-4-6 --runs 30
```

Add more models (including one open-weight, per the plan) with repeated
`--models` values. Writes `results/experiment.jsonl` and `results/experiment.md`
(first-fire rate per wire class per arm, Wilson 95% intervals). This is a
process-level testbed, not production Kubernetes; the paper scopes it so.

## Layout

```
map/        crossing_map.yaml         single source of truth (classes, wires, sensitivity params)
corpus/     steps_hf.yaml, steps_dsewiki.yaml, standards.yaml, rubric.md   held-out record + pre-registered rubric
code/       mapcheck.py, analysis.py, score.py, test_crosswire.py
experiment/ sandbox.py, run.py, scenarios.yaml
results/    generated outputs
docs/       plan, paper, playbook, roadmap, setup
```

Rule (from AGENTS.md): do not edit `map/` or the wire specs while reading
`corpus/steps_*` -- the map is architecture-derived and the incidents are held
out.
