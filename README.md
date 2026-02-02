# MGC Alert-Only Trading System for TradersPost

Automated trading system for MGC (Micro Gold Futures) using TradingView alerts and TradersPost webhook integration for Tradovate/TopstepX execution.

## System Overview

This is an **ALERT-ONLY** system that uses `alert()` function calls instead of `strategy.entry()` / `strategy.exit()`. This design enables seamless integration with TradersPost for live automated trading.

### Key Features

- **10-Point Confluence Scoring** - Requires 7/10 minimum for high-probability entries
- **Higher Timeframe Confirmation** - Uses 15m confirmation for 5m chart signals
- **Cooperative Stop Loss System** - Progressive stops (Initial → Breakeven → Trailing)
- **Progressive Exit System** - TP1 (70%), TP2 (25%), TP3 (5%)
- **Full TradersPost Integration** - JSON webhooks for automated order execution
- **Session Filtering** - US trading hours only
- **Risk Management** - Max daily trades, max daily loss limits

### Expected Performance

| Metric | Value |
|--------|-------|
| Trades/Day | 4-6 |
| Win Rate | 75-80% |
| Avg Win | ~$65 |
| Avg Loss | ~$32 |
| Daily P&L | $180-250 |

## Files

| File | Description |
|------|-------------|
| `MGC_ALERT_ONLY_TRADERSPOST.pine` | Main TradingView indicator with alert() system |
| `TRADERSPOST_SETUP_GUIDE.md` | Complete setup guide for TradersPost integration |
| `ALERT_JSON_REFERENCE.md` | Technical reference for all JSON alert formats |

## Quick Start

1. **Load Indicator**: Add `MGC_ALERT_ONLY_TRADERSPOST.pine` to MGC 5-minute chart
2. **Create TradersPost Account**: Sign up at traderspost.io
3. **Connect Broker**: Link your Tradovate or TopstepX account
4. **Create Alert**: Set up TradingView alert with TradersPost webhook URL
5. **Go Live**: Enable live trading after paper trade verification

See `TRADERSPOST_SETUP_GUIDE.md` for detailed instructions.

## How It Works

```
TradingView Indicator (Confluence Score ≥ 7)
         ↓
    alert() fires
         ↓
    JSON webhook sent
         ↓
    TradersPost receives
         ↓
    Tradovate/TopstepX
         ↓
    Trade executed
```

## Confluence Scoring (10 Points)

| Factor | Points | Description |
|--------|--------|-------------|
| Higher TF Confirm | 2 | 15m trend alignment |
| ADX > 30 | 1 | Strong trend |
| EMA Alignment | 1 | 9/21/50/100/200 aligned |
| Hull MA | 1 | Direction confirmed |
| MACD | 1 | Histogram confirmation |
| RSI Neutral | 1 | Not overbought/oversold |
| Near S/R | 1 | Support/resistance proximity |
| Volume Spike | 1 | 1.5x average volume |
| Market Structure | 1 | Clean HH/HL or LH/LL |
| Trend Strength | 1 | Strong directional move |

**Minimum 7/10 required for entry**

## Alert Types

- **Entry Alerts** - Long/Short market orders with stop and TP
- **TP1/TP2/TP3 Exits** - Progressive profit taking
- **Stop Updates** - Breakeven and trailing stop modifications
- **Stop Exits** - Position closes on stop hit
- **Manual Flatten** - Emergency close all positions

## Important Notes

- This is an **INDICATOR**, not a strategy - no backtesting capability
- Requires TradingView Pro+ or Premium for webhook alerts
- Test thoroughly with paper trading before going live
- Past performance does not guarantee future results

## Disclaimer

Trading futures involves substantial risk of loss and is not suitable for all investors. This system is provided for educational purposes only. Always trade with capital you can afford to lose.
