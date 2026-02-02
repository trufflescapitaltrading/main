# Risk/Reward + Trade Filters (Trend/Impulse Only)

This repo contains a TradingView Pine v5 strategy focused on:

- **Wins > losses (positive expectancy)**: targets are enforced to be larger than the stop (RR enforced).
- **No choppy trades**: a strict **ADX + ATR-regime** gate blocks entries in chop/chaos.
- **Only 3 allowed trade types**: **Trend**, **Continuation**, **Impulse (spike)**.

## Files

- `trend_impulse_only_v1.pine`: Strategy implementation.

## How to use

1. Open TradingView → Pine Editor.
2. Paste the contents of `trend_impulse_only_v1.pine`.
3. Add to chart, then tune inputs:
   - **No Chop Filters**: `ADX Threshold`, `ATR Ratio` bounds.
   - **Risk:Reward**: `Stop ATR Multiple`, `TP1/TP2/TP3 ATR Multiple`.
   - **Allowed Trades**: enable/disable Trend / Continuation / Impulse independently.

## Live alerts

When enabled, alerts emit JSON payloads including:

- `action`: `buy` or `sell`
- `quantity`: contract count used by the strategy
- `stop_loss`, `tp1`, `tp2`, `tp3`
- `trade_type`: `TREND` / `CONTINUATION` / `IMPULSE`
- `adx`, `atr_ratio`, `rr_tp1`

If `Account ID` is provided, the payload includes `"account":"..."`.