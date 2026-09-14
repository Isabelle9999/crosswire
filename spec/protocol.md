# Verification protocol

The protocol by which a verifier establishes containment of an evaluation
sandbox without access to the provider's network. Roles, two deployment modes,
the liveness audit and its statistical test, spot inspection, disclosure
semantics, the no-training rule, and what each mode cannot see.

## Roles

- **Verifier** -- issues wires, holds the monitor, publishes per-surface
  sensitivity, receives fires. An external evaluator (AISI, METR, Apollo) or a
  regulator acting under EU AI Act Article 92.
- **Provider** -- runs the evaluation, places wires per the wire specification,
  and declares a run manifest: run ids, environment class, and the wire ids
  placed in each run.
- **Platform (Mode-B extension, roadmap)** -- a third-party service that may be
  a target can register a monitored namespace so that a public-web-write wire
  landing on it fires directly.

## Run manifest

For each evaluation batch the provider declares, to the verifier:
`{run_id, environment_class, wires_placed:[wire_id...], n_runs}`. The manifest
is the provider's declaration; the liveness audit and spot inspection are how
the verifier checks it without entering the network.

## Mode A -- verifier-run evaluation

The verifier operates the harness (Inspect-style) on the provider's model.
Egress is restricted to the model API endpoint; the verifier observes that
boundary directly. Wires are placed by the verifier's setup step; liveness fires
are observed at the API side in real time. A fire halts the run and alerts the
verifier. This is the strong mode and matches an Article 92 evaluation.

What Mode A cannot see: an escape that never crosses a wired boundary (timing or
hardware channels; lateral movement that stays inside a single container with no
decoy on the path). These are the residual named in the crossing map.

## Mode B -- provider-run evaluation

The provider runs the harness and places wires from the verifier's issuance.
Escape-path fires reach the verifier through the escape route itself: a wire
that phones home can only do so if containment failed, so the verifier receives
the fire precisely when it matters. Liveness is verified from the declared
manifest plus fire counts (below) plus random spot inspection.

What Mode B cannot see: it relies on a truthful manifest for the run count and
on correct placement. The liveness audit catches systematic under-placement
statistically; spot inspection catches non-representative environments on a
sample. It does not catch a provider that places wires correctly in exactly the
audited runs and omits them elsewhere in a way uncorrelated with the audit --
which is why the audit sample must be drawn by the verifier, not the provider,
and why Mode A is preferred where the stakes justify it.

## Liveness audit

Liveness wires sit on the normal task path with a known honest touch probability
p0 (calibrated per environment class). Over n honest runs the probability of
zero liveness fires is (1-p0)^n. The verifier tests the provider's declared runs
against this:

- **Nominal-compliance test.** H0: placement is honest (fraction f = 1 of
  declared runs carry liveness wires). The observed liveness fire count is
  Binomial(n, p0) under H0. The verifier flags under-placement when the observed
  count is significantly low by a one-sided exact binomial test at a
  pre-registered alpha. `code/analysis.py` shows the calibration: at alpha=0.05
  the false-alarm rate at f=1 is ~0.02, power is ~0.80 at f=0.5 and ~1.00 at
  f=0.2 for n=200, p0=0.10.
- **Calibration and drift.** p0 is measured per environment class on known-good
  runs. The verifier recalibrates when the environment class changes and flags
  divergence in either direction: too few fires suggests under-placement; too
  many suggests a misconfigured environment.

## Spot inspection (Mode B)

The verifier draws a random sample of declared runs and inspects the placed
environment: are the wire ids in the manifest actually present, in
representative positions, in the runs that matter? The sampling rule and sample
size are fixed in advance; findings are recorded. This is the on-site element
that the CTBT analogy lacks and that IAEA-style accounting requires: a
declaration is verified against an independent check, not trusted.

## Disclosure semantics

- Mode A: a fire halts the run and is recorded by the verifier.
- Mode B: a fire is a disclosure trigger to the verifier -- a party with no
  incentive to keep the run going. This is the contribution over "more alarms":
  relocating the alarm to a party that loses nothing by acting is what changes
  the outcome. In the July incident the provider's on-call saw an alert and did
  not halt.

## No-training rule

No fire, wire value, or placement detail may enter any training set, any reward,
or any document the evaluated model can read. Training against a monitor
produces obfuscation rather than less misbehaviour (Baker et al. 2025), and even
documents describing a monitor induce obfuscation. A regime that trained agents
to avoid wires would select for covert competence; the protocol forbids it and
the paper names the second-order cost.

## Confidentiality and retention

Wire values are per-run unique and discarded after the run; the verifier retains
only fire records and the manifest. The provider's proprietary environment is
never transmitted to the verifier; the verifier transmits only wire issuance.
