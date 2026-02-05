# RUN MASTER — Trade Logic & Execution

This repo contains a TradingView Pine strategy focused on **alert-only live automation** for:

- TradingView → TradersPost → Tradovate / TopstepX

## Files

- `pine/RUN_MASTER_V14_1_ALERT_ONLY_LIVE.pine`: Alert-only live execution script (slippage guard + trend/breakout regime filter + optional stop updates).
- `docs/live_deploy_traderspost_tradovate.md`: Deployment checklist and what to verify before going live.

## Quick start

1. Open `pine/RUN_MASTER_V14_1_ALERT_ONLY_LIVE.pine` in TradingView Pine Editor.
2. Add to chart.
3. Create an alert using the script’s `alert()` calls (webhook to TradersPost).
4. In TradersPost, **verify bracket orders are actually placed** (entry + stop + take profit).
