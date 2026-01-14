# mnq-5m-strategy-optimization

This repo contains the TradingView Pine v5 strategy source:

- `mnq_mes_multitf_cursor_v70.pine`

## What changed to target ~83% win rate (MNQ 5m)

- **Single-contract exits**: MNQ 5m in **High Win Rate Mode** targets **TP1** (not TP2).
- **Post-TP1 protection**: once TP1 is tagged, remaining size is protected at **breakeven** (optionally fee/slippage-adjusted) to prevent a later stop from creating a “loser leg” that drags win rate down.
- **On-chart performance table**: now uses full Strategy Tester totals (no daily reset), so it should match the Strategy Tester win rate/trade count.