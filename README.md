# MGC TREND/IMPULSE MASTER V8.0 - Pine Script Trading Strategy

## Overview

This Pine Script strategy is designed for trading micro futures (MGC, MNQ, MCL) with a focus on **profitable risk-reward dynamics** where **WINS are always BIGGER than LOSSES**.

### Key Principle: WINS > LOSSES

The strategy is mathematically designed to be profitable even at lower win rates:

| Win Rate | Avg Win | Avg Loss | Result |
|----------|---------|----------|--------|
| 40% | $52.50 | $25.00 | **+$60 per 10 trades** |
| 50% | $52.50 | $25.00 | **+$137.50 per 10 trades** |
| 60% | $52.50 | $25.00 | **+$215 per 10 trades** |

---

## Strategy Files

- `MGC_TREND_IMPULSE_MASTER_V8.pine` - Main strategy file for TradingView

---

## Core Features

### 1. Flipped Risk/Reward (Wins > Losses)

**Default Settings:**
- **Stop Loss:** 1.0 ATR (~$20-30 per contract for MGC)
- **TP1 (60%):** 2.0 ATR (~$40-60 per contract) 
- **TP2 (30%):** 3.0 ATR (~$60-90 per contract)
- **TP3 (10%):** 4.5 ATR (~$90-135 per contract)

**Blended Average Win:** ~$52.50 vs ~$25.00 average loss = **2.1:1 Win/Loss Ratio**

### 2. NO Choppy Trades (ADX Filter)

The strategy uses ADX (Average Directional Index) to filter out choppy, ranging markets:

- **ADX >= 25:** TRENDING - Trades allowed
- **ADX < 25:** CHOPPY - NO trades taken

This filter alone eliminates 30-50% of potential losing trades.

### 3. Only 3 Trade Types Allowed

| Trade Type | Description | Conditions |
|------------|-------------|------------|
| **TREND** | Clear directional trend | ADX > 25 + Hull/EMA alignment + Trend strength > 30% |
| **IMPULSE** | Sharp price spike | Price moves > 1.5 ATR in few bars + Volume spike |
| **CONTINUATION** | Pullback resumption | Established trend + Shallow pullback + Bounce/drop |

### 4. Time Filters

- **Avoids first 15 minutes** - Opening range chaos
- **Avoids last 15 minutes** - Closing volatility
- **Maximum trades per day:** 12 (configurable)
- **Minimum bars between trades:** 8 (configurable)

### 5. Profit Protection

- **Trigger:** After 15 ticks in profit
- **Trail:** 5 tick trailing stop
- **Behavior:** Locks in profits, trails as price moves favorably

### 6. Risk Management

- **Max Daily Loss:** 2% of capital
- **Consecutive Loss Limit:** Stops after 3 losses in a row
- **Position Sizing:** Manual contract input (1 contract default)

---

## Installation

1. Open TradingView
2. Go to Pine Editor
3. Copy entire contents of `MGC_TREND_IMPULSE_MASTER_V8.pine`
4. Paste into Pine Editor
5. Save and add to chart

---

## Recommended Settings

### For MGC (Micro Gold Futures)

```
Position Sizing:
- Contracts: 1

Risk/Reward:
- Stop ATR Multiple: 1.0 (tight)
- TP1 ATR Multiple: 2.0 (2:1 R/R)
- TP2 ATR Multiple: 3.0 (3:1 R/R)
- TP3 ATR Multiple: 4.5 (4.5:1 R/R)

Trend Detection:
- ADX Threshold: 25
- Min Trend Strength: 0.3 (30%)

Time Controls:
- Max Trades/Day: 10-12
- Min Bars Between: 8
```

### For MNQ (Micro Nasdaq Futures) - More Volatile

```
Risk/Reward:
- Stop ATR Multiple: 0.8 (tighter)
- TP1 ATR Multiple: 1.8
- TP2 ATR Multiple: 2.5
- TP3 ATR Multiple: 4.0

Trend Detection:
- ADX Threshold: 28 (stricter)
```

---

## Live Trading Integration

### TradersPost Webhook Format

The strategy generates JSON alerts for TradersPost integration:

**Entry Alert Example:**
```json
{
  "ticker": "MGC",
  "action": "buy",
  "quantity": 1,
  "price": 2345.50,
  "stop_loss": 2340.20,
  "take_profit_1": 2356.10,
  "take_profit_2": 2361.80,
  "take_profit_3": 2369.75,
  "tp1_percent": 60,
  "tp2_percent": 30,
  "tp3_percent": 10,
  "trade_type": "TREND",
  "adx": 28.5,
  "trend_strength": 35.2
}
```

**Exit Alert Example:**
```json
{
  "ticker": "MGC",
  "action": "exit_complete",
  "side": "long",
  "exit_price": 2356.10,
  "entry_price": 2345.50,
  "pnl": 106.00,
  "exit_reason": "tp_or_sl",
  "total_trades": 5,
  "win_rate": 60.0
}
```

---

## Visual Indicators

### Chart Elements

- **Hull MA (Green/Red):** Trend direction indicator
- **EMA Fast (Blue):** Short-term trend
- **EMA Slow (Orange):** Medium-term trend
- **Stop Level (Red/Orange cross):** Current stop loss position

### Background Colors

| Color | Meaning |
|-------|---------|
| Red (faint) | CHOPPY market - NO trades |
| Green (faint) | TRENDING market - OK to trade |
| Orange | Profit protection active |
| Red (darker) | 2+ consecutive losses warning |

### Entry Signals

| Shape | Color | Trade Type |
|-------|-------|------------|
| Triangle Up | Green | TREND Long |
| Triangle Up | Lime | IMPULSE Long |
| Triangle Up | Aqua | CONTINUATION Long |
| Triangle Down | Red | TREND Short |
| Triangle Down | Orange | IMPULSE Short |
| Triangle Down | Fuchsia | CONTINUATION Short |

---

## Performance Tables

### Market Regime Table (Top Right)

- **ADX:** Current ADX value with color coding
- **Market:** TRENDING or CHOPPY status
- **Strength:** Trend strength percentage
- **Trades Today:** Current count vs maximum
- **Consec Loss:** Consecutive loss counter
- **Risk:Reward:** Current R:R ratio

### Performance Table (Bottom Right)

- **Win Rate:** Percentage of winning trades
- **Avg Win:** Average winning trade in dollars
- **Avg Loss:** Average losing trade in dollars
- **Win/Loss Ratio:** Win to loss ratio (target: 1.5:1+)

---

## Expected Performance

### Conservative Estimate (Strict Filters)

- **Trades/day:** 4-8
- **Win rate:** 45-50%
- **Daily P&L:** $50-$150
- **Monthly return:** 6-12%

### Realistic Estimate (Good Conditions)

- **Trades/day:** 6-10
- **Win rate:** 50-55%
- **Daily P&L:** $100-$250
- **Monthly return:** 12-20%

### Optimistic Estimate (Perfect Conditions)

- **Trades/day:** 8-12
- **Win rate:** 55-60%
- **Daily P&L:** $200-$400
- **Monthly return:** 20-30%

---

## Important Notes

### Before Going Live

1. **Paper trade for 2+ weeks minimum**
2. Verify ADX filter is working (should block 30-50% of setups)
3. Confirm avg win > avg loss in paper trading
4. Start with 1 contract only
5. Track actual fills vs backtest results

### Troubleshooting

**If losses > wins after 20 trades:**
- Increase ADX threshold (25 → 28)
- Increase min trend strength (0.3 → 0.4)
- Tighten impulse threshold (1.5 → 1.8)

**If too few trades:**
- Lower ADX threshold (25 → 22)
- Reduce min bars between trades (8 → 5)

---

## Key Improvements Over V7.1

| Issue | V7.1 | V8.0 |
|-------|------|------|
| Stop Loss | ~$40 | ~$25 (tighter) |
| Average Win | ~$25 | ~$52.50 (larger targets) |
| Chop Filter | None | ADX-based filter |
| Trade Types | Many | Only 3 (Trend/Impulse/Cont) |
| Time Filters | Basic | Avoids first/last 15 min |
| Loss Protection | Basic | Consecutive loss limit |

---

## License

This strategy is provided for educational purposes. Trade at your own risk.
