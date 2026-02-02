# MGC 80% WIN RATE SYSTEM (ALERT-ONLY) — TradersPost → Tradovate/TopstepX

This repo contains an **ALERT-ONLY TradingView indicator** designed to send automated signals to **TradersPost**, which then routes orders to **Tradovate / TopstepX**.

## What’s included

- **`MGC_80_PERCENT_WINRATE.pine`**
  - TradingView **indicator** (not a backtesting strategy)
  - Uses **ONLY** `alert()` calls (no backtest/strategy functions)
  - 10-point confluence scoring with HTF confirmation
  - Cooperative stop progression: initial → breakeven → trailing
  - Progressive exit alerts: TP1 / TP2 / TP3 + STOP (optional)

## How the alert system works

1. Indicator calculates confluence score each bar close
2. If score ≥ threshold and filters pass → **entry alert fires**
3. Indicator tracks a **virtual position** internally
4. When TP/STOP levels are hit (based on bar high/low) → **exit alerts fire**
5. TradersPost receives the JSON webhook and places orders in Tradovate/TopstepX

## Critical notes (read this)

- **This is not a backtesting strategy** (it’s an indicator). TradingView will not manage a real broker position for you.
- The indicator’s “position” is **virtual** (based on alerts), so it assumes:
  - entry fill at **bar close**
  - TP/STOP fill at the **target/stop price** if the bar hits it
- If a bar hits TP and STOP in the same candle, the indicator **prioritizes STOP** for safety.

## Quick start (TradingView → TradersPost)

### 1) Add the script to TradingView

1. Open TradingView
2. Open an **MGC** chart (recommended 5m)
3. Pine Editor → paste `MGC_80_PERCENT_WINRATE.pine` → Add to chart
4. Confirm the top-right table shows status (trades/day, confluence, etc.)

### 2) Set up TradersPost

1. Create your TradersPost account
2. Connect your **Tradovate/TopstepX** account
3. Copy your **TradersPost webhook URL**

### 3) Create the TradingView alert (this is the key)

1. Click **Alert** in TradingView
2. **Condition**: select the indicator, then choose **“Any alert() function call”**
3. **Options / Frequency**: **Once Per Bar Close**
4. **Webhook URL**: paste your TradersPost webhook URL
5. **Message**: leave empty (or any placeholder text) — the script sends the JSON from `alert()`
6. Create the alert

Important:
- Do **not** use TradingView “strategy placeholders” in the alert message (the `{{...}}` fields meant for backtesting strategies); this script is an indicator.
- With “Any alert() function call”, the payload is whatever the script passes into `alert()`.

## TradersPost strategy configuration (high level)

Exact configuration depends on your TradersPost account and broker connection, but generally:

- **Symbol mapping**: map `MGC1!` (continuous) to your broker’s MGC contract
- **Quantity**: match the indicator’s `Fixed Contracts` input
- **Order type**: market entries
- **Risk controls**: set broker-side max loss / max positions / max daily trades as appropriate

## Alert payload format (what TradersPost receives)

The indicator sends JSON like:

### Entry (Long)

```json
{"ticker":"MGC1!","action":"buy","orderType":"market","quantity":1,"confluenceScore":8,"stopLoss":{"stopPrice":2515.8},"takeProfit":{"limitPrice":2522.3}}
```

### Entry (Short)

```json
{"ticker":"MGC1!","action":"sell","orderType":"market","quantity":1,"confluenceScore":8,"stopLoss":{"stopPrice":2525.8},"takeProfit":{"limitPrice":2519.3}}
```

### Exit (example TP1 for a long)

```json
{"ticker":"MGC1!","action":"sell","orderType":"market","quantity":0.7,"reduceOnly":true,"reason":"TP1","referencePrice":2522.3}
```

### Exit (example STOP for a long)

```json
{"ticker":"MGC1!","action":"sell","orderType":"market","quantity":1,"reduceOnly":true,"reason":"STOP","referencePrice":2515.8}
```

Notes:
- For long positions, exits use `"action":"sell"`.
- For short positions, exits use `"action":"buy"`.
- The script includes `reduceOnly:true` as a safety hint (ignored if unsupported).

## Recommended TradingView chart settings

- **Timeframe**: 5m (default HTF confirm 15m)
- **Session filter**: enabled (US hours) unless you want overnight trades
- **Confluence threshold**: 7 for the intended “quality over quantity” behavior

## Troubleshooting

- **No alerts firing**
  - Confirm TradingView alert condition is **Any alert() function call**
  - Confirm alert is **enabled** and frequency is **Once per bar close**
  - Confirm `Enable TradersPost Alerts` input is ON
  - Confirm you’re on an MGC ticker (script blocks non-MGC charts)

- **Trades fire but no exits**
  - Ensure `Emit TP/STOP Exit Alerts` is ON
  - Ensure your TradersPost strategy supports partial exits / reduce-only behavior
  - If you only want bracket exits from the entry, enable `Include Stop/TP1 In Entry Alert` and disable exit alerts

- **Symbol mismatch**
  - Change the indicator input `TradersPost Ticker` (default `MGC1!`)
  - Fix symbol mapping inside TradersPost
