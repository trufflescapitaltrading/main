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

## Perfect trade setup (live checklist)

Use this as the ideal entry environment for the bot:

- **HTF trend aligned** (HTF bullish for longs / HTF bearish for shorts)
- **ADX above threshold** (strong-trend regime, not chop)
- **EMA stack aligned + Hull direction aligned**
- **Directional dominance**: the chosen direction’s confluence score beats the opposite direction by at least the dominance margin
- **Not into opposing S/R**: longs not near resistance; shorts not near support
- **Stop makes sense**: structure/ATR stop distance falls inside the min/max ATR guardrails (not too tight, not too wide)

## Institutional risk management (what’s built in)

The indicator includes “institutional-style” safety controls to avoid low-quality regimes and protect the account:

- **HTF alignment requirement** (optional but recommended): longs only when HTF is bullish; shorts only when HTF is bearish
- **MTF confirmation** (optional): adds a second, slower timeframe trend gate (e.g., 60m)
- **Reversal protection exit** (optional): exits remaining position at market if a strong opposite regime appears (dominant opposite score + confirmation)
- **Losing-streak kill-switch**: disables new entries after N consecutive losing trades (resets next day/session)
- **Cooldown after loss/win**: forces a pause after a trade closes to avoid “revenge trading”
- **Time-stop** (optional): exits at market after a max number of bars in a trade (prevents overstaying)
- **MAE/MFE tracking** (virtual): tracks max adverse excursion and max favorable excursion during each trade for monitoring/optimization

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

## Daily trade estimates (realistic ranges)

With the current **quality-first** filters (HTF + ADX + dominance + S/R + stop sanity):

- **Trades/day**: ~1–4 typical (can be 0 on choppy days; can be higher on strong trend days)
- **Win rate**: commonly trends toward **65–85%** depending on thresholds (not guaranteed)
- **PnL/day**: highly variable; depends mostly on contracts, volatility, and slippage. Expect uneven distribution (many small days, occasional larger days)

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

## Live Deployment Mode (choose one)

You can run this indicator in one of two practical “live” modes depending on your broker/TradersPost scaling support:

### Mode A — Bracket only (ENTRY + STOP/TP1 only)

Best when partial exits are not reliable, or you want the simplest live behavior.

- **Indicator settings**:
  - `Include Stop + TP1 on Entry Alert` = **ON**
  - `Emit TP/STOP Exit Alerts` = **OFF**
- Result:
  - Entry alert includes **stopLoss + TP1 takeProfit**
  - No TP2/TP3 scale-out alerts will be sent

### Mode B — Scale-out exits (ENTRY + TP1/TP2/TP3 + STOP)

Best when your TradersPost strategy supports scaling out (reduce-only orders).

- **Indicator settings**:
  - `Include Stop + TP1 on Entry Alert` = **ON** (recommended)
  - `Emit TP/STOP Exit Alerts` = **ON**
- Result:
  - Entry alert includes **stopLoss + TP1 takeProfit**
  - The indicator also sends **TP2/TP3** reduce-only exit alerts and a **STOP** exit alert for any remaining size

## Recommended TradingView chart settings

- **Timeframe**: 5m (default HTF confirm 15m)
- **Session filter**: enabled (US hours) unless you want overnight trades
- **Confluence threshold**: 7 for the intended “quality over quantity” behavior
- **Institutional settings (recommended)**:
  - `Require HTF Alignment` = ON
  - `Use MTF Confirmation` = OFF initially (turn ON after you validate signal frequency)
  - `Exit On Reversal Signal` = ON
  - `Max Consecutive Losing Trades` = 2
  - `Cooldown Bars After Loss` = 30
  - `Max Hold Bars` = 0 (off) initially; turn on only if you see overstaying in chop

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
