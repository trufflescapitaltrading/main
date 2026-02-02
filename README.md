# V7.1 Master Logic — Deploy-Ready Alerts (TradersPost/Tradovate/TopstepX)

This repo contains a TradingView Pine v5 strategy focused on restoring your **V7.1 profit logic** while making live deployment safer via **alert()-only automation**.

## Files

- `mgc_master_v71_profit_logic_fixed.pine`: **Primary** — restored V7.1 profitable logic with execution fixes (stable entry IDs, exits tied via `from_entry`, contract qty consistency).
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