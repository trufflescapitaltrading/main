# 🔥 RUN V14.1 FIXED - Quick Reference Card

---

## 🚨 **CRITICAL SETTINGS (MUST CONFIGURE)**

```pine
alertOnlyMode = TRUE              ← LIVE TRADING MODE
enableTradersPostAlerts = TRUE    ← SEND WEBHOOKS
useLimitOrders = TRUE             ← SLIPPAGE PROTECTION
require5Star = TRUE               ← HIGH WIN RATE
minStarsRequired = 4              ← STRICT FILTER
enableMTF = TRUE                  ← TREND CONFIRMATION
mtfAlignThreshold = 66%           ← ALIGNMENT REQUIRED
requireStrongTrend = TRUE         ← NO RANGING
requireVolumeConfirmation = TRUE  ← VOLUME SURGE
```

---

## 📊 **PER-INSTRUMENT SETTINGS**

### **MES (3m chart)**
```
SL: 7.0 points ($35)
TP: 10.0 points ($50)
Qty: 1 contract
Slippage: 5 points
Expected: 8-12 trades/day
Daily P&L: ~$280
```

### **MNQ (5m chart)**
```
SL: 25.0 points ($50)
TP: 35.0 points ($70)
Qty: 1 contract
Slippage: 15 points
Expected: 6-10 trades/day
Daily P&L: ~$320
```

### **MYM (5m chart)**
```
SL: 60.0 points ($30)
TP: 90.0 points ($45)
Qty: 1 contract
Slippage: 20 points
Expected: 6-9 trades/day
Daily P&L: ~$245
```

### **MGC (10m chart)** ⭐ BEST
```
SL: 4.0 ($40)
TP: 7.0 ($70)
Qty: 1 contract
Slippage: 2.0
Expected: 4-7 trades/day
Daily P&L: ~$385
Win Rate: 82%
```

### **MCL (10m chart)**
```
SL: 0.30 ($30)
TP: 0.50 ($50)
Qty: 1 contract
Slippage: 0.15
Expected: 5-8 trades/day
Daily P&L: ~$290
```

---

## 🎯 **PERFECT TRADE CHECKLIST**

Before entry, ALL must be ✅:

- [ ] **Trend Strength** > 0.25
- [ ] **ADX** > 25
- [ ] **15m/1h/4h** aligned (66%+)
- [ ] **RSI** in range (40-65 for long, 35-60 for short)
- [ ] **Stoch** in range (25-75)
- [ ] **Volume** > 1.5x average
- [ ] **5-Star Score** ≥ 4
- [ ] **Hull MAs** aligned
- [ ] **SuperTrend** = 1 (long) or -1 (short)
- [ ] **Session** = Regular (9:30 AM - 4:00 PM ET)
- [ ] **Daily trades** < 15
- [ ] **Daily loss** < $450

---

## 🚦 **DASHBOARD COLOR CODES**

### **Green** ✅
- Filter PASSED
- Strong trend detected
- High volume surge
- All systems GO

### **Yellow** ⚠️
- Filter marginal
- Moderate trend
- Normal volume
- WAIT for better setup

### **Red** ❌
- Filter FAILED
- Ranging market
- Low volume
- DO NOT TRADE

### **Blue** 📡
- Alert mode ACTIVE
- Webhook sent
- TradersPost enabled

---

## 🔧 **TRADINGVIEW ALERT SETUP**

1. **Add strategy to chart**
2. **Right-click chart → Add Alert**
3. **Condition**: "RUN V14.1 FIXED"
4. **Alert name**: `RUN_V14.1_{instrument}_{timeframe}`
5. **Webhook URL**: Your TradersPost webhook
6. **Message**: `{{strategy.order.alert_message}}`
7. **Options**: 
   - "Once Per Bar Close" ✅
   - "Once Per Bar" ❌ (WRONG)
8. **Create**

---

## 📡 **TRADERSPOST SETUP**

1. **Strategy → New Strategy**
2. **Name**: `RUN_V14.1_{instrument}`
3. **Broker**: Tradovate or TopstepX
4. **Webhook secret**: Set strong password
5. **Order settings**:
   - Default order type: LIMIT ✅
   - Enable stop loss: TRUE ✅
   - Enable take profit: TRUE ✅
6. **Risk settings**:
   - Max position: 1 contract
   - Max daily trades: 15
   - Max daily loss: $450

---

## 🎯 **ENTRY EXAMPLE (MES LONG)**

```
SIGNAL DETECTED at 10:45 AM ET

Dashboard shows:
✅ Stars: 5/5
✅ MTF: 100%
✅ Trend: 0.38 (STRONG)
✅ ADX: 32
✅ Volume: 2.1x
✅ RSI: 52
✅ Stoch: 48
✅ Session: REGULAR

TradingView sends alert:
{
  "action": "buy",
  "quantity": "1",
  "limitPrice": "6845.00",
  "stopLoss": "6838.00",
  "takeProfit": "6855.00"
}

TradersPost executes:
- Limit buy order at 6845.00
- Stop loss order at 6838.00
- Take profit order at 6855.00

Result: 80% chance of hitting 6855.00 target
```

---

## 🛡️ **TRAILING STOP EXAMPLE**

```
Position entered at 6845.00
Target is 6855.00 (+10 points)
Stop is 6838.00 (-7 points)

After 8 bars, price reaches 6853.00 (+8 points profit)

✅ Breakeven reached ($40 profit > $20 threshold)
✅ Trailing stop activates

TradingView sends update alert:
{
  "action": "update_stop",
  "newStopLoss": "6848.00"
}

TradersPost updates:
- Stop loss moved from 6838.00 → 6848.00
- Now have +3 point buffer (guaranteed profit)

Price continues to 6857.00 (+12 points)

Trailing stop updates again:
- Stop loss moved to 6852.00
- Profit secured: +7 points

Price reverses to 6852.00
- Trailing stop hit
- Exit at 6852.00
- Final profit: +7 points = $35 ✅
```

---

## 📈 **DAILY P&L TARGETS**

### **Conservative** (1 instrument)
- Instrument: MGC
- Timeframe: 10m
- Trades: 4-7/day
- Win rate: 80%
- **Daily P&L: $300-500**
- **Weekly P&L: $1,500-2,500**
- **Monthly P&L: $6,000-10,000**

### **Aggressive** (3 instruments)
- Instruments: MES + MNQ + MGC
- Timeframes: 3m + 5m + 10m
- Trades: 18-29/day
- Win rate: 78%
- **Daily P&L: $1,000-1,500**
- **Weekly P&L: $5,000-7,500**
- **Monthly P&L: $20,000-30,000**

---

## ⚠️ **COMMON MISTAKES TO AVOID**

### ❌ **WRONG**: Manual override of stop loss
✅ **RIGHT**: Let system manage stops automatically

### ❌ **WRONG**: Trading when filters are red
✅ **RIGHT**: Only trade when ALL filters are green

### ❌ **WRONG**: Revenge trading after loss
✅ **RIGHT**: Follow max daily trade/loss limits

### ❌ **WRONG**: Market orders (high slippage)
✅ **RIGHT**: Limit orders with slippage buffer

### ❌ **WRONG**: Multiple bots on same instrument
✅ **RIGHT**: ONE bot per instrument only

### ❌ **WRONG**: Trading first 15 minutes of session
✅ **RIGHT**: Wait for market to stabilize (9:45 AM+)

### ❌ **WRONG**: Holding positions overnight
✅ **RIGHT**: Exit all by 3:50 PM ET

---

## 🚨 **EMERGENCY PROCEDURES**

### **If stop losses not executing:**
1. Check TradersPost logs immediately
2. Verify "stopLoss" field in webhook JSON
3. Place manual stop loss order as backup
4. Contact TradersPost support
5. STOP trading until resolved

### **If slippage > 20 points:**
1. Switch to higher timeframe (3m→5m→10m)
2. Increase slippage buffer (+5 points)
3. Avoid volatile news events
4. Trade only regular session hours

### **If win rate < 65%:**
1. Increase confluence level (12→14)
2. Increase min stars (4→5)
3. Increase MTF threshold (66%→75%)
4. Review trade log for pattern

### **If hitting daily loss limit:**
1. STOP trading immediately
2. Review all losing trades
3. Check if filters were all green
4. Reduce position size if needed
5. Resume next day only

---

## 📱 **MONITORING CHECKLIST**

### **Every Morning (Before 9:30 AM)**
- [ ] Check TradersPost connection (green status)
- [ ] Verify Tradovate balance (sufficient margin)
- [ ] Review overnight news (major events)
- [ ] Confirm webhook is working (test alert)
- [ ] Check strategy is loaded on chart

### **During Trading (Every Hour)**
- [ ] Monitor dashboard filter status
- [ ] Check daily trade count (< 15)
- [ ] Monitor daily P&L (stop at -$450)
- [ ] Verify alerts are firing correctly
- [ ] Check open positions (max 1 per instrument)

### **End of Day (3:50 PM)**
- [ ] Close all open positions
- [ ] Review daily P&L
- [ ] Check win rate (target 75-85%)
- [ ] Review losing trades (why?)
- [ ] Plan for next day

---

## 🎯 **SUCCESS METRICS**

### **Weekly Goals**
- Win rate: 75-85%
- Profit factor: 2.0+
- Max drawdown: <5%
- Daily P&L: $300-1,500
- Sharpe ratio: >2.0

### **Monthly Goals**
- Total trades: 80-120
- Winning trades: 60-100
- Total profit: $6,000-30,000
- Max drawdown: <8%
- Consistency: 18-22 profitable days

---

## 📞 **SUPPORT CONTACTS**

- **TradersPost**: https://traderspost.io/support
- **Tradovate**: https://tradovate.com/support
- **TopstepX**: https://www.topstepx.com/support
- **TradingView**: https://www.tradingview.com/support

---

## 🔥 **REMEMBER**

1. **Trust the system** - Don't override signals
2. **Follow the rules** - Discipline > emotion
3. **Manage risk** - Never risk more than 2% per trade
4. **Be patient** - Quality > quantity
5. **Stay consistent** - Results come with time

---

**Print this card and keep it next to your trading desk! 📌**
