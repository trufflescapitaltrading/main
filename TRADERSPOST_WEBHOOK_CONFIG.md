# TradersPost Webhook Configuration Guide

## 🔴 CRITICAL: Why Your Stops Were Not Executing

The original strategy sent alerts in a format that TradersPost couldn't properly parse for bracket orders. Here's the fix:

### ❌ OLD FORMAT (BROKEN):
```json
{
  "ticker": "MES1!",
  "action": "buy",
  "quantity": "1",
  "stop_loss": "5844.25",
  "take_profit": "5854.25"
}
```

**Problem**: `stop_loss` and `take_profit` as flat strings are NOT automatically converted to bracket orders by TradersPost.

### ✅ NEW FORMAT (FIXED):
```json
{
  "ticker": "MES1!",
  "action": "buy",
  "orderType": "limit",
  "limitPrice": "5850.25",
  "quantity": "1",
  "stopLoss": {
    "type": "stop",
    "stopPrice": "5844.25"
  },
  "takeProfit": {
    "type": "limit", 
    "limitPrice": "5854.25"
  }
}
```

---

## 📋 TradersPost Strategy Settings

### Step 1: Create/Edit Strategy

1. Go to TradersPost Dashboard → Strategies
2. Click "Create Strategy" or edit existing
3. Configure these settings:

| Setting | Value | Notes |
|---------|-------|-------|
| Name | V15 Fixed Scalper | Or your preferred name |
| Broker | Tradovate | Select your broker |
| Account | Your trading account | Paper or live |
| Symbol Mapping | Enabled | Maps MES1! to correct contract |

### Step 2: Webhook Configuration

```
Webhook URL: https://traderspost.io/trading/webhook/{STRATEGY_ID}/{SECRET}
```

**Webhook Settings:**
- ✅ Parse JSON body: **ON**
- ✅ Allow position sizing from signal: **ON**
- ✅ Enable bracket orders: **ON** (CRITICAL!)

### Step 3: Order Type Mapping

Configure these field mappings:

| Signal Field | TradersPost Field | Notes |
|--------------|-------------------|-------|
| `ticker` | Symbol | e.g., MES1! |
| `action` | Side | buy/sell/exit |
| `quantity` | Quantity | Number of contracts |
| `orderType` | Order Type | limit/market |
| `limitPrice` | Limit Price | Entry price |
| `stopLoss.stopPrice` | Stop Loss Price | SL trigger price |
| `takeProfit.limitPrice` | Take Profit Price | TP limit price |

---

## 🔧 Tradovate-Specific Configuration

### Bracket Order Settings:

1. Go to TradersPost → Broker Settings → Tradovate
2. Enable these options:
   - ✅ Use OCO (One-Cancels-Other) for bracket orders
   - ✅ Submit stop as STOP order (not stop-limit)
   - ✅ Submit take profit as LIMIT order

### Symbol Mapping for Micro Futures:

| Alert Symbol | Tradovate Symbol | Contract |
|--------------|------------------|----------|
| MES1! | MESZ4 (or current) | Micro E-mini S&P |
| MNQ1! | MNQZ4 (or current) | Micro E-mini Nasdaq |
| MYM1! | MYMZ4 (or current) | Micro E-mini Dow |
| MCL1! | MCLZ4 (or current) | Micro Crude Oil |
| MGC1! | MGCZ4 (or current) | Micro Gold |
| M2K1! | M2KZ4 (or current) | Micro Russell 2000 |

---

## 📤 Alert Examples

### Long Entry Alert:
```json
{
  "ticker": "MES1!",
  "action": "buy",
  "orderType": "limit",
  "limitPrice": "5850.50",
  "quantity": "1",
  "stopLoss": {
    "type": "stop",
    "stopPrice": "5844.50"
  },
  "takeProfit": {
    "type": "limit",
    "limitPrice": "5854.50"
  },
  "instrument": "MES",
  "strategy": "V15_FIXED",
  "signalPrice": "5850.00",
  "adx": "25.3",
  "trending": "true",
  "mtfAligned": "true"
}
```

### Short Entry Alert:
```json
{
  "ticker": "MNQ1!",
  "action": "sell",
  "orderType": "limit", 
  "limitPrice": "20150.00",
  "quantity": "1",
  "stopLoss": {
    "type": "stop",
    "stopPrice": "20170.00"
  },
  "takeProfit": {
    "type": "limit",
    "limitPrice": "20138.00"
  },
  "instrument": "MNQ",
  "strategy": "V15_FIXED",
  "signalPrice": "20152.00",
  "adx": "28.1",
  "trending": "true",
  "mtfAligned": "true"
}
```

### Exit Alert:
```json
{
  "ticker": "MES1!",
  "action": "exit",
  "reason": "trailing_stop"
}
```

### Trailing Stop Update Alert:
```json
{
  "ticker": "MES1!",
  "action": "update_stop",
  "newStopPrice": "5852.00",
  "direction": "long",
  "trailing": "true"
}
```

---

## ⚠️ Common Issues & Solutions

### Issue: Stop Loss Not Executing

**Symptoms:**
- Trades exit past the stop loss level
- No stop order appears in Tradovate

**Solutions:**
1. Check TradersPost logs for "bracket order" creation
2. Verify `stopLoss.stopPrice` is being parsed
3. Ensure Tradovate bracket orders are enabled
4. Check if stop was placed as STOP (not STOP-LIMIT)

### Issue: Large Entry Slippage

**Symptoms:**
- Entry fill price far from alert price
- Multiple points of slippage

**Solutions:**
1. Use LIMIT orders (not MARKET)
2. Add slippage buffer to entry price
3. Avoid trading during news events
4. Trade during high liquidity sessions (NY open)

### Issue: Orders Rejected by Tradovate

**Symptoms:**
- TradersPost shows "order rejected"
- No position opened

**Solutions:**
1. Check margin requirements
2. Verify contract month is correct
3. Ensure account has trading permissions
4. Check Tradovate for error messages

### Issue: Multiple Alerts Firing

**Symptoms:**
- Duplicate trades opened
- Same signal sent multiple times

**Solutions:**
1. Use `alert.freq_once_per_bar` in Pine Script
2. Enable deduplication in TradersPost
3. Add unique entry ID to alerts
4. Set minimum time between alerts

---

## 🧪 Testing Procedure

### Step 1: Paper Trading Test
1. Connect TradersPost to Tradovate PAPER account
2. Run strategy on chart with alerts enabled
3. Monitor TradersPost logs for each alert
4. Verify bracket orders appear in Tradovate

### Step 2: Verify Stop Loss Placement
1. After entry, check Tradovate for pending SL order
2. Compare SL price in Tradovate vs alert JSON
3. Manually trigger SL to verify execution

### Step 3: Test Trailing Stop Updates
1. Let trade move to breakeven
2. Verify "update_stop" alert is sent
3. Check if SL moves in Tradovate

### Step 4: Full Day Test
1. Run strategy for full trading session
2. Track all entries, exits, and SL levels
3. Compare expected vs actual PnL
4. Document any discrepancies

---

## 📊 Monitoring Dashboard

Create a tracking sheet with these columns:

| Time | Symbol | Action | Alert Price | Fill Price | Slippage | SL Set | SL Executed | PnL |
|------|--------|--------|-------------|------------|----------|--------|-------------|-----|
| 9:35 | MES | BUY | 5850.25 | 5850.50 | 0.25 | 5844.25 | Yes | +$12.50 |
| 10:12 | MNQ | SELL | 20150 | 20149 | 1.00 | 20170 | Yes | +$22.00 |

Track these metrics daily:
- Total trades
- Win rate %
- Average slippage
- SL execution rate
- Average winner/loser
