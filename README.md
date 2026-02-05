# Trade logic & execution fixes (RUN bot)

This repo contains a **live-deploy Pine v5 template** that emits **`alert()` webhook JSON only** (designed for TradersPost→Tradovate / TopstepX-style automation) and includes **trend/continuation filters + MTF alignment + slippage-controlled entries + post-breakeven trailing stop updates**.

## What was “wrong” in the original script you posted (high-impact)

These are the issues that most directly explain the behavior you described (huge entry slippage, stops not acting as intended, and “logic fighting itself”):

- **Duplicate entry paths (can double-fire / conflict)**
  - Your script has a dedicated “V8-correct” LONG/SHORT entry block *and later* another “ORIGINAL 70% WIN RATE” `strategy.entry()` block with different IDs.
  - In backtests this can create unexpected pyramiding / re-entries; in live automation it can create **multiple alerts / mismatched bracket logic** if you’re not extremely careful.

- **Stop-loss / take-profit sources disagree (alerts vs exits)**
  - In parts of the code, entry alerts compute SL/TP using `getActiveSL()/getActiveTP()` (fixed/custom distances).
  - Later exits are managed using `futuresStopDistance` (ATR-derived) and multi-tier logic.
  - If your automation platform/broker uses the alert SL/TP but your TradingView strategy “thinks” a different SL/TP is active, you’ll see **immediate stop-outs**, “wrong distance” stops, and broken performance assumptions.

- **Session “ET” logic was not actually ET**
  - `hour` / `minute` without a timezone argument uses the chart/exchange timezone, not guaranteed ET.
  - This can cause the bot to trade inside what you *think* is a no-trade window or outside intended sessions.

- **Risk limit flags exist but were never enforced**
  - `instrumentRiskLimitReached` was always `false` (never set from `currentInstrumentLoss >= currentInstrumentMaxLoss`), so “individual risk limits” do nothing.
  - `dailyPnL` / `maxLossReached` were effectively placeholders (no robust daily realized PnL tracking), so “max daily loss” does not reliably block entries.

- **One “5-star” component is effectively always true**
  - `star_directionalMomentum = fastEMA > slowEMA or fastEMA < slowEMA` is almost always true (except equality), making the scoring less meaningful.

- **Live execution reality check**
  - A 132-point fill gap in 2 seconds is typically not “Pine math” — it’s usually **market orders + volatility/liquidity**, **wrong contract mapping**, or **order type fields not being honored** by your automation layer.

## The included “live deploy” Pine file

See:

- `pine/run_master_live_v14_2_alerts_only.pine`

Key properties:

- **Single alert entry path** (no duplicate entry systems).
- Session filters computed in **ET** via `hour(time, "America/New_York")`.
- **Trend/range avoidance** using ADX, but still allows **breakout** entries if enabled.
- **MTF alignment** gate (15m/60m/240m by default).
- Webhook JSON includes:
  - `order_type`: `market` / `limit` / `stop_limit`
  - `stop_price`, `limit_price` for stop-limit entries
  - `stop_loss`, `take_profit` (absolute prices)
  - `stop_loss_amount`, `take_profit_amount` (dollars, computed from `syminfo.pointvalue`)
  - `max_slippage_ticks` (advisory field)
- **Trailing stop after breakeven** via `alert()` stop-update messages (`action:"move_stop"`).

## Live deploy checklist (TradersPost → Tradovate)

You must verify your automation platform is actually placing brackets:

- **Symbol mapping**
  - Confirm TradersPost symbol `MNQ1!` / `MES1!` etc maps to the exact Tradovate contract you intend.
  - A mapping mismatch can look like “massive slippage” because it’s effectively a different market/price feed.

- **Order type support**
  - If you choose `stop_limit`, confirm TradersPost supports `stop_price` + `limit_price` for Tradovate.
  - If not supported, use `limit` (best slippage control, may miss fills) or `market` (best fill rate, worst slippage).

- **Bracket fields**
  - Confirm which fields TradersPost reads for stops:
    - `stop_loss` vs `stop_loss_amount`
    - `take_profit` vs `take_profit_amount`
  - If the platform prioritizes the “amount” fields and interprets them in a different unit, stops can become dangerously tight.

## Measuring “80% win rate / $1500/day” realistically

No code can guarantee fixed daily returns. What you *can* do:

- Turn on **simulation** in the script and run a realistic backtest (commission + slippage).
- Check:
  - `strategy.wintrades / strategy.closedtrades` for win rate
  - `strategy.netprofit` and average daily trades across the test window
- Then validate live in **paper trading** with the exact same webhook and order types.
