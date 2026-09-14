# Control by phase by cost (generated)

Rows: the organizers' named controls plus CrossWire wire classes. Cells: fires = detective control observes this phase; prevents = preventive control stops the step but yields no third-party evidence; - = no effect. Every column is a documented phase; every cell traces to a step in corpus/steps_*.yaml.

## hugging_face

| control | coordination | egress | privilege_escalation | evasion | lateral_movement | implement | operate | verifiable by |
|---|---|---|---|---|---|---|---|---|
| Canary credentials | - | - | - | - | - | 3h | low | verifier |
| Egress tripwires | - | fires | - | - | - | 2h | low | verifier |
| Credential scoping | - | - | - | - | - | 4h | low | none (preventive) |
| Kill criteria | - | - | - | - | - | 2h | low | none (preventive) |
| Allowlisted proxy | - | prevents | - | - | - | 4h | medium | none (preventive) |
| CrossWire W1 (egress DNS) | - | - | - | - | - | 2h | low | verifier |
| CrossWire W2 (egress HTTP) | - | fires | - | - | - | 2h | low | verifier |
| CrossWire W3 (credential) | - | - | - | - | - | 3h | low | verifier |
| CrossWire W4 (shared-service write) | fires | - | - | fires | - | 6h | medium | verifier |
| CrossWire W5 (public-web write) | - | - | - | - | - | 4h | medium | verifier |
| CrossWire W6 (host metadata) | - | - | - | - | - | 8h | medium | verifier |
| CrossWire W7 (control plane) | - | - | fires | - | fires | 5h | medium | verifier |

## dsewiki

| control | coordination | implement | operate | verifiable by |
|---|---|---|---|---|
| Canary credentials | - | 3h | low | verifier |
| Egress tripwires | - | 2h | low | verifier |
| Credential scoping | - | 4h | low | none (preventive) |
| Kill criteria | - | 2h | low | none (preventive) |
| Allowlisted proxy | - | 4h | medium | none (preventive) |
| CrossWire W1 (egress DNS) | - | 2h | low | verifier |
| CrossWire W2 (egress HTTP) | - | 2h | low | verifier |
| CrossWire W3 (credential) | - | 3h | low | verifier |
| CrossWire W4 (shared-service write) | - | 6h | medium | verifier |
| CrossWire W5 (public-web write) | fires | 4h | medium | verifier |
| CrossWire W6 (host metadata) | - | 8h | medium | verifier |
| CrossWire W7 (control plane) | - | 5h | medium | verifier |
