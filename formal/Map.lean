/-
CrossWire cut property, Lean 4 (optional; needs the Lean toolchain).
Mirrors map/crossing_map.yaml: every crossing class is wired-with-first-touch or
explicitly excluded (residual), so the wired classes form a cut separating
INSIDE from OUTSIDE. `native_decide` checks the concrete map. Core only; no
Mathlib.

Run inside a Lake project, or: `lean --run formal/Map.lean` after `#eval main`.
-/

inductive Cover where
  | wired      -- wired with a first-touch wire
  | excluded   -- out of scope (acknowledged residual)
  | uncovered  -- neither: would break the cut
  deriving DecidableEq, Repr

structure CrossingClass where
  name  : String
  cover : Cover
  deriving Repr

/-- The concrete map, mirroring map/crossing_map.yaml. -/
def crossingMap : List CrossingClass :=
  [ ⟨"egress_dns",            .wired⟩,
    ⟨"egress_http",           .wired⟩,
    ⟨"egress_rawsocket",      .wired⟩,
    ⟨"credential",            .wired⟩,
    ⟨"shared_service_write",  .wired⟩,
    ⟨"artifact_store",        .wired⟩,
    ⟨"host_metadata",         .wired⟩,
    ⟨"control_plane",         .wired⟩,
    ⟨"public_web_write",      .wired⟩,
    ⟨"timing_channel",        .excluded⟩,
    ⟨"hardware_sidechannel",  .excluded⟩,
    ⟨"internal_only_lateral", .excluded⟩,
    ⟨"human_insider",         .excluded⟩ ]

/-- A class is covered iff it is wired or explicitly excluded. -/
def isCovered (c : CrossingClass) : Bool := c.cover != Cover.uncovered

/-- The cut holds iff no class is left uncovered. -/
def cutHolds : Bool := crossingMap.all isCovered

/-- Machine-checked: the cut property holds on the concrete map. -/
theorem cut_holds : cutHolds = true := by native_decide

/-- Number of wired-with-first-touch classes. -/
def wiredCount : Nat :=
  (crossingMap.filter (fun c => c.cover == Cover.wired)).length

/-- Machine-checked: there are nine wired classes. -/
theorem wired_count_nine : wiredCount = 9 := by native_decide

def main : IO Unit := do
  IO.println s!"cut holds: {cutHolds}"
  IO.println s!"wired-with-first-touch classes: {wiredCount}"
