# TradersPost “Exit Rejected” (MNQ/MES) Fix Pack

This repo contains a small Pine Script module you can copy into your TradingView strategy to stop **exit-only webhook alerts** from firing when TradersPost has **no open position/orders** (the exact rejection shown in your logs).

## Why you’re seeing the rejection

TradersPost rejects an `{"action":"exit"}` webhook when:

- There is **no open order** to cancel for that symbol, and/or
- There is **no open position** to exit for that symbol.

Common causes:

- **Symbol mismatch**: your alert sends `MNQ1!` (continuous) while your broker position is on `MNQH2026` (contract). TradersPost can’t close what it doesn’t recognize/match.
- **State desync**: TradingView strategy logic (or your own “simulated position” variables) thinks a position exists, but the broker/TradersPost is flat (entry rejected, missed alert, manual close, connection hiccup).

## What’s included

- `pine/traderspost_exit_guard.pine`: a **drop‑in module** that:
  - prevents sending `action:"exit"` when you’re flat (using either strategy position or your simulated TP position state)
  - optionally forces `ticker` to your configured futures contract (ex: `MNQH2026`) instead of `MNQ1!`
- `pine/TRADERSPOST_FULL_FIX_BLOCK.pine`: a **copy/paste router block** you can drop into larger bots to fully fix TradersPost routing (exit guard + forced contract tickers + router state).
- `pine/MJV6_Micro_Futures_Ultra_Strategy_FIXED.pine`: a **complete, compiling strategy** based on your pasted MJV6 snippet, with:
  - repaired entry/exit IDs so strategy tester exits work
  - fixed time/session + pivot compile issues
  - fully fixed TradersPost routing (exit guard + forced contract tickers)

## How to use

1. Open your TradingView strategy in Pine.
2. Copy the contents of `pine/traderspost_exit_guard.pine` into your script.
3. Replace your existing TradersPost `actualTicker` selection (or wrap it) using the helper shown in the module.
4. Wrap every place you call `alert()` with an exit payload behind the guard:
   - **reverse‑signal exits**
   - **EOD exits**
   - any explicit “exit now” logic

## Recommended settings (MNQ/MES)

- **Do not use** `MNQ1!`/`MES1!` for live execution unless your broker mapping is explicitly configured that way.
- Prefer **explicit contracts**:
  - MNQ: `MNQH2026` (example)
  - MES: `MESH2026` (example)
- If you run **alert-only mode**, use the guard’s **simulated position** source.
- If you run **strategy orders + alerts**, use the guard’s **strategy position** source.
