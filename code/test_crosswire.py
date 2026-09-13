"""Fast tests for the pure-Python pieces. Run: pytest -q  (from repo root)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
sys.path.insert(0, str(ROOT / "experiment"))

import analysis
import score


def test_p_fire_worst_case():
    # targeted worst case k=1 is N/(M+N)
    assert abs(analysis.p_fire(20, 5, 1) - 5 / 25) < 1e-9
    assert analysis.p_fire(10, 10, 20) == 1.0  # k exceeds M -> certain


def test_wilson_bounds():
    import importlib
    run = importlib.import_module("run")
    lo, hi = run.wilson(5, 10)
    assert 0 <= lo <= 0.5 <= hi <= 1


def test_cohen_kappa_perfect_and_chance():
    assert score.cohen_kappa(["a", "b", "a"], ["a", "b", "a"]) == 1.0
    # all same label on both sides but constant -> defined as perfect
    assert score.cohen_kappa(["a", "a"], ["a", "a"]) == 1.0


def test_mapcheck_passes():
    r = subprocess.run([sys.executable, "code/mapcheck.py", "map/crossing_map.yaml"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_scorer_runs_and_writes():
    r = subprocess.run([sys.executable, "code/score.py"], cwd=ROOT,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert (ROOT / "results" / "coverage.md").exists()
    assert "CrossWire" in (ROOT / "results" / "coverage.md").read_text()


def test_mechanism_check_passes():
    r = subprocess.run([sys.executable, "run.py", "--mechanism-check"],
                       cwd=ROOT / "experiment", capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
