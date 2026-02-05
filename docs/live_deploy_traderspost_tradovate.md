# RUN MASTER — Live Deploy Notes (TradingView → TradersPost → Tradovate/TopstepX)

This repo contains `pine/RUN_MASTER_V14_1_ALERT_ONLY_LIVE.pine`, an **alert-only** Pine strategy script intended for automated execution via webhook.

## What was “wrong” in your original script (high-impact items)

- **Stop-loss not actually being placed at the broker (most critical)**  
  Your TradingView alert JSON can be perfect and you can still get blown out if **TradersPost → Tradovate** isn’t mapping the SL/TP fields into a real bracket/OTO order. The symptom you showed (stops ignored / exits far past SL) is almost always:
  - wrong JSON key names, or
  - connector expects *offsets* but receives *absolute prices*, or
  - stop type mismatch (STOP vs STOP LIMIT), or
  - rejected bracket legs (min tick/price format), silently falling back to “naked” market position.

- **Catastrophic entry slippage**  
  A market order during a volatility spike can fill far away from the “signal price.” If your automation then places SL/TP from the wrong reference (signal close vs fill), you can end up **filled inside your intended risk zone**.

- **Range/trend logic not fully aligned**  
  You stated: “don’t trade sideways except impulse/breakout.” Many multi-filter stacks accidentally allow “meh” signals in chop because each filter is permissive on its own.

- **Common Pine wiring issues that reduce quality**
  - Using exchange timezone (`hour`, `minute`) while labeling sessions as “ET.”
  - “Gate” booleans that are effectively always true (example: a momentum check that is true in almost every bar).
  - Risk-limit flags calculated but never enforced.
  - Multiple entry blocks that can double-fire alerts or create inconsistent “state.”

## What the included live script does

### 1) Slippage-guarded entries (marketable LIMIT)

If `useMarketableLimitEntries=true`, entry alerts include:

- `order_type: "limit"`
- `limit_price`:  
  - Long: `close + (maxEntrySlippageTicks * mintick)`  
  - Short: `close - (maxEntrySlippageTicks * mintick)`

This caps the *worst* allowable fill price. You will sometimes miss trades; that’s the tradeoff for preventing the “+132 points worse” fills you observed.

### 2) Stops and targets sent as BOTH absolute price AND $ amount

The script emits:

- Absolute prices: `stop_loss`, `take_profit`  
- Redundant keys (optional): `stopLoss`, `takeProfit`, `stopPrice`, `takeProfitPrice`
- Dollar amounts (optional): `stop_loss_amount`, `take_profit_amount` (+ camelCase variants)

**Why amounts help:** if your connector supports `$` offsets, it can place stops relative to the *actual fill* (good when fills differ from signal).

### 3) Trend vs range enforcement (range only on impulse/breakout)

Continuation trades require:

- ADX ≥ `minADXForTrendTrades`
- EMA alignment + Hull slope alignment
- Strong volume + RSI sanity

If the market is ranging (low ADX), trades are blocked **unless** there is a true breakout/impulse (breaks prior high/low or envelope breakout with strong volume).

### 4) Breakeven → trailing stop update alerts

After breakeven is reached (profit ≥ ATR × `breakevenAfterATR`), the script can emit throttled:

- `{"action":"update_stop","new_stop":...}`

This requires your automation platform to support stop modification. If it doesn’t, keep this off and manage trailing on the broker side.

## TradersPost / Tradovate verification checklist (do this before live)

- **Confirm bracket placement in logs**  
  In TradersPost order logs, verify that every entry results in:
  - an entry order, AND
  - an attached stop order, AND
  - an attached take-profit order

- **Confirm key mapping**  
  Verify which keys TradersPost expects for brackets. Common patterns:
  - absolute price fields (`stopPrice`, `takeProfitPrice`) OR
  - offset fields (`stopLossAmount`, `takeProfitAmount`) OR
  - ticks (`stopLossTicks`, `takeProfitTicks`)

  If you discover the canonical keys, update the Pine JSON builder to match exactly.

- **Use LIMIT or STOP-LIMIT where possible**  
  If Tradovate supports it via connector, prefer order types that cap slippage.

- **Tick size formatting**  
  Ensure price values are formatted to the instrument’s tick size. The script uses `format.mintick` for this.

## “Perfect trade setup” (aligned to your stated intent)

The highest quality trades for this bot are typically:

- **Market regime**: ADX trending (≥ your threshold) OR an obvious breakout impulse with strong volume.
- **Continuation structure**: EMA bull/bear alignment + Hull slopes aligned + price on the right side of the basis.
- **Volume**: above a rising volume average (strong participation).
- **MTF** (if enabled): higher timeframe trend aligns with the direction (Filter mode).

Avoid:

- low ADX chop with alternating slopes,
- thin/liquidity-gap periods (often the cause of “teleport fills”),
- “session” mismatches due to timezone misconfiguration.

## Win-rate / daily PnL estimates

I can’t produce a credible win-rate or “$1500/day” estimate from code alone—those depend on:

- instrument,
- timeframe,
- slippage model,
- commission,
- session windows,
- and whether your broker actually attaches stops/targets.

**How to estimate correctly:**

1. Run TradingView Strategy Tester on your target instrument/timeframe with realistic commission/slippage.
2. Compare “signal price” vs real fills from Tradovate (paper) for at least 50–200 trades.
3. Measure:
   - average adverse excursion,
   - fill slippage distribution,
   - % of trades where brackets failed (should be 0%).

Only after that should you choose daily trade caps and size targets.

