# MGC Master Logic V7.1 - PineScript Strategy

A comprehensive trading strategy for Micro Gold (MGC) futures, converted from Python/LumiBot to TradingView PineScript.

## Overview

This strategy implements a multi-indicator approach with a quality scoring system to identify high-probability trade setups in the gold futures market. It includes both long and short trading capabilities with sophisticated risk management.

## Features

### Indicators
- **Hull Moving Average (HMA)**: Three HMA lines (Main: 55, Fast: 21, Signal: 13) for trend identification
- **SuperTrend**: Dynamic support/resistance with multiplier 3.0 and length 10
- **RSI**: 14-period RSI with overbought (60) and oversold (40) levels
- **ADX**: 14-period ADX with threshold of 25 for trend strength filtering
- **ATR**: 14-period ATR for volatility-based stops and position sizing
- **Envelopes**: 0.2% price envelopes for harmony confirmation

### Quality Scoring System (5-Star System)
Each trade is evaluated on 5 criteria:
1. **Trend Alignment**: HMA Fast > Signal (for longs) or Fast < Signal (for shorts)
2. **Price Position**: Price above/below Main HMA
3. **SuperTrend Direction**: Bullish or bearish confirmation
4. **RSI Bias**: Above/below 50 level
5. **Envelope Harmony**: Price within appropriate envelope bounds

**Signal Types:**
- **Ultra Long/Short**: Quality score ≥ 90%, 4+ stars, with RSI extremes
- **Strong Long/Short**: Quality score ≥ 80%, 4+ stars

### Risk Management
- **Stop Loss**: ATR-based (2.5x ATR from entry)
- **Take Profit Ladder**: 4 levels at 0.5R, 1.0R, 1.5R, 2.0R
- **Position Splits**: 40%, 30%, 20%, 10% at each TP level
- **Breakeven Stop**: Moves to BE + 0.1R buffer after TP2
- **Trailing Stop**: SuperTrend-based, activates after 0.5R profit
- **Max Hold Time**: 32 bars (8 hours on 15-minute timeframe)
- **Consecutive Loss Limit**: 3 losses stops new entries
- **Session Filter**: Trading only 06:00-21:00 UTC

### Position Sizing
- **Manual Mode**: Fixed contract size (default: 12 contracts)
- **ATR Mode**: Risk 1% of equity per trade using ATR-based calculation

## Installation

1. Open TradingView
2. Go to Pine Editor (bottom panel)
3. Create new indicator/strategy
4. Paste the code from `MGCMasterLogic_v7_1.pine`
5. Click "Add to Chart"
6. Configure settings as needed

## Settings Guide

### Position Sizing
| Parameter | Default | Description |
|-----------|---------|-------------|
| Manual Contracts | 12 | Fixed position size |
| Use ATR-Based Sizing | false | Enable dynamic sizing |
| ATR Risk % | 1.0% | Equity risk per trade |

### Quality Gate
| Parameter | Default | Description |
|-----------|---------|-------------|
| Quality Threshold | 80% | Minimum score for entry |
| ADX Threshold | 25 | Minimum trend strength |

### Take Profit Levels
| Level | R Multiple | Position % |
|-------|------------|------------|
| TP1 | 0.5R | 40% |
| TP2 | 1.0R | 30% |
| TP3 | 1.5R | 20% |
| TP4 | 2.0R | 10% |

### Session Filter
| Parameter | Default | Description |
|-----------|---------|-------------|
| Session Start | 06:00 UTC | Trading window open |
| Session End | 21:00 UTC | Trading window close |

## Visual Elements

- **HMA Lines**: Blue (Main), Green (Fast), Orange (Signal)
- **SuperTrend**: Green (bullish) / Red (bearish)
- **Entry Signals**: Triangle markers below/above bars
- **TP Levels**: Horizontal lines when in position
- **Stop Loss**: Red line showing current stop level
- **Info Table**: Real-time display of key metrics

## Alerts

The strategy includes alerts for:
- Long/Short entry signals
- Ultra quality signals (highest probability)
- Strong quality signals
- Session start/end
- TP level hits
- Stop loss triggers
- EOD exits

## Recommended Timeframe

- **Primary**: 15-minute charts
- The strategy is optimized for intraday futures trading

## Notes

- Designed for Micro Gold (MGC) futures
- Aligned with TopstepX trading rules ($50,000 starting capital)
- Daily loss limit: $1,000 (display/alert only in PineScript)
- Daily profit target: $1,000 (display/alert only in PineScript)

## Conversion Notes

This PineScript version was converted from a Python/LumiBot strategy. Some features have been adapted for PineScript's capabilities:

- Daily PnL tracking is simplified (PineScript limitations)
- Position state management uses persistent variables
- Exit management is handled through strategy functions
- The quality scoring system is fully implemented
- All indicator calculations match the original Python logic

## License

This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0.
