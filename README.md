# RUN MASTER (Alert-Only) – Live Deployment Scaffold

This repo contains a **TradingView Pine v5 alert-only** script designed for **TradersPost → Tradovate/TopstepX** automation.

## Files

- `RUN_MASTER_ALERT_ONLY_v14_2.pine`
  - **No `strategy.*` orders.** Uses `alert()` system calls only.
  - Adds **slippage protection**, **MTF trend confirmation**, **sideways-market avoidance**, and **breakeven → trailing stop** logic.
  - Sends **multiple stop/TP field variants** (`stop_loss`, `stopLoss`, `stop_loss_amount`, `stopLossAmount`, etc.) to reduce webhook-schema mismatch risk.

## Why your current live fills/stops are failing (root causes)

Based on the execution notes you pasted, these are the practical issues that break live trading even if the “signal logic” is good:

- **Absolute-price stops + market entries = doomed trades under slippage**
  - Your alerts build `stop_loss` and `take_profit` from the **signal bar price** (typically `close`).
  - If TradersPost sends a **market** order and the fill is far away (your MNQ example: +132.25 points), the “stop price” computed from the signal can become **nonsensical relative to fill**, or effectively inside the wrong zone.
  - Fix: use **LIMIT entries** (or strict gap/range filters) and/or send **dollar-based offsets** so the broker can place stops relative to the fill.

- **Stop-loss orders not being placed (webhook field mismatch)**
  - A very common failure mode is: entry parses fine, but bracket fields don’t match what the bridge expects.
  - Fix: send both **price-based** and **amount-based** fields, and include **camelCase + snake_case** variants.

- **Sideways market participation**
  - Your own requirement says “don’t trade consolidation/range except impulse/breakout.”
  - Fix: explicit **regime gate** that blocks ranging *unless* an impulse/breakout condition is present.

## What this script changes (live-ready improvements)

- **Slippage Guard**
  - Default is **LIMIT entries** with a small tick offset (`entryOffsetTicks`).
  - Adds entry filters: **max open gap (ATR)** and **max bar range (ATR)** to avoid “news spike” fills.
  - Adds `slippageTicksForStops` to widen stop placement slightly for real fills.

- **Stops that cooperate with filters**
  - Stops are computed once at entry (ATR or per-instrument override), then:
  - When breakeven triggers, it transitions to **BE + buffer**, then **trailing stop**.
  - Stop update alerts are **throttled** (`stopUpdateStepTicks`) to avoid webhook spam.

- **Ranging-market avoidance**
  - Blocks ranging by default.
  - Allows only **impulse/breakout** signals while ranging (configurable).

- **MTF confirmation**
  - Default mode is **Confirmation** with alignment threshold of **66%**.

## “Perfect setup” checklist (recommended starting point)

This is the configuration that matches your stated intent: **trend/continuation/momentum with MTF confirmation**, avoid sideways, allow only impulse breakouts.

- **Chart**
  - **Timeframes**: start with **1m–3m** for scalps, **5m** for fewer/higher-quality trades.
  - Avoid low-liquidity hours; keep `No Trade Zone` enabled.

- **Core filters**
  - `confluenceLevel`: **12–15**
  - `enableMTF`: **ON**
  - `mtfMode`: **Confirmation**
  - `mtfAlignThreshold`: **66–99**
  - `blockRanging`: **ON**
  - `allowImpulseInRange`: **ON**

- **Execution**
  - `useLimitEntries`: **ON**
  - `entryOffsetTicks`: **1–4** (start with 2)
  - `maxGapAtr`: **0.6–1.0**
  - `maxBarRangeAtr`: **1.0–1.6**

- **Stops**
  - `enableBreakeven`: **ON**
  - `enableTrailAfterBE`: **ON**
  - `slippageTicksForStops`: **1–3**

## Daily trade estimates / win rate / PnL (honest expectations)

I can’t truthfully guarantee “80% wins”, “$1500/day”, or “1.5% daily returns” from code alone—those depend on:

- the market regime,
- the instrument (MNQ vs MES vs MCL),
- liquidity/spread,
- your bridge execution mode,
- and your exact session/timeframe choice.

That said, with **strict filtering + limit entries**, a realistic starting envelope for a trend/continuation scalper is often:

- **Trades/day**: ~**3–12**
- **Win rate**: ~**55–75%** (higher in strong trend days, lower in chop)
- **PnL/day**: extremely variable; the goal should be **process stability** first, not a fixed daily target.

If you want credible estimates, you must:

- run a structured backtest (multiple months),
- then replay (bar replay) through high-volatility events,
- then run paper/live-sim with real bridge logs and verify brackets are placed.

## Deploy steps (TradingView → TradersPost)

1. Paste `RUN_MASTER_ALERT_ONLY_v14_2.pine` into TradingView and add to chart.
2. Create an alert:
   - Condition: **Any alert() function call**
   - Webhook URL: your TradersPost webhook
3. In TradersPost:
   - Confirm it reads either `stop_loss`/`take_profit` or `stopLoss`/`takeProfit`.
   - Prefer brackets based on `stop_loss_amount` / `take_profit_amount` if supported (more slippage-resistant).

## Notes

- This script includes a **bar-based simulation** for BE/trailing and exits to decide when to fire exit/stop-update alerts.
  - Your broker fills can differ; the point is to avoid catastrophic “signal-stop mismatch” and to give TradersPost enough fields to place brackets correctly.
