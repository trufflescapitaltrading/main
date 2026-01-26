# Trading Bot Fix Analysis - MES 3m / MNQ 3m Not Firing Trades

## Root Cause Analysis

After analyzing the 2000+ line Pine Script, I identified **7 critical issues** blocking trades on MES 3m and MNQ 3m charts:

### Issue 1: Filter Harmony Minimum Quality Too High
- **Location**: Line ~177 `fhMinQuality = input.float(70.0, ...)`
- **Problem**: 70% quality threshold is too strict for 3m scalping
- **Fix**: Lower to 55% for 3m charts

### Issue 2: Candle Quality Gate Too Strict
- **Location**: Lines ~440-460 `minBodyRatioEntry_eff` and `minBodyAtrEntry_eff`
- **Problem**: Even "auto-tuned" values (0.28-0.30 body ratio) block many valid trend candles
- **Fix**: Lower to 0.20-0.24 for 3m charts

### Issue 3: HTF Permission Chain Blocking
- **Location**: Lines ~700-730 permission chain logic
- **Problem**: 3m requires 5m permission which often doesn't align during trend starts
- **Fix**: Allow bypass when strong signals exist (P-1, P0, P1, P2)

### Issue 4: MTF Strict Filter Too Aggressive
- **Location**: Lines ~810-825 `mtfStrictApplies`
- **Problem**: Requires BOTH 15m AND 60m SMA50 alignment
- **Fix**: Require only ONE of them, or allow bypass for high-priority signals

### Issue 5: Generic Candle Confirm Thresholds
- **Location**: Lines ~570-590 `genConfirmBodyRatio_eff`
- **Problem**: 0.28-0.30 body ratio still blocks normal trend candles
- **Fix**: Lower to 0.18-0.22 for 3m

### Issue 6: Doji/Hard Block Too Aggressive
- **Location**: Lines ~395-410 `hardDojiMaxBodyPct` and doji detection
- **Problem**: 0.20 body/range blocks many valid small-body trend candles
- **Fix**: Lower to 0.12-0.15 for 3m charts

### Issue 7: Run Trigger Thresholds
- **Location**: Lines ~500-530 run trigger settings
- **Problem**: Displacement tick requirements may be too high
- **Fix**: Lower minimum ticks for 3m charts

## Recommended Parameter Changes

```pine
// Filter Harmony - lower threshold for 3m
fhMinQuality = 55.0  // was 70.0

// Candle Quality - relaxed for 3m
minBodyRatioEntry_eff for MES_3m = 0.22  // was 0.30
minBodyRatioEntry_eff for MNQ_3m = 0.20  // was 0.28

// Generic confirm - relaxed
genConfirmBodyRatio_eff for MES_3m = 0.20  // was 0.30
genConfirmBodyRatio_eff for MNQ_3m = 0.18  // was 0.28

// Doji detection - less aggressive
hardDojiMaxBodyPct = 0.12  // was 0.20

// Permission chain - allow P-1/P0/P1/P2 bypass
// MTF Strict - require only 1 of 2 timeframes
```
