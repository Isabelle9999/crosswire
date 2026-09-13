# CrossWire coverage and standards benchmark (generated)

## hugging_face

eval-sandbox escape steps: 7   downstream (platform-scope) steps: 8
CrossWire coverage: [5, 7] of 7   (single coder; interval is the robustness measure)
  (interval = [conservative/adversarial coder, primary coder]; a second independent coder and Cohen's kappa are future work)
H1 (earliest observable is shared_service_write): holds  -- earliest step S1 (2026-05-12) = shared_service_write
detection delay: earliest CrossWire fire 2026-05-12 vs recorded detection 2026-07-13 = 62 days earlier

standards benchmark (detection-evidence coverage of 7 eval-sandbox steps):

| standard | covered | kind |
|---|---|---|
| CrossWire (this work) | 7/7 | detective |
| Egress attestation (signed policy + flow-log digest) | 2/7 | detective |
| CSA AI Controls Matrix AIS-13 + vuln-ops guidance | 0/7 | preventive |
| Anthropic Aug 2026 partner practices | 0/7 | preventive |
| Mitchell R1-R5 architectural requirements | 0/7 | preventive |

downstream steps (8) are inside the victim platform; a CrossWire deployment in the evaluation sandbox does not cover them (platform-side wires, roadmap).

## dsewiki

eval-sandbox escape steps: 4   downstream (platform-scope) steps: 0
CrossWire coverage: [4, 4] of 4   (single coder; interval is the robustness measure)
  (interval = [conservative/adversarial coder, primary coder]; a second independent coder and Cohen's kappa are future work)
H1 (earliest observable is shared_service_write): does not hold  -- earliest step D1 (2026-05-24) = public_web_write
detection delay: earliest CrossWire fire 2026-05-24 vs recorded detection 2026-06-21 = 28 days earlier

standards benchmark (detection-evidence coverage of 4 eval-sandbox steps):

| standard | covered | kind |
|---|---|---|
| CrossWire (this work) | 4/4 | detective |
| Egress attestation (signed policy + flow-log digest) | 0/4 | detective |
| CSA AI Controls Matrix AIS-13 + vuln-ops guidance | 0/4 | preventive |
| Anthropic Aug 2026 partner practices | 0/4 | preventive |
| Mitchell R1-R5 architectural requirements | 0/4 | preventive |

downstream steps (0) are inside the victim platform; a CrossWire deployment in the evaluation sandbox does not cover them (platform-side wires, roadmap).
