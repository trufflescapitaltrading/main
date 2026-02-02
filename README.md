# V7.1 Master Logic — Deploy-Ready Alerts (TradersPost/Tradovate/TopstepX)

This repo contains a TradingView Pine v5 strategy focused on restoring your **V7.1 profit logic** while making live deployment safer via **alert()-only automation**.

## Files

- `mgc_master_v71_profit_logic_fixed.pine`: **Primary** — restored V7.1 profitable logic with execution fixes (stable entry IDs, exits tied via `from_entry`, contract qty consistency).
- `mgc_master_v71_original_profit_logic_2025_11_05.pine`: **Original baseline** — preserves original V7.1 sizing + behavior for matching the historical backtest stats.
- `trend_impulse_only_v1.pine`: Experimental rewrite (not recommended if win-rate collapses).

## How to use

1. Open TradingView → Pine Editor.
2. Paste the contents of `mgc_master_v71_profit_logic_fixed.pine`.
3. Add to chart, then tune inputs:
   - **Strict Quality Mode (Entry Only)**: ADX no-chop gate, time blocks, quality score, frequency limiter (does not change exits).
   - **Deploy Ready Alerts**: trailing activation/updates, emergency close alerts, optional no-trade diagnostics.

## Live alerts

When enabled, alerts emit JSON payloads including:

- `action`: `buy` or `sell`
- `quantity`: contract count used by the strategy
- **Entry bracket fields**: `stop_loss`, `take_profit_1..4`
- **Stop modification**: `action:"modify_stop"`, `stop_type:"protection"|"trailing"`, `new_stop_price`
- **Emergency flatten**: `action:"emergency_exit"` with `reason`
- Optional: `action:"diagnostic"` when a signal is blocked

If `Account ID` is provided, the payload includes `"account":"..."`.

## Perfect Trade Setup (Checklist)

Only allow trades when **most** of these are true:

- **Regime**
  - `volatilityOK == true`
  - Market is **not ranging** (avoid `rangingMarket == true`)
  - Best when **SuperTrend direction is stable** and **Hull slopes agree**
- **Direction alignment**
  - **Long**: `trend == 1`, `slopeMain == 1`, `hullAnyBullish == true`, price above/near `smaBasis`
  - **Short**: `trend == -1`, `slopeMain == -1`, `hullAnyBearish == true`, price below/near `smaBasis`
- **Entry type**
  - **Continuation**: pullback to envelope/basis in-trend, then resumption (highest win-rate subtype)
  - **Impulse**: breakout/touch + strong slope/trend confirmation (best in regular session)
- **Avoid**
  - First/last ~15 minutes of RTH (unless explicitly designed for it)
  - ATR ratio too low/high (dead chop or chaos)

If you want **70–80% win-rate behavior**, filter harder:

- **Continuation only** (or continuation + best impulse)
- Cap trades per session/day

## Live deployment best practice (alert() only)

- **Entry alert places bracket at broker**: entry alert JSON includes `stop_loss` + `take_profit_1..4`
- **Optional stop upgrades**: `alert()` events with `action:"modify_stop"` for profit protection / trailing updates
- **Emergency flatten**: `alert()` with `action:"emergency_exit"` on max daily loss / gap loss
- Avoid relying on `strategy.exit()` to execute live; use it for backtest while broker manages brackets from alerts

## Institutional risk add-ons (what’s enforced)

`mgc_master_v71_profit_logic_fixed.pine` adds **entry gates + alert-only exits** (does not alter the original profit logic):

- **HTF/MTF alignment gate** via `request.security()` EMA trend direction
- **HTF/MTF flip emergency exits** (alert flatten)
- **MAE/MFE tracking** and optional **MAE emergency exit** (alert flatten)
- **Consecutive loss kill-switch** (halts new entries; optional alert)
- **Intraday peak-to-valley drawdown kill-switch** (halts + alert flatten)
- **Time stop / losing timeout exits** (alert flatten)
- **Volatility shock guard + cooldown** (blocks entries; optional shock flatten)
- **Idempotency fields** in alerts: `signal_id`, plus `intent` / `position_intent`