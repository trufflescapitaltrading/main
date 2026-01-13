# bot-trade-execution-logic

This repo contains a TradingView Pine strategy intended for **MNQ trend / continuation / momentum** trading with **multi-timeframe confirmation**, and **no sideways trading** except for **true breakouts/impulses**.

## Files

- `MNQ_3m_bot_v71.pine`
  - Live-ready strategy iteration focused on:
    - **Catching continuation runs** (multi green/red candle sequences) via a dedicated continuation/breakout priority.
    - **Avoiding chop/range** unless impulse/breakout/continuation is present.
    - **Fixing “backup/nuclear stop failed”** behavior by using intrabar `high/low` triggers and adding a nuclear-distance stop.
    - **Fixing TradersPost signal format**: sends numeric stop/TP prices and includes `price` for market orders.

## TradersPost notes (important)

- **Do not hardcode expired futures contracts** like `MNQH2025`.
- This strategy defaults to using the **chart symbol** for `ticker` (auto mode).
  - If you want to override, set `Auto-detect symbol from chart = false` and set `TradersPost Symbol Override` to a valid, non-expired contract.
- Signals include:
  - `orderType: "market"`
  - `price` (numeric, optional via input)
  - `entryPrice` (numeric reference)
  - `stopLoss.price` + `takeProfit.price` (numeric)
