# 🏆 MGC Filter Harmony V3 Trading Bot

## Overview

This is an enhanced TradingView Pine Script trading bot implementing the **Filter Harmony System V3** - a revolutionary approach that replaces hard blocking filters with a quality scoring system.

## Key Features

### 🎯 Quality Score System (0-100%)
Instead of YES/NO gates, filters contribute to a quality score:
- **Trend Regime**: 30 points
- **Confluence**: 20 points (7 factors)
- **Signal Line Permission**: 15 points
- **Pattern Quality**: 10 points
- **Star Score**: 15 points
- **MTF Alignment**: 10 points
- **Extreme Trend Bonus**: 10 points

**Minimum threshold: 70%** (configurable 50-90%)

### 🔥 Consecutive Candle Detection
Captures trending moves that were previously missed:
- Detects 3+ consecutive same-direction candles
- Extreme trend detection at 7+ candles
- Impulse override for big candles (1.1× ATR)

### 🚀 Smart Override System
Extremely strong conditions can bypass some filters:
- **Extreme Trend**: 7+ consecutive candles + 2× min price move
- **Impulse Override**: 1.1× ATR candle + 1.8× volume surge
- **Consecutive Trend**: 3+ same-direction candles with 1.5× ATR range

### 📊 Multi-Timeframe Confirmation
- 3 higher timeframes (15m, 60m, 240m)
- **33% alignment threshold** (1 of 3 timeframes)
- Modes: Confirmation, Filter, Advisory

### 💰 Profit Protection Systems
- **MAE Protection**: Exit if profit drops 25% from peak
- **Breakeven Protection**: Move SL to entry at $40 profit
- **3-Tier Profit Locks**: 50%/60%/70% at 2.0/3.5/5.0 ATR
- **Trailing Stop**: 0.6× ATR after profit activation

## Supported Instruments

| Instrument | Multiplier | Commission | Best Sessions |
|------------|------------|------------|---------------|
| MNQ | 1.8× | $0.52 RT | Asian, NY |
| MGC | 1.4× | $1.60 RT | Asian, London |
| MCL | 1.6× | $1.60 RT | London, UAE |
| MES | 1.5× | $0.52 RT | NY |
| MYM | 1.3× | $0.85 RT | NY |
| M2K | 1.4× | $0.65 RT | NY |

## Files

- `MGC_FilterHarmony_V3.pine` - Main trading bot script
- `ANALYSIS_AND_DEPLOYMENT.md` - Detailed analysis and deployment guide

## Quick Start

1. Copy `MGC_FilterHarmony_V3.pine` to TradingView
2. Add to chart (3-minute recommended for MGC)
3. Configure TradersPost webhook
4. Set up alerts for LONG/SHORT signals
5. Start with 1 contract, scale after 5 profitable days

## Performance Targets

| Metric | Target |
|--------|--------|
| Daily Profit | $1,500+ |
| Win Rate | 70-77% |
| Daily Profit % | 1.5% |
| Trades per Day | 15-25 |
| Profit Factor | 1.8-2.5 |

## Safety Checklist ✅

- [x] All strategy.exit() calls present
- [x] Alert syntax valid (TradersPost compatible)
- [x] No undefined variables
- [x] Correct ATR multiples for TP/SL
- [x] Logical entry conditions
- [x] Safe position sizing
- [x] No Pine Script errors
- [x] Matches proven baseline logic

## Deployment Status

**✅ READY FOR LIVE TRADING**

See `ANALYSIS_AND_DEPLOYMENT.md` for detailed deployment instructions and trade estimates.
