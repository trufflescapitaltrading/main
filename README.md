# main

This repo contains the current TradingView Pine v5 strategy source at:

- `mnq_mes_v71_cursor_strategy.pine`

Key restores in this version:

- MNQ 3m SL/TP selection is controlled by `mnq_useCustom3m` (no longer ignored).
- V71 “Strict Entry Filter” is used as an actual entry gate (with strong-signal bypass).
- In High Win Rate Mode, MNQ 3m/5m single-contract exits target TP1 (restoring the high-WR behavior).