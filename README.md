# bot-win-rate-optimization

This repo contains the TradingView Pine v5 strategy source with enhanced win rate optimization features:

- `mnq_mes_multitf_cursor_v71.pine`

## V71 Win Rate Optimization Features

This version builds upon V70's foundation and adds several new win rate optimization systems:

### 🏆 New Features in V71

#### 1. Adaptive Trailing Stop System
- **Purpose**: Protect profits by trailing the stop loss as price moves in your favor
- **Activation**: Triggers when profit reaches a configurable percentage of TP1 (default: 50%)
- **Behavior**: Trails from the maximum profit seen, stepping back by a configurable percentage (default: 25%)
- **Benefit**: Locks in profits on extended moves while allowing room for normal retracements

#### 2. Time-Decay Profit Lock
- **Purpose**: Automatically protect profits that have been held for multiple bars
- **Activation**: Triggers after holding a profitable position for X bars (default: 8 bars)
- **Requirement**: Position must be at minimum profit threshold (default: 30% of TP1)
- **Behavior**: Locks in a percentage of current profit (default: 50%)
- **Benefit**: Prevents profitable trades from turning into losses due to delayed exits

#### 3. Momentum-Fade Early Exit
- **Purpose**: Exit early when momentum is fading while in profit
- **Detection**: Monitors RSI changes over configurable lookback period (default: 3 bars)
- **Trigger**: Exits when RSI delta exceeds threshold (default: 0.7) and momentum reverses
- **Benefit**: Captures profits before momentum reversal turns winners into losers

#### 4. Quick Scalp Exit
- **Purpose**: Take quick profits on fast-moving trades
- **Target**: Lower than normal TP1 (default: 40% of TP1)
- **Window**: Only active within first X bars (default: 5 bars)
- **Benefit**: Increases win rate by capturing smaller, more frequent wins

#### 5. Volatility-Adjusted Exits
- **Purpose**: Adapt take-profit targets based on current market volatility
- **Detection**: Compares current ATR to 20-period ATR average
- **Adjustment**: Reduces TP targets during high volatility (ratio > 1.2)
- **Benefit**: Prevents unrealistic TP targets in choppy/volatile conditions

#### 6. Strict Entry Filter (Optional)
- **Purpose**: Filter entries to only take highest-probability setups
- **Requirements**: Minimum ADX (default: 18) and RSI within range (default: 35-65)
- **Benefit**: Reduces low-quality trades that lower overall win rate

### ⚙️ Configuration Options

```
🏆 WIN RATE OPTIMIZATION V71 Settings:
├── ✅ Enable Adaptive Trailing Stop (default: true)
│   ├── Trailing Activation: 50% of TP1
│   └── Trailing Step: 25%
├── ✅ Enable Time-Decay Profit Lock (default: true)
│   ├── Bars Before Lock: 8
│   ├── Min Profit for Lock: 30% of TP1
│   └── Keep Profit: 50%
├── ✅ Enable Momentum-Fade Exit (default: true)
│   ├── Bars for Check: 3
│   └── Fade Threshold: 0.7
├── ✅ Quick Scalp Exit (default: true)
│   ├── Quick Profit: 40% of TP1
│   └── Max Bars: 5
├── ✅ Volatility-Adjusted Exits (default: true)
│   └── Adjustment Factor: 0.8
└── ✅ Strict Entry Filter (default: true)
    ├── Min ADX: 18
    ├── RSI Low: 35
    └── RSI High: 65
```

### 📊 Enhanced Performance Table

The on-chart performance table now includes:
- **V71 OPT**: Shows current optimization state (READY/ACTIVE/TRAIL/LOCK)
- **VOL ADJ**: Shows current volatility adjustment multiplier

### 🎯 Target Win Rate Improvement

These optimizations are designed to:
1. **Reduce losing trades** by exiting early when momentum fades
2. **Protect profits** through adaptive trailing and time-based locks
3. **Capture quick wins** with scalp-level exit targets
4. **Filter low-quality entries** with strict entry requirements
5. **Adapt to volatility** to avoid unrealistic profit targets

### 📈 Recommended Usage

1. **For MNQ 5-minute charts**: Enable all V71 features with default settings
2. **For MES charts**: Consider slightly higher trailing activation (60-70%)
3. **For 3-minute charts**: Lower quick scalp bars to 3-4
4. **For volatile sessions**: V71 automatically adjusts via volatility detection

### ⚠️ Important Notes

- V71 features work best with **High Win Rate Mode** enabled
- All V71 features can be individually enabled/disabled
- Features are cumulative - the best stop level is always selected
- Variables reset automatically on position close

## Previous Features (from V70)

- **Single-contract exits**: MNQ 5m in High Win Rate Mode targets TP1 (not TP2)
- **Post-TP1 protection**: Once TP1 is tagged, remaining size protected at breakeven
- **On-chart performance table**: Uses full Strategy Tester totals

## Changelog

### V71 (Current)
- Added Adaptive Trailing Stop System
- Added Time-Decay Profit Lock mechanism
- Added Momentum-Fade Early Exit system
- Added Quick Scalp Exit feature
- Added Volatility-Adjusted Exits
- Added Strict Entry Filter option
- Enhanced performance metrics table

### V70
- Initial win rate optimization features
- Single-contract TP1 targeting
- BE-after-TP1 protection
