# Trading Strategy Patch Kit

This repo contains a **drop-in patch** to fix the most common causes of:
- **late entries** (P1/P2 showing up 1 candle late)
- **entries “on the wrong candle color”** (looks like it fired on a red candle for longs / green candle for shorts)
- **missed 3–6 candle runs** (because the first usable trend-start signal came too late)

## Files

- `pine/TRADE_FIRING_FIX_PATCH.pine`: Patch sections to paste into your script.

## What this fixes (the big one)

In your script you currently have:
- `enterOnBarClose = true` (you want bar-close entries)
- but also `process_orders_on_close = false` in `strategy()`

That combo makes TradingView **fill your market order on the NEXT bar open**, so the entry will:
- look **late**
- often print on an **opposite-color candle**
- miss the first chunk of multi-candle runs

The patch explicitly tells you to change `process_orders_on_close` to `true`.
