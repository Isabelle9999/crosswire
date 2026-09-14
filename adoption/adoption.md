# Adoption package

Where CrossWire slots into existing standards and instruments. Each mapping
states, clause by clause, what the standard says and what CrossWire adds.

## Anthropic August 2026 partner practices

| Anthropic practice | CrossWire relation |
|---|---|
| No-internet sandbox | extends: CrossWire's W1/W2/W2b make a breach of this observable to an outside party; the practice prevents, CrossWire detects when prevention fails. |
| API-only egress | covered by Mode A: the verifier operates exactly this boundary and observes it. |
| Credentials outside the sandbox | extends: W3 places a zero-privilege decoy so that any attempt to use an in-sandbox credential fires. |
| Pre-engagement probe (Parallax-style) | extends: the probe is provider-run and self-verified; CrossWire moves the check to the verifier. |
| Real-time scope monitoring | extends: the monitoring signal is provider-held; CrossWire's fires are verifier-held, which is the property a third party needs. |

Where the practices say containment "should be verified before every
evaluation," CrossWire supplies the missing "by whom and how": by the verifier,
via issued wires, at a stated sensitivity.

## CSA AI Controls Matrix AIS-13 and the Catastrophic Risk Annex

AIS-13 (AI sandboxing) and the vulnerability-operations guidance require no
egress and no live production credentials. These are preventive controls with no
third-party evidence when bypassed. CrossWire is filed as **testing criteria and
evidence requirements for AIS-13** under CSA's STAR for AI Catastrophic Risk
Annex (rollout June 2026 - December 2027), which is collecting exactly this for
controls covering loss of oversight and uncontrolled behaviour. The wire matrix
maps to AI-CAIQ question candidates: for each crossing class, "does an
independent party receive evidence of a crossing without provider network
access? (wire id, sensitivity)". Routed through the sprint's delivery commitment
for control matrices.

## EU AI Act

- **Article 91 (request for information).** A regulator may request the run
  manifest and the verifier's fire log for a given evaluation. CrossWire defines
  what such a request would ask for: manifest, wire issuance record, fire log,
  published sensitivity.
- **Article 92 (evaluations).** Mode A **is** the shape of an Article 92
  evaluation: the AI Office (or an appointed evaluator) runs the harness on the
  provider's model with verifier-issued wires. The AI Office can require it
  directly.
- **Article 93 (corrective measures).** A fire is grounds for a requested
  measure; the fire record is the evidence. A missing manifest or a failed
  liveness audit is itself a signal under Article 93.

## External-evaluator agreement template

A clause for engagements between a provider and an external evaluator:

> The Provider shall place, in every evaluation run within scope, the wire set
> issued by the Evaluator per the CrossWire wire specification, and shall
> declare a run manifest. The Evaluator shall hold the monitor and shall not
> transmit wire values or fire records into any training corpus. Placement is
> subject to the Evaluator's liveness audit and random spot inspection. A fire
> is disclosed to the Evaluator and does not, by itself, constitute a breach of
> this agreement; failure to place wires, or a failed liveness audit, does.

## Second hop

The July escape staged on a third party's compute (a user-hosted code-execution
sandbox), not a lab environment. CrossWire's W3 and W5 fire wherever the agent
stands: a provider-issued credential used from a third party's compute still
authenticates against the provider's IAM and fires; a marker seeded in the
environment still appears on a public surface and fires. Obligations on the
hosting provider -- what a platform owes when its compute is used as a staging
base -- are outside CrossWire's scope; the platform-registry branch of the
roadmap is the extension that would place wires platform-side.
