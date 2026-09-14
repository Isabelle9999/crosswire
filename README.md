\# CrossWire



Verifying evaluation-sandbox containment from outside the provider's network.



When a lab reports that an evaluation sandbox held, no outside party can

currently check it — the evidence lives on the lab's machines. CrossWire lets a

verifier detect a sandbox escape without access to the provider's network: it

enumerates the classes of boundary crossing an evaluation sandbox exposes (from

the ATT\&CK-for-Containers matrix), places a verifier-held tripwire on each, and

uses a liveness audit to statistically detect a provider that installs nothing.



This repository contains the crossing map, a held-out corpus of two 2026

incidents, the wire and protocol specifications, and the code that produces the

results.



\## Setup

conda activate crosswire

pip install -r requirements.txt





\## Reproduce the results

python code/mapcheck.py map/crossing\_map.yaml # cut property + provenance

python code/analysis.py # sensitivity, liveness power

python code/score.py # coverage, standards benchmark

python code/matrix.py # control-by-phase-by-cost matrix

pytest -q



Outputs are written to `results/`.



\## Escape experiment



pip install anthropic

export ANTHROPIC\_API\_KEY=... 

python experiment/run.py --mechanism-check # testbed self-check

python experiment/run.py --live --model anthropic:claude-sonnet-4-6 --runs 30



Results are written to `results/experiment.md`. A container-based version

(`experiment/crosswire\_eval.py`, Inspect + Docker) is included and in progress.



\## Layout

map/ crossing\_map.yaml — crossing classes, wires, sensitivity parameters

corpus/ incident record and pre-registered scoring rubric

spec/ wire specifications and verification protocol

code/ analysis and scoring

experiment/ escape testbed

formal/ optional Lean cut theorem

results/ generated outputs



