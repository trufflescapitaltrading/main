# Trade Loss Analysis - MES 3m Strategy

## Trade Details
| Field | Value |
|-------|-------|
| Symbol | MESH6 (MES Micro E-mini S&P 500) |
| Quantity | 1 contract |
| Entry Price | 7006.25 |
| Entry Time | 01/15/2026 09:25:12 |
| Exit Price | 7003.25 |
| Exit Time | 01/15/2026 09:25:29 |
| Duration | 17 seconds |
| Loss | $15.00 (3 points × $5/point) |

## Analysis

### 1. CRITICAL BUG: Duplicated Strategy Code
**The most significant issue is that your Pine Script code is DUPLICATED.** The entire strategy appears twice in your script (two `//@version=5` declarations with identical code). This can cause unpredictable behavior in TradingView including:
- Conflicting signal calculations
- Multiple exit orders firing simultaneously
- Unexpected position closures

### 2. Expected Stop Loss vs Actual Exit
According to your MES settings:
- **Configured Stop Loss**: 14 points (`mes_customSL = 14.0`)
- **Expected Stop Price**: 7006.25 - 14 = **6992.25**
- **Actual Exit Price**: 7003.25 (only 3 points below entry)

The trade exited at 7003.25, which is **11 points ABOVE** where your stop loss should have been triggered. This strongly suggests an unintended exit mechanism fired.

### 3. MES 3m Win-Rate Booster Analysis
Your MES 3m Booster is enabled with these settings:
- `enableMes3mWinRateBooster = true`
- `mes3mBoosterTargetPctOfTP1 = 0.60` (Target = 18 × 0.6 = 10.8 points)
- `mes3mBoosterBETriggerPctOfTarget = 0.60` (BE trigger = 10.8 × 0.6 = 6.48 points)

For single-contract trades, the strategy uses:
- **Target**: ~11 points profit (43 ticks)
- **Stop**: Should remain at entry - 14 = 6992.25 until profit exceeds 6.48 points

### 4. Possible Exit Causes

#### Most Likely: Code Duplication Bug
The duplicated strategy definition is creating conflicts. Two strategy instances may be:
- Both placing orders simultaneously
- Overriding each other's stops
- Causing immediate exits on entry

#### Other Potential Factors:
- **High Volatility at 9:25 AM**: Near market open, rapid price movements with `calc_on_every_tick=true` could trigger unexpected behavior
- **Priority System Conflict**: If a P2:TREND or P1:IMPULSE signal immediately reversed direction, it might conflict with the open position

## Recommended Fixes

### Fix #1: Remove Duplicate Code (CRITICAL)
Your script contains the ENTIRE strategy TWICE. Remove the second instance starting from the second `//@version=5` declaration.

### Fix #2: Verify Stop Loss Calculation
After fixing duplication, verify stops are being set correctly:
```pine
// For MES, stop should be:
localStopLoss = localEntryPrice - currentSL  // 7006.25 - 14 = 6992.25
```

### Fix #3: Add Debug Labels (Optional)
To diagnose future issues, add visual labels showing actual stop levels:
```pine
if strategy.position_size > 0 and strategy.position_size[1] == 0
    label.new(bar_index, low - 5, "SL: " + str.tostring(localStopLoss), color=color.red)
```

### Fix #4: Consider Disabling calc_on_every_tick
For 3-minute charts, `calc_on_every_tick=true` may cause excessive order modifications:
```pine
// Change to:
calc_on_every_tick=false
```

## Summary
The trade lost $15 in 17 seconds because your stop loss at 6992.25 was never properly enforced - the trade exited at 7003.25 instead. The root cause is almost certainly the **duplicated strategy code** which creates undefined behavior in Pine Script. Remove the duplicate code and retest.
