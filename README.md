# trufflescapitaltrading — MCL A++ Trend-Only Bot (Live-Safe)

This repo contains a deployable Pine Script v6 strategy optimized for **trend/continuation** on **MCL** with strict “trend day only” gating plus an optional **impulse breakout exception** for breakout-from-compression situations.

## Files

- `MCL_Axx_TrendOnly_Continuation_BOT.pine`: Main strategy.

## What was fixed vs the provided snippet

- **Correct TP math (critical)**: TP1/TP2 are now computed from the **entry price** and the **entry-time R** (stop distance), not from the current bar `close` (which would move targets every bar and distort/live-break logic).
- **Live-safe position sizing**: The script no longer forces `qty=1` when the stop distance implies risk > `riskPerTrade`. If risk is too large, `qty` becomes 0 and entries are blocked.
- **Mandatory trend-only “no trade day” checks added**:
  - **HTF structure**: requires **HH+HL** for longs or **LL+LH** for shorts on HTF (default 60m).
  - **VWAP slope**: requires VWAP sloping in the trade direction.
- **Impulse breakout exception** (configurable): If `useTrendDayOnly` blocks trading (trendDay == false), the bot can still take a **single high-quality breakout** if:
  - HTF trend + structure are aligned
  - VWAP acceptance + slope are aligned
  - candle range ≥ ATR×mult and volume ≥ SMA×mult

## Safety checklist (requested)

- **1) All `strategy.exit()` calls present and correct**: **PASS**
  - Long: `L-TP1`, `L-TP2`, `L-TRAIL`
  - Short: `S-TP1`, `S-TP2`, `S-TRAIL`
  - Uses a dynamic stop (BE logic) + fixed TPs derived from entry.
- **2) Alert syntax valid**: **PASS**
  - JSON strings are well-formed and passed via `alert_message`.
- **3) No undefined variables**: **PASS**
  - Script is self-contained.
- **4) Profit calculations use correct R / ATR multiples**: **PASS**
  - TPs are based on **R**, and impulse detection uses **ATR** multipliers.
- **5) Entry conditions logical (no contradictions)**: **PASS (with a note)**
  - Core entries require strict trendDay + regime.
  - Impulse entries are only possible when strict trendDay blocks trading, but still require HTF alignment.
- **6) Position sizing safe**: **PASS**
  - Will not enter if `qty` computed is 0.
- **7) No common Pine errors**: **PASS**
  - No loops, no repainting via lookahead, guards for ATR>0.
- **8) TradersPost compatibility**: **PASS (expected)**
  - Alerts provide stable JSON with account/route/ticker/action/orderType/quantity/score/mode.

## Red flags check

- **Infinite loops**: **None**
- **Divide-by-zero risks**: **Mitigated**
  - ATR checks use `atr > 0`, R uses `max(..., tick)`.
- **Missing safety stops**: **None obvious**
  - Daily loss stop + max consecutive losses.
- **Alert formatting errors**: **None obvious**
- **“Moving target” exits**: **Fixed**

## Deployment readiness

**Ready** for live deployment *from a code correctness/safety perspective*.

Important: “$1500/day” and “80% win rate” are **not guarantees**—they depend on market regime frequency and your threshold settings. This bot is designed to **trade rarely** and only in clean trend/continuation conditions.
