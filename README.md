# Strategy: RUN V14.1 (Pine v5)

This repo includes a TradingView Pine v5 strategy in `strategy.pine`.

## Live deployment (alert-only)
- Set **Alert Only Mode** to `true` to disable strategy orders.
- Configure a TradingView alert to use the script's `alert()` payloads.
- If your broker/connector supports limit orders, enable:
  - **Use Limit Entries** and adjust **Limit Entry Buffer (ticks)**.
- Use **Stop/Trail Slippage Buffer (ticks)** to avoid tight stops after breakeven.

## Regime and MTF gating
- To avoid sideways trading, keep **Avoid Ranging Markets** enabled.
- Allow breakouts during ranges with **Allow Range Breakout Trades**.
- For multi-timeframe confirmation, set:
  - **Enable MTF** and **MTF Mode = Confirmation**.

## Backtesting
Disable Alert Only Mode and backtest on your target instrument/timeframe.
No strategy can guarantee a specific win rate or daily returns. Use your own
data and risk controls before live deployment.