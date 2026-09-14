"""Score the crossing map against the held-out incident record.

Produces the paper's headline results, all from data:
  - CrossWire coverage of recorded eval-sandbox escape steps, as an interval
    [adversarial-coder lower bound, primary-coder point];
  - Cohen's kappa between the primary and secondary coders;
  - the standards benchmark: detection-evidence coverage of every standard over
    the same steps;
  - hypothesis H1 (earliest observable in each OpenAI incident is a write to a
    shared mutable surface);
  - detection delay (earliest CrossWire fire vs actual detection date);
  - the control-by-step matrix.

A step "fires" for a standard S iff its crossing_class is in S's
observable_classes and the step is eval-sandbox scope. For CrossWire the
observable set is additionally intersected with the map's
wired-with-first-touch classes, so the map is the single source of truth.

Usage:
    python code/score.py
    python code/score.py --map map/crossing_map.yaml --standards corpus/standards.yaml \
        --steps corpus/steps_hf.yaml corpus/steps_dsewiki.yaml
"""
from __future__ import annotations
import argparse
from datetime import date
from pathlib import Path
import yaml


def load(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def detected_classes(map_doc) -> set[str]:
    """Classes CrossWire detects: wired with first-touch."""
    return {c["id"] for c in map_doc["classes"]
            if c.get("wired") and c.get("first_touch") is not False}


def cohen_kappa(a: list[str], b: list[str]) -> float | None:
    """Cohen's kappa for two lists of categorical labels."""
    if not a:
        return None
    n = len(a)
    cats = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = {c: a.count(c) / n for c in cats}
    pb = {c: b.count(c) / n for c in cats}
    pe = sum(pa[c] * pb[c] for c in cats)
    if abs(1 - pe) < 1e-12:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


def fires(step_class: str, observable: set[str]) -> bool:
    return step_class in observable


def score_incident(inc, map_detected, standards):
    steps = inc["steps"]
    evs = [s for s in steps if s.get("scope") == "eval_sandbox"]
    down = [s for s in steps if s.get("scope") == "downstream"]

    cw_obs = set(standards["crosswire"]["observable_classes"]) & map_detected

    # CrossWire coverage interval over eval-sandbox steps.
    primary = [fires(s["crossing_class"], cw_obs) for s in evs]
    adversarial = [fires(s.get("class_adversarial", s["crossing_class"]), cw_obs)
                   for s in evs]
    cw_point = sum(primary)
    cw_lower = sum(adversarial)
    n = len(evs)

    # Kappa on eval-sandbox steps where both coders present.
    pa = [s["crossing_class"] for s in evs if "class_secondary" in s]
    pb = [s["class_secondary"] for s in evs if "class_secondary" in s]
    kappa = cohen_kappa(pa, pb) if pa else None

    # Standards benchmark over the same eval-sandbox steps.
    bench = {}
    for name, spec in standards.items():
        obs = set(spec["observable_classes"])
        if name == "crosswire":
            obs = obs & map_detected
        bench[name] = sum(fires(s["crossing_class"], obs) for s in evs)

    # H1: earliest eval-sandbox step by order.
    earliest = min(evs, key=lambda s: s["order"]) if evs else None
    h1 = (earliest["crossing_class"] == "shared_service_write") if earliest else None

    # Detection delay: earliest CrossWire fire date vs recorded detection date.
    fire_dates = [date.fromisoformat(s["date"]) for s, f in zip(evs, primary) if f]
    det = date.fromisoformat(inc["detection_date"])
    first_fire = min(fire_dates) if fire_dates else None
    delay_days = (det - first_fire).days if first_fire else None

    return dict(inc=inc, evs=evs, down=down, n=n, cw_point=cw_point,
                cw_lower=cw_lower, kappa=kappa, bench=bench, h1=h1,
                earliest=earliest, first_fire=first_fire, delay_days=delay_days,
                cw_obs=cw_obs, standards=standards, map_detected=map_detected)


def matrix_md(r) -> str:
    standards = r["standards"]
    order = ["crosswire", "attestation", "csa_ais13", "anthropic_aug31",
             "mitchell_r1_r5"]
    order = [s for s in order if s in standards]
    head = "| step | date | phase | scope | class | " + \
           " | ".join(standards[s]["label"].split(" (")[0] for s in order) + " |"
    sep = "|" + "---|" * (5 + len(order))
    lines = [head, sep]
    for s in r["evs"] + r["down"]:
        cells = []
        for name in order:
            obs = set(standards[name]["observable_classes"])
            if name == "crosswire":
                obs = obs & r["map_detected"]
            hit = "fires" if (s.get("scope") == "eval_sandbox"
                              and fires(s["crossing_class"], obs)) else "-"
            cells.append(hit)
        lines.append(f"| {s['id']} | {s['date']} | {s['phase']} | "
                     f"{s.get('scope')} | {s['crossing_class']} | "
                     + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", default="map/crossing_map.yaml")
    ap.add_argument("--standards", default="corpus/standards.yaml")
    ap.add_argument("--steps", nargs="+",
                    default=["corpus/steps_hf.yaml", "corpus/steps_dsewiki.yaml"])
    args = ap.parse_args()

    map_doc = load(args.map)
    map_detected = detected_classes(map_doc)
    standards = load(args.standards)["standards"]

    cov_lines = ["# CrossWire coverage and standards benchmark (generated)", ""]
    mat_lines = ["# Control-by-step matrix (generated)", ""]
    print("=" * 70)

    for sp in args.steps:
        inc = load(sp)
        r = score_incident(inc, map_detected, standards)
        name = inc["incident"]
        cov_lines.append(f"## {name}")
        cov_lines.append("")
        cov_lines.append(f"eval-sandbox escape steps: {r['n']}   "
                         f"downstream (platform-scope) steps: {len(r['down'])}")
        kv = f"kappa = {r['kappa']:.2f} (primary by-object vs secondary by-tactic)" \
            if r['kappa'] is not None \
            else "single coder; interval is the robustness measure"
        cov_lines.append(f"CrossWire coverage: [{r['cw_lower']}, {r['cw_point']}] "
                         f"of {r['n']}   ({kv})")
        cov_lines.append("  (interval = [conservative/adversarial coder, "
                         "primary coder]; kappa is between two matching rubrics "
                         "coded by one author; a second independent human coder "
                         "is future work)")
        h1s = {True: "holds", False: "does not hold", None: "n/a"}[r["h1"]]
        if r["earliest"]:
            cov_lines.append(f"H1 (earliest observable is shared_service_write): "
                             f"{h1s}  -- earliest step {r['earliest']['id']} "
                             f"({r['earliest']['date']}) = "
                             f"{r['earliest']['crossing_class']}")
        if r["delay_days"] is not None:
            cov_lines.append(f"detection delay: earliest CrossWire fire "
                             f"{r['first_fire']} vs recorded detection "
                             f"{inc['detection_date']} = {r['delay_days']} days earlier")
        cov_lines.append("")
        cov_lines.append("standards benchmark (detection-evidence coverage of "
                         f"{r['n']} eval-sandbox steps):")
        cov_lines.append("")
        cov_lines.append("| standard | covered | kind |")
        cov_lines.append("|---|---|---|")
        for nm, spec in standards.items():
            cov_lines.append(f"| {spec['label']} | {r['bench'][nm]}/{r['n']} | "
                             f"{spec['kind']} |")
        cov_lines.append("")
        cov_lines.append(f"downstream steps ({len(r['down'])}) are inside the "
                         "victim platform; a CrossWire deployment in the "
                         "evaluation sandbox does not cover them (platform-side "
                         "wires, roadmap).")
        cov_lines.append("")

        mat_lines.append(f"## {name}")
        mat_lines.append("")
        mat_lines.append(matrix_md(r))
        mat_lines.append("")

        # console summary
        print(f"{name}: CrossWire [{r['cw_lower']}, {r['cw_point']}]/{r['n']}  "
              f"kappa={kv}  H1={h1s}  "
              f"delay={r['delay_days']}d  "
              f"attestation={r['bench'].get('attestation')}/{r['n']}")

    Path("results").mkdir(exist_ok=True)
    Path("results/coverage.md").write_text("\n".join(cov_lines), encoding="utf-8")
    Path("results/matrix.md").write_text("\n".join(mat_lines), encoding="utf-8")
    print("=" * 70)
    print("[written] results/coverage.md, results/matrix.md")


if __name__ == "__main__":
    main()
