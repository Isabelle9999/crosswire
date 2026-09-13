"""Sensitivity and liveness-audit analysis.

Three deterministic/statistical results, all reproducible and parameter-driven
from map/crossing_map.yaml where applicable. No external state.

1. Escape-path sensitivity (hypergeometric). A surface holds M genuine objects
   and N wires; an adversary that touches k distinct objects fires with
   probability 1 - C(M,k)/C(M+N,k). The targeted worst case is k=1, giving
   N/(M+N). We report the worst case per wired class using the reference M,N in
   the map, and a reference grid.

2. Liveness-audit power. With per-run touch probability p0 under honest
   placement, the probability of observing zero liveness fires over n runs is
   (1-p0)^n. Small values mean silent placement is implausible.

3. Partial-placement recovery. If the provider places liveness wires in only a
   fraction f of n declared runs, the fire count is Binomial(n*f, p0). The MLE
   is f_hat = F / (n*p0); we report a Wald 95% interval and the Monte-Carlo
   probability that the interval excludes f=1 (i.e. that under-placement is
   detected). This validates that the audit recovers f.

Usage:
    python code/analysis.py                       # all tables, default map
    python code/analysis.py --map map/crossing_map.yaml
"""
from __future__ import annotations
import argparse
from math import comb
from pathlib import Path
import numpy as np
import yaml

RNG = np.random.default_rng(20260913)


# ---- 1. hypergeometric sensitivity ----
def p_fire(M: int, N: int, k: int) -> float:
    k = min(k, M + N)
    if k > M:
        return 1.0
    return 1.0 - comb(M, k) / comb(M + N, k)


def sensitivity_by_class(map_path: str) -> str:
    doc = yaml.safe_load(Path(map_path).read_text(encoding="utf-8"))
    out = ["## 1. Escape-path sensitivity, per wired class",
           "",
           "Worst case is k=1 (targeted): P = N/(M+N). Reported first.",
           "",
           "| class | wire | M | N | k=1 | k=3 | k=5 | k=10 |",
           "|---|---|---|---|---|---|---|---|"]
    for c in doc["classes"]:
        if not c.get("wired"):
            continue
        M, N = int(c["M"]), int(c["N"])
        row = " | ".join(f"{p_fire(M, N, k):.2f}" for k in (1, 3, 5, 10))
        out.append(f"| {c['id']} | {c['wire_id']} | {M} | {N} | {row} |")
    out += ["",
            "Reference grid (M genuine objects, N wires):",
            "",
            "| M | N | k=1 | k=3 | k=5 | k=10 | k=20 |",
            "|---|---|---|---|---|---|---|"]
    for M, N in [(20, 2), (20, 5), (20, 10), (100, 10), (100, 30)]:
        row = " | ".join(f"{p_fire(M, N, k):.2f}" for k in (1, 3, 5, 10, 20))
        out.append(f"| {M} | {N} | {row} |")
    return "\n".join(out)


# ---- 2. liveness power ----
def liveness_power() -> str:
    out = ["## 2. Liveness-audit power: P(zero fires over n honest runs) = (1-p0)^n",
           "",
           "| p0 | n=10 | n=30 | n=100 | n=300 |",
           "|---|---|---|---|---|"]
    for p0 in (0.05, 0.10, 0.30):
        row = " | ".join(f"{(1 - p0) ** n:.1e}" for n in (10, 30, 100, 300))
        out.append(f"| {p0:.2f} | {row} |")
    return "\n".join(out)


# ---- 3. partial-placement recovery ----
def recovery(n: int = 200, p0: float = 0.10, trials: int = 2000,
             alpha: float = 0.05) -> str:
    """Test H0: f=1 (honest placement) vs H1: f<1 with a one-sided exact
    binomial test on the observed liveness fire count. Under H0 the fire count
    is Binomial(n, p0); we flag under-placement when P(X <= observed | H0) <
    alpha. This is calibrated: the flag rate at f=1 is ~alpha."""
    from scipy import stats
    out = [f"## 3. Partial-placement recovery (n={n} declared runs, p0={p0}, "
           f"{trials} trials, one-sided exact binomial at alpha={alpha})",
           "",
           "Provider places liveness wires in fraction f of n declared runs. "
           "f_hat = F/(n*p0). We flag under-placement when the observed fire "
           "count is significantly low under H0: f=1.",
           "",
           "| true f | mean f_hat | flag rate |",
           "|---|---|---|"]
    for f in (1.0, 0.5, 0.2):
        fhats, flags = [], 0
        for _ in range(trials):
            placed = RNG.random(n) < f            # which runs got liveness wires
            fires = int(np.sum(RNG.random(n)[placed] < p0))
            fhats.append(fires / (n * p0))
            pval = stats.binomtest(fires, n, p0, alternative="less").pvalue
            if pval < alpha:
                flags += 1
        label = "false-alarm" if f == 1.0 else "detects under-placement"
        out.append(f"| {f:.1f} | {np.mean(fhats):.2f} | "
                   f"{flags / trials:.2f} ({label}) |")
    out.append("")
    out.append("Reading: flag rate at f=1 is ~alpha (calibrated false alarm); "
               "at f<1 the flag rate is the audit's power to catch silent "
               "under-placement.")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", default="map/crossing_map.yaml")
    ap.add_argument("--out", default="results/analysis.md")
    args = ap.parse_args()
    text = "\n\n".join([
        "# CrossWire analysis (generated)",
        sensitivity_by_class(args.map),
        liveness_power(),
        recovery(),
    ]) + "\n"
    print(text)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"[written] {args.out}")


if __name__ == "__main__":
    main()
