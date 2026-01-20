# MNQ/MES Trading Bot V72 - Trade Firing Fixes

## Overview

This repository contains the V72 fixed version of the MNQ/MES 3m/5m trend scalp trading bot for micro futures. The V72 update addresses critical trade firing issues that were causing:

- Late entries (4th-5th candle instead of 1st-2nd)
- Wrong candle color signals (longs on red, shorts on green)
- Missing multi-candle runs (3-7 consecutive candles)
- Signals firing on doji/indecision candles
- Missed momentum moves

## Files

- `MNQ_MES_V72_TRADE_FIRING_FIXED.pine` - The main fixed PineScript strategy
- `V72_TRADE_FIRING_FIXES_DOCUMENTATION.md` - Detailed documentation of all fixes

## Key Fixes in V72

### 1. Early Entry System (P0:FIRST)
- Enters on the FIRST strong directional candle instead of waiting for 3-4 candles
- Requires: Strong body ratio (50%+), volume confirmation, trend alignment

### 2. Strict Direction Validation
- **CRITICAL FIX:** Longs ONLY on green candles, Shorts ONLY on red candles
- Hard gate enforcement - cannot be bypassed by any override

### 3. Enhanced Doji Protection
- Three detection methods (ratio, ATR, range)
- Blocks ALL signals on doji, small body, and spinning top candles

### 4. Momentum Pre-Signal Detection
- Detects momentum building BEFORE price confirms
- Uses RSI shift, price acceleration, MACD confirmation

### 5. Reduced Consecutive Requirements
- P1 entry: 1 consecutive candle (was 3)
- P2 entry: 2 consecutive candles (was 3-4)

## Signal Priority System

| Priority | Signal Type | When It Fires |
|----------|------------|---------------|
| P0:FIRST | First Candle | 1st strong directional candle |
| P0:MOMENTUM | Pre-Signal | Before trend confirms |
| P1:IMPULSE | Impulse Move | Large single-candle move |
| P1:EARLY_TREND | Early Trend | 1st-2nd candle of run |
| P2:TREND | Continuation | 2nd-3rd candle of run |
| P2:STRONG_TREND | Strong Trend | Established trend |
| P3:SWING | Swing Signal | Swing reversal |

## Installation

1. Open TradingView
2. Create a new Pine Script strategy
3. Paste the contents of `MNQ_MES_V72_TRADE_FIRING_FIXED.pine`
4. Save and add to chart
5. Configure alerts for TradersPost integration

## Configuration

See `V72_TRADE_FIRING_FIXES_DOCUMENTATION.md` for detailed configuration recommendations for each instrument/timeframe combination.

## Visual Debugging

- Green triangles = Long entry signals
- Red triangles = Short entry signals
- X marks = Blocked signals (wrong candle color)
- Performance table shows: Win rate, trades, P&L, signal type, consecutive counts, RSI, MACD, candle color, body ratio, block reason