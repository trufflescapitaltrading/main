## V71 MNQ/MES 3m “no trades” fix

This bot can end up taking **zero trades on MNQ 3m / MES 3m** even when conditions warrant, primarily because:

1) In **Filter Harmony** mode, the **Higher‑TF permission chain** (`permLongOK` / `permShortOK`) is used as a **hard entry gate**:

```pine
fhCandidateLong = canGoLong and permLongOK and ...
fhCandidateShort = canGoShort and permShortOK and ...
```

On 3m charts, that permission chain depends on 5m EMA/SMA conditions that can stay false for long stretches → Harmony candidates never become eligible.

2) The **MTF STRICT filter** can still hard‑block **Harmony-derived** entries (especially those labeled `"HARMONY"`), even though Harmony already scores MTF/HTF conditions and is intended to keep those filters “soft”.

Below are the two minimal code changes to restore 3m entries **only when your signals/priority logic say so**, while still keeping the permission/MTF logic as a quality enhancer.

---

### Change 1 — Make permission-chain “soft” in Filter Harmony (allow strong-signal bypass)

**Find** this section inside the Filter Harmony block (near the lines that build `fhCandidateLong` / `fhCandidateShort`):

```pine
fhCandidateLong = canGoLong and permLongOK and fhRawLong and longBarOK and not fhDojiBlock and not fhTier4Block and fhAllowSidewaysLong
fhCandidateShort = canGoShort and permShortOK and fhRawShort and shortBarOK and not fhDojiBlock and not fhTier4Block and fhAllowSidewaysShort
```

**Replace with**:

```pine
// Permission chain is a WR enhancer, but on 3m it can starve entries.
// Keep it strict for “normal” setups, but allow the strongest/earliest setups to bypass.
fhPermBypassLong = fhStrongLong2 or runTriggerLong or earlyTrendLong
fhPermBypassShort = fhStrongShort2 or runTriggerShort or earlyTrendShort

fhCandidateLong = canGoLong and (permLongOK or fhPermBypassLong) and fhRawLong and longBarOK and not fhDojiBlock and not fhTier4Block and fhAllowSidewaysLong
fhCandidateShort = canGoShort and (permShortOK or fhPermBypassShort) and fhRawShort and shortBarOK and not fhDojiBlock and not fhTier4Block and fhAllowSidewaysShort
```

This preserves your permission chain for most entries, but prevents 3m from going “dead” when momentum/ignition/run triggers happen before 5m structure flips.

---

### Change 2 — Don’t hard-block Harmony entries with MTF STRICT

**Find** this block (MTF STRICT application):

```pine
mtfStrictNeed =
     enableMTFStrictFilter and mtfStrictApplies and
     (shouldEnterLong or shouldEnterShort) and
     not (str.startswith(selectedPriority, "P-1") or str.startswith(selectedPriority, "P0") or str.startswith(selectedPriority, "P1") or str.startswith(selectedPriority, "P2"))
```

**Replace with**:

```pine
// In Filter Harmony mode, MTF STRICT should be “soft” (scored), not a hard blocker,
// otherwise MNQ/MES 3m can go to zero trades.
mtfStrictNeed =
     (not enableFilterHarmony) and
     enableMTFStrictFilter and mtfStrictApplies and
     (shouldEnterLong or shouldEnterShort) and
     not (str.startswith(selectedPriority, "P-1") or str.startswith(selectedPriority, "P0") or str.startswith(selectedPriority, "P1") or str.startswith(selectedPriority, "P2"))
```

---

### Notes

- These are intentionally **minimal** changes: they don’t alter your core signal generation, stops, ladders, or safety exits.
- If you still see “no trades”, the next most common cause is the **Doji/CandleQuality** gate being too strict for your broker’s 3m feed (but the two changes above are the usual “dead bot” culprits for MNQ/MES 3m).

