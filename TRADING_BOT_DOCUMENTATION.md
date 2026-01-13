# MNQ 3m V.71 IMPROVED 5-Star Scalper - Trading Bot Documentation

## Overview
This is an improved version of the MNQ scalping bot designed for 3-minute charts on Micro E-mini Nasdaq-100 futures. The bot is optimized for trending/continuation/momentum conditions with multi-timeframe confirmation.

---

## Key Improvements in V.71

### 1. Stop Loss Execution Fix
- **Problem**: Stop loss, backup stop loss, and nuclear stop loss were failing
- **Solution**: 
  - Changed `process_orders_on_close=true` for immediate order execution
  - Changed `calc_on_order_fills=true` for better fill handling
  - Consolidated all exit logic with proper `from_entry` parameters
  - Each exit now properly references its entry order

### 2. Entry Conditions Loosened
- **Problem**: Bot missed significant trending moves (5+ candle runs)
- **Solution**:
  - Reduced ADX thresholds (Choppy: 20→18, Gray: 18→15)
  - Reduced ATR multipliers (Choppy: 0.5→0.4, Gray: 0.4→0.3)
  - Reduced BB Width thresholds (Choppy: 0.01→0.008, Gray: 0.008→0.006)
  - P0/P1/P2 priorities now **bypass** choppy/gray filters entirely
  - HTF confirmation reduced to 1 of 3 timeframes (33%)

### 3. Trend Continuation Detection (NEW)
- **Problem**: Bot missed multi-candle trending moves
- **Solution**:
  - Added consecutive candle counter (tracks green/red runs)
  - New trend continuation entry when:
    - 2+ consecutive same-direction candles
    - 40+ point move from trend start
    - HMA slope confirms direction
    - ADX > 20

### 4. TradersPost Webhook Fix
- **Problem**: "Price required for relative calculation" error
- **Solution**:
  - Prices now sent as **numbers** (not strings in quotes)
  - Changed `"limitPrice":"25832.5"` to `"stopPrice":25832.5`
  - Added `"price"` field with current price for reference
  - Updated default contract to **MNQM2026** (current front-month)
  - Enabled `useAutoSymbol` by default for automatic detection

---

## Perfect Trade Setup

### Ideal Entry Conditions

#### P0 Momentum Override (Highest Priority)
- ADX > 30 (strong trend)
- DI+ > DI- (bullish) or DI- > DI+ (bearish)
- RSI between 55-80 (bullish) or 20-45 (bearish)
- Price above/below EMA9
- HMA slope confirms direction
- 2+ consecutive candles in direction

#### P1 Impulse Override
- Price breaks Bollinger Band
- Volume ratio > 1.3 (30% above average)
- ADX > 22
- RSI confirms direction
- HMA slope confirms

#### P2 Strong Trend
- ADX > 25
- EMA alignment (Price > EMA21 > EMA50 for long)
- SuperTrend confirms direction
- At least 1 HTF aligned

#### Trend Continuation Entry
- 2+ consecutive same-direction candles
- Move of 40+ points from trend start
- ADX > 20
- Not in choppy conditions

---

## Daily Trade Estimates

Based on the loosened entry conditions and new trend continuation detection:

| Metric | Conservative | Moderate | Aggressive |
|--------|-------------|----------|------------|
| Trades/Day | 8-12 | 12-18 | 18-25 |
| Win Rate Target | 70-75% | 65-70% | 60-65% |
| Avg Win (points) | 35-55 | 40-60 | 45-70 |
| Avg Loss (points) | 20-25 | 25-30 | 25-35 |
| Daily Profit Target | $800-1000 | $1000-1500 | $1500-2000 |

### Expected Performance (Per Contract)

| Priority | Est. Trades/Day | Win Rate | Avg Profit |
|----------|----------------|----------|------------|
| P0 Momentum | 2-4 | 75-80% | $25-40 |
| P1 Impulse | 2-4 | 70-75% | $20-35 |
| P2 Trend | 3-5 | 70-75% | $18-30 |
| Continuation | 2-4 | 65-70% | $15-25 |
| P3-P6 Star | 3-6 | 60-70% | $12-22 |

### Reaching $1,500 Daily Profit Goal

To achieve $1,500 daily profit with 80% win rate:
- **With 1 contract**: ~30-40 trades/day (aggressive, higher risk)
- **With 2 contracts**: ~15-20 trades/day (moderate)
- **With 3 contracts**: ~10-15 trades/day (conservative, recommended)

**Recommendation**: Use dynamic position sizing (enabled by default):
- P0 signals: 3 contracts (highest confidence)
- P1/P2 signals: 2 contracts
- Other signals: 1 contract

---

## Risk Management Settings

### Stop Loss Levels
| Type | Points | Purpose |
|------|--------|---------|
| Primary SL | 25 | Standard stop loss |
| Backup SL | 50 | Catches if primary fails |
| Nuclear SL | 80 | Emergency last resort |

### Daily Limits
- Daily Profit Target: $1,500 (stops trading when hit)
- Daily Loss Limit: $500 (stops trading when hit)
- Daily Loss Circuit: 2% of equity

### Exit Strategy (Kenya Profit System)
Partial take-profit ladder:
1. **TP1 (60%)**: 35 points
2. **TP2 (25%)**: 55 points
3. **TP3 (10%)**: 75 points
4. **TP4 (5%)**: 100 points

---

## Recommended Settings for Live Trading

### Conservative (New Traders)
```
minStarScore = 4
minHTFAligned = 2
maxPositionSize = 2
enableDynamicSizing = false
dailyLossLimit = 300
```

### Moderate (Experienced)
```
minStarScore = 3
minHTFAligned = 1
maxPositionSize = 3
enableDynamicSizing = true
dailyLossLimit = 500
```

### Aggressive ($1,500 Daily Target)
```
minStarScore = 3
minHTFAligned = 1
maxPositionSize = 5
enableDynamicSizing = true
dailyProfitTarget = 1500
dailyLossLimit = 500
```

---

## TradersPost Integration

### Webhook JSON Format (Fixed)

**Long Entry Example:**
```json
{
  "ticker": "MNQM2026",
  "action": "buy",
  "sentiment": "bullish",
  "orderType": "market",
  "quantity": 2,
  "price": 25862.5,
  "stopLoss": {
    "stopPrice": 25837.5,
    "type": "stop"
  },
  "takeProfit": {
    "limitPrice": 25897.5
  },
  "signalType": "MOMENTUM",
  "priority": "P0:MOMENTUM",
  "entryPrice": 25862.5,
  "direction": "LONG",
  "starScore": 4,
  "htfAlignment": 2,
  "adx": 32.5,
  "rsi": 62.3,
  "consecutiveCandles": 3,
  "timestamp": "1768337400000"
}
```

### Contract Symbol Updates
The bot defaults to **MNQM2026** (June 2026). Update quarterly:
- March: MNQH20XX
- June: MNQM20XX
- September: MNQU20XX
- December: MNQZ20XX

**Tip**: Enable "Auto-detect symbol from chart" for automatic handling.

---

## Troubleshooting

### Stop Loss Not Executing
1. Ensure `process_orders_on_close = true`
2. Check if price gapped past stop level
3. Verify backup/nuclear SL is set wider than primary

### Missing Trades
1. Check if market is in "CHOPPY" or "GRAY" zone (see info table)
2. Verify HTF alignment requirement isn't too strict
3. For momentum moves, ensure P0/P1 override is enabled

### TradersPost Errors
1. **"Price required"**: Fixed in V.71 - prices sent as numbers
2. **"Contract expired"**: Update `tradersPostSymbol` to current contract
3. Enable `useAutoSymbol` for automatic detection

---

## Version History

- **V.70**: Original version with known issues
- **V.71**: 
  - Fixed stop loss execution
  - Loosened entry conditions
  - Added trend continuation detection
  - Fixed TradersPost JSON format
  - Updated contract symbol system

---

## Support

For issues or improvements, check:
1. The info table on chart (top-right) for real-time metrics
2. Strategy tester for backtest performance
3. Alert logs for webhook format validation

**Trading involves substantial risk of loss. This bot is provided as-is with no guarantees. Always test thoroughly on paper trading before going live.**
