# 🚀 Trend/Impulse Master Strategy V8.0

## Overview

A redesigned Pine Script trading strategy focused on **WINS > LOSSES** with strict trend/impulse-only filters. No trades in choppy market conditions.

## Key Principles

### 1. Flipped Risk/Reward (Wins > Losses)

| Component | ATR Multiple | Typical $ Value (MGC) |
|-----------|-------------|----------------------|
| Stop Loss | 1.0 ATR | ~$20-30 |
| TP1 (60%) | 2.0 ATR | ~$40-60 |
| TP2 (30%) | 3.0 ATR | ~$60-90 |
| TP3 (10%) | 4.5 ATR | ~$90-135 |

**Blended Average Win:** ~$52.50  
**Average Loss:** ~$25.00  
**Win/Loss Ratio:** 2.1:1

### 2. Only 3 Trade Types Allowed

| Trade Type | Description | Confirmation |
|------------|-------------|--------------|
| **TREND** | Clear directional move | ADX > 25 + Hull/EMA alignment |
| **IMPULSE** | Sharp price spike | 1.5x ATR move + Volume spike |
| **CONTINUATION** | Pullback resumption | Shallow pullback + Bounce in trend |

### 3. NO Choppy Trades

The strategy uses **ADX (Average Directional Index)** to filter market conditions:
- **ADX ≥ 25** = Trending market ✓ (OK to trade)
- **ADX < 25** = Choppy market ✗ (NO trades)

## Profitability Math

### At Different Win Rates:

```
40% Win Rate:
- 10 trades = 4 wins × $52.50 = $210 won
           - 6 losses × $25 = $150 lost
           = +$60 profit ✅

50% Win Rate:
- 10 trades = 5 wins × $52.50 = $262.50 won
           - 5 losses × $25 = $125 lost
           = +$137.50 profit ✅✅

60% Win Rate:
- 10 trades = 6 wins × $52.50 = $315 won
           - 4 losses × $25 = $100 lost
           = +$215 profit ✅✅✅
```

## Configuration

### Position Sizing
```
MNQ Contracts: 1
MCL Contracts: 1
MGC Contracts: 1
```

### Risk/Reward Settings
```
Stop ATR Multiple:  1.0 (tight)
TP1 ATR Multiple:   2.0 (2:1 R/R)
TP2 ATR Multiple:   3.0 (3:1 R/R)
TP3 ATR Multiple:   4.5 (4.5:1 R/R)
```

### Trend Detection
```
ADX Threshold:      25 (trending vs choppy)
ADX Length:         14
Min Trend Strength: 0.3 (30% directional move)
Trend Lookback:     20 bars
```

### Impulse Detection
```
Impulse Threshold:  1.5 ATR (sharp spike)
Impulse Lookback:   3 bars
Volume Spike:       1.3x average
```

### Time Filters
```
Avoid First:        15 minutes
Avoid Last:         15 minutes
Max Trades/Day:     12
Min Bars Between:   8
```

### Risk Management
```
Max Daily Loss:         2%
Max Consecutive Losses: 3 (stops trading)
Profit Protection:      15 ticks trigger, 5 tick trail
```

## Visual Indicators

### Background Colors
- 🟢 Green tint = Trending market (OK to trade)
- 🔴 Red tint = Choppy market (NO trades)
- 🟠 Orange tint = Profit protection active
- 🔴 Dark red = Consecutive losses warning

### Entry Markers
- **TREND** triangle = Trend trade entry
- **IMPULSE** triangle = Impulse trade entry
- **CONT** triangle = Continuation trade entry

### Tables
- **Top Right:** Market regime (ADX, trend state, trades today)
- **Bottom Right:** Performance metrics (win rate, avg win/loss)

## Alert Format (TradersPost Compatible)

```json
{
  "ticker": "MGCZ2024",
  "action": "buy",
  "quantity": 1,
  "price": 2650.50,
  "stop_loss": 2648.20,
  "take_profit_1": 2655.10,
  "take_profit_2": 2658.40,
  "take_profit_3": 2663.00,
  "tp1_percent": 60,
  "tp2_percent": 30,
  "tp3_percent": 10,
  "trade_type": "TREND",
  "adx": 28.5,
  "trend_strength": 35.2,
  "account": "optional_account_id"
}
```

## Bug Fixes from Original

1. **Stop Loss Execution** - Fixed if-else chain that prevented stop execution
2. **Position Sizing** - Single source of truth (`currentManualContracts`)
3. **Profit Protection** - Proper trailing stop updates
4. **Pyramiding Disabled** - Prevents position sizing conflicts
5. **Time Filters** - Avoids opening/closing volatility

## Recommended Deployment

1. **Paper trade for 2 weeks minimum**
2. Verify ADX filter blocks 30-50% of potential trades
3. Confirm avg win > avg loss after 20+ trades
4. Start with 1 contract only
5. Track actual fills vs backtest results

## Adjustment Guidelines

If losses > wins after 20 trades:
- Increase ADX threshold (25 → 28)
- Increase min trend strength (0.3 → 0.4)
- Tighten impulse threshold (1.5 → 1.8)

## Files

- `trend-impulse-master-v8.pine` - Main strategy file
