"""Build the control-by-phase-by-cost matrix (the organizers' Track-1 brief #4).

Rows: the controls the organizers name (canary credentials, egress tripwires,
credential scoping, kill criteria, allowlisted proxy) plus CrossWire's wire
classes. Columns: the phases of each incident, in order. A cell is 'fires' if
the control is detective and addresses a crossing class present in that phase;
'prevents' if the control is preventive (stops the step but yields no
third-party evidence); '-' otherwise. Extra columns: implement cost, operate
cost, and who can verify it (verifier / provider / none).

Every cell traces to a step in corpus/steps_*.yaml.

Usage: python code/matrix.py
"""
from __future__ import annotations
from pathlib import Path
import yaml


def load(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


# Controls: the organizers' named set + CrossWire wire classes.
# addresses = crossing classes the control acts on; kind = detective|preventive;
# custody = who holds the evidence a third party would need.
CONTROLS = [
    # organizers' named controls
    {"name": "Canary credentials", "addresses": {"credential"},
     "kind": "detective", "custody": "verifier",
     "implement": "3h", "operate": "low", "note": "== CrossWire W3"},
    {"name": "Egress tripwires", "addresses": {"egress_dns", "egress_http"},
     "kind": "detective", "custody": "verifier",
     "implement": "2h", "operate": "low", "note": "== CrossWire W1/W2"},
    {"name": "Credential scoping", "addresses": {"credential"},
     "kind": "preventive", "custody": "provider",
     "implement": "4h", "operate": "low",
     "note": "prevents; no third-party evidence when bypassed"},
    {"name": "Kill criteria", "addresses": set(),
     "kind": "preventive", "custody": "provider",
     "implement": "2h", "operate": "low",
     "note": "response control; depends on a detection signal to trigger"},
    {"name": "Allowlisted proxy", "addresses": {"egress_http", "egress_dns",
                                                "egress_rawsocket"},
     "kind": "preventive", "custody": "provider",
     "implement": "4h", "operate": "medium",
     "note": "prevents egress; attested only via provider-held flow logs"},
    # CrossWire wire classes
    {"name": "CrossWire W1 (egress DNS)", "addresses": {"egress_dns"},
     "kind": "detective", "custody": "verifier", "implement": "2h", "operate": "low"},
    {"name": "CrossWire W2 (egress HTTP)", "addresses": {"egress_http"},
     "kind": "detective", "custody": "verifier", "implement": "2h", "operate": "low"},
    {"name": "CrossWire W3 (credential)", "addresses": {"credential"},
     "kind": "detective", "custody": "verifier", "implement": "3h", "operate": "low"},
    {"name": "CrossWire W4 (shared-service write)",
     "addresses": {"shared_service_write", "artifact_store"},
     "kind": "detective", "custody": "verifier", "implement": "6h", "operate": "medium"},
    {"name": "CrossWire W5 (public-web write)", "addresses": {"public_web_write"},
     "kind": "detective", "custody": "verifier", "implement": "4h", "operate": "medium"},
    {"name": "CrossWire W6 (host metadata)", "addresses": {"host_metadata"},
     "kind": "detective", "custody": "verifier", "implement": "8h", "operate": "medium"},
    {"name": "CrossWire W7 (control plane)", "addresses": {"control_plane"},
     "kind": "detective", "custody": "verifier", "implement": "5h", "operate": "medium"},
]


def phases_in_order(steps):
    seen = []
    for s in steps:
        if s.get("scope") == "eval_sandbox" and s["phase"] not in seen:
            seen.append(s["phase"])
    return seen


def classes_by_phase(steps):
    d = {}
    for s in steps:
        if s.get("scope") == "eval_sandbox":
            d.setdefault(s["phase"], set()).add(s["crossing_class"])
    return d


def cell(ctrl, phase_classes):
    hit = ctrl["addresses"] & phase_classes
    if ctrl["kind"] == "detective":
        return "fires" if hit else "-"
    return "prevents" if hit else "-"


def matrix_for(inc):
    steps = inc["steps"]
    phases = phases_in_order(steps)
    cbp = classes_by_phase(steps)
    header = ("| control | " + " | ".join(phases) +
              " | implement | operate | verifiable by |")
    sep = "|" + "---|" * (len(phases) + 4)
    lines = [f"## {inc['incident']}", "", header, sep]
    for c in CONTROLS:
        cells = [cell(c, cbp.get(p, set())) for p in phases]
        verifiable = c["custody"] if c["kind"] == "detective" else "none (preventive)"
        lines.append("| " + c["name"] + " | " + " | ".join(cells) +
                     f" | {c['implement']} | {c['operate']} | {verifiable} |")
    return "\n".join(lines)


def main():
    out = ["# Control by phase by cost (generated)", "",
           "Rows: the organizers' named controls plus CrossWire wire classes. "
           "Cells: fires = detective control observes this phase; prevents = "
           "preventive control stops the step but yields no third-party "
           "evidence; - = no effect. Every column is a documented phase; every "
           "cell traces to a step in corpus/steps_*.yaml.", ""]
    for sp in ("corpus/steps_hf.yaml", "corpus/steps_dsewiki.yaml"):
        out.append(matrix_for(load(sp)))
        out.append("")
    Path("results").mkdir(exist_ok=True)
    Path("results/control_matrix.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    print("\n[written] results/control_matrix.md")


if __name__ == "__main__":
    main()
