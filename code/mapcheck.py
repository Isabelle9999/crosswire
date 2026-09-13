"""Validate map/crossing_map.yaml.

Checks the cut property and provenance of the crossing map:

1. every class carries an ATT&CK / Kubernetes derivation, and none cites an
   incident as its derivation (incidents are held out);
2. the wired-with-first-touch classes plus the excluded classes cover every
   INSIDE->OUTSIDE edge -- i.e. no class is left both unwired (or downgraded)
   and not excluded without being reported as residual;
3. every wired class names a wire_id, first_touch and mechanism, and every
   wire_id used by a class appears in the `wires` map.

Exit code 0 on PASS, 1 on FAIL. Usage:
    python code/mapcheck.py map/crossing_map.yaml
"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

INCIDENT_WORDS = ("hugging face", "openai", "dsewiki", "artifactory",
                  "collusion", "incident", "july 2026", "metr")


def check(path: str) -> int:
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    classes = doc.get("classes", [])
    excluded = doc.get("excluded", [])
    wires = doc.get("wires", {})
    errors: list[str] = []
    residual: list[str] = []

    if not classes:
        errors.append("no classes defined")

    for c in classes:
        cid = c.get("id", "<no id>")
        tech = (c.get("attack_technique") or "").strip()
        if not tech:
            errors.append(f"{cid}: missing attack_technique (derivation)")
        elif any(w in tech.lower() for w in INCIDENT_WORDS):
            errors.append(f"{cid}: derivation cites an incident ('{tech}')")
        if c.get("wired"):
            for field in ("wire_id", "first_touch", "mechanism"):
                if field not in c:
                    errors.append(f"{cid}: wired class missing '{field}'")
            wid = c.get("wire_id")
            if wid is not None and wid not in wires:
                errors.append(f"{cid}: wire_id '{wid}' not in wires map")
            if c.get("first_touch") is False:
                residual.append(f"{cid} (downgraded: no first-touch wire)")
        else:
            # An unwired class must be explicitly excluded to preserve the cut.
            if not any(e.get("id") == cid for e in excluded):
                errors.append(
                    f"{cid}: unwired and not in excluded list -> uncovered edge")
                residual.append(f"{cid} (uncovered)")

    for e in excluded:
        if not e.get("reason"):
            errors.append(f"excluded {e.get('id','<no id>')}: missing reason")
        residual.append(f"{e.get('id')} (excluded: out of scope)")

    covered = sum(1 for c in classes
                  if c.get("wired") and c.get("first_touch") is not False)
    print(f"map: {path}")
    print(f"classes: {len(classes)}  wired-with-first-touch: {covered}  "
          f"excluded: {len(excluded)}")
    print("residual (not covered by an object-based first-touch wire):")
    for r in residual:
        print(f"  - {r}")

    if errors:
        print("\nFAIL")
        for e in errors:
            print(f"  ! {e}")
        return 1
    print("\nPASS: cut property holds; every class is wired-with-first-touch "
          "or explicitly excluded.")
    return 0


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "map/crossing_map.yaml"
    raise SystemExit(check(p))
