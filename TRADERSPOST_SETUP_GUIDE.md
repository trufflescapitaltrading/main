# TradersPost Setup Guide for MGC Alert-Only System

## Complete Setup Instructions for Automated Trading

This guide walks you through setting up the MGC Alert-Only system with TradersPost for automated trading on Tradovate or TopstepX.

---

## Prerequisites

Before you begin, ensure you have:

- [ ] TradingView Pro account (or higher) - Required for webhook alerts
- [ ] TradersPost account (free tier works, paid recommended)
- [ ] Tradovate or TopstepX broker account
- [ ] MGC_ALERT_ONLY_TRADERSPOST.pine indicator file

---

## Step 1: Load the Indicator in TradingView

### 1.1 Open Pine Script Editor
1. Open TradingView and navigate to MGC chart
2. Select **5-minute timeframe** (recommended)
3. Click the "Pine Editor" tab at the bottom

### 1.2 Add the Indicator
1. Click "New" > "Create new indicator"
2. Delete all default code
3. Copy the entire contents of `MGC_ALERT_ONLY_TRADERSPOST.pine`
4. Paste into the Pine Editor
5. Click "Save" and name it: `MGC ALERT ONLY - TradersPost`
6. Click "Add to Chart"

### 1.3 Verify Indicator is Working
You should see:
- Two tables on chart (Performance + Confluence)
- EMA lines plotted
- Hull MA line
- Background color changes when confluence is high

---

## Step 2: Set Up TradersPost Account

### 2.1 Create Account
1. Go to [traderspost.io](https://traderspost.io)
2. Click "Sign Up"
3. Complete registration
4. Verify email

### 2.2 Connect Your Broker

#### For Tradovate:
1. Go to **Settings** > **Brokers**
2. Click "Connect Broker"
3. Select "Tradovate"
4. Enter your Tradovate credentials
5. Authorize the connection
6. Select your trading account (live or paper)

#### For TopstepX:
1. Go to **Settings** > **Brokers**
2. Click "Connect Broker"
3. Select "Tradovate" (TopstepX uses Tradovate)
4. Use your TopstepX-provided Tradovate credentials
5. Authorize the connection
6. Select your funded account

### 2.3 Verify Broker Connection
- Status should show "Connected" in green
- Account balance should be visible
- Test with a small manual trade if desired

---

## Step 3: Create TradersPost Strategy

### 3.1 Create New Strategy
1. Go to **Strategies** in TradersPost
2. Click "Create Strategy"
3. Configure:

```
Strategy Name: MGC 80% Win Rate System
Broker: [Your connected broker]
Asset Class: Futures
```

### 3.2 Symbol Mapping
Configure the symbol mapping:

```
TradingView Symbol: MGC1!
Broker Symbol: MGCM4 (or current front month)
```

Note: Update the broker symbol to match the current contract month:
- MGCM4 = June 2024
- MGCU4 = September 2024
- MGCZ4 = December 2024
- MGCG5 = February 2025

### 3.3 Position Sizing
```
Quantity Type: Fixed
Quantity: 1 contract
Max Position Size: 1 contract
```

### 3.4 Risk Management
```
Max Daily Loss: $100 (or your preference)
Max Trades Per Day: 10 (indicator limits to 5, this is safety buffer)
Flatten at End of Day: Enabled
Flatten Time: 15:55 ET
```

### 3.5 Get Webhook URL
1. Click "Save Strategy"
2. Go to "Webhook" tab
3. Copy the Webhook URL - you'll need this for TradingView

Your webhook URL looks like:
```
https://traderspost.io/trading/webhook/XXXXXX/XXXXXX
```

---

## Step 4: Create TradingView Alert

### 4.1 Open Alert Dialog
1. On your MGC chart with the indicator loaded
2. Click the "Alert" button (clock icon) or press Alt+A
3. Select "Create Alert"

### 4.2 Configure Alert Condition

```
Condition: MGC ALERT ONLY - TradersPost
         > Any alert() function call

Options:
  - Trigger: Once Per Bar Close
  - Expiration: Open-ended (or set to 1 year)
```

### 4.3 Configure Actions

```
Alert actions:
  [x] Webhook URL
  
Webhook URL: [Paste your TradersPost webhook URL from Step 3.5]
```

### 4.4 Configure Message

**IMPORTANT**: Leave the message field with the default or use:

```
{{message}}
```

The indicator automatically generates the correct JSON message.

### 4.5 Notification Settings (Optional)
```
[x] Show popup
[x] Send email
[ ] Play sound
[x] Send to app
```

### 4.6 Create Alert
1. Click "Create"
2. Verify alert appears in your Alert Manager

---

## Step 5: Verify the Setup

### 5.1 Test Alert Firing
1. Wait for a 7/10+ confluence signal
2. Or temporarily lower minimum confluence to 5/10 for testing
3. Watch for alert to fire

### 5.2 Check TradersPost Activity Log
1. Go to TradersPost > Activity Log
2. Look for your webhook
3. Verify JSON payload received correctly
4. Check if order was sent to broker

### 5.3 Verify Broker Execution
1. Log into Tradovate/TopstepX
2. Check order history
3. Verify trade executed at expected price

### 5.4 Monitor First Live Trade
1. Watch the full trade lifecycle:
   - Entry alert fires
   - Position opens
   - TP1 alert fires (if reached)
   - Stop or TP2/TP3 closes position

---

## Configuration Reference

### Indicator Settings

| Setting | Default | Description |
|---------|---------|-------------|
| Minimum Confluence Score | 7 | Signals need 7/10 points minimum |
| ADX Threshold | 30 | Only trade strong trends |
| Max Trades Per Day | 5 | Quality over quantity |
| Min Bars Between Trades | 15 | Prevents overtrading |
| Fixed Contracts | 1 | Position size |
| Ticker Symbol | MGC1! | Symbol sent in alerts |
| Enable TradersPost Alerts | true | Master alert switch |

### Stop Loss Settings

| Setting | Default | Description |
|---------|---------|-------------|
| Initial Stop (ATR) | 1.2 | ~$30 for MGC |
| Breakeven Trigger (ATR) | 1.5 | Move stop to BE after +1.5 ATR |
| Trailing Activation (ATR) | 3.0 | Start trailing after +3 ATR |
| Trailing Distance (ATR) | 1.5 | Trail distance |

### Take Profit Settings

| Setting | Default | Description |
|---------|---------|-------------|
| TP1 (ATR) | 2.5 | ~$60 profit, exit 70% |
| TP2 (ATR) | 4.0 | ~$100 profit, exit 25% |
| TP3 (ATR) | 6.0 | ~$150 profit, exit final 5% |

---

## Troubleshooting

### Alert Not Firing

**Problem**: No alerts despite high confluence
**Solutions**:
1. Verify "Enable TradersPost Alerts" is checked
2. Check session hours (default: 9:30 AM - 3:50 PM ET only)
3. Verify daily trade limit not reached
4. Ensure minimum bars between trades has passed
5. Check TradingView alert is active (not expired)

### Webhook Not Received

**Problem**: Alert fires but TradersPost shows no activity
**Solutions**:
1. Verify webhook URL is correct in TradingView alert
2. Check TradersPost account is active
3. Ensure no typos in webhook URL
4. Check TradersPost service status

### Order Not Executing

**Problem**: Webhook received but no broker order
**Solutions**:
1. Verify broker connection is active
2. Check symbol mapping (MGC1! -> correct contract month)
3. Verify account has sufficient margin
4. Check max daily loss not exceeded
5. Ensure trading hours are correct for futures

### Position Size Incorrect

**Problem**: Wrong number of contracts traded
**Solutions**:
1. Check "Fixed Contracts" setting in indicator
2. Verify TradersPost quantity settings
3. Ensure "Quantity" in strategy matches indicator

### Stop/TP Not Working

**Problem**: Exits not executing properly
**Solutions**:
1. Check broker supports bracket orders
2. Verify stop/limit prices are valid
3. Check position is open before exit alerts fire
4. Review TradersPost activity log for errors

---

## Best Practices

### Daily Routine

1. **Before Market Open (9:00 AM ET)**
   - Check TradingView alert is active
   - Verify TradersPost broker connection
   - Review any overnight changes

2. **During Trading (9:30 AM - 3:50 PM ET)**
   - Monitor TradersPost activity log
   - Watch for signal quality (confluence score)
   - Don't interfere with automated system

3. **After Market Close**
   - Review daily trades in TradersPost
   - Check P&L against expected
   - Note any issues for troubleshooting

### Weekly Maintenance

- Roll to new contract month before expiration
- Update symbol mapping in TradersPost
- Review win rate and adjust confluence threshold if needed
- Check for indicator updates

### Risk Management

- Never increase contract size after losses
- Stick to 1 contract until consistent profitability
- Keep max daily loss at $100 or 2% of account
- Don't override the system manually

---

## Quick Reference Card

### Alert Message Format (Auto-generated)

**Entry (Long)**:
```json
{
  "ticker": "MGC1!",
  "action": "buy",
  "orderType": "market",
  "quantity": 1,
  "stopLoss": {"type": "stop", "stopPrice": 2515.80},
  "takeProfit": {"type": "limit", "limitPrice": 2608.30},
  "sentiment": "bullish",
  "confluenceScore": 8
}
```

**Entry (Short)**:
```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 1,
  "stopLoss": {"type": "stop", "stopPrice": 2608.30},
  "takeProfit": {"type": "limit", "limitPrice": 2515.80},
  "sentiment": "bearish",
  "confluenceScore": 7
}
```

**Exit (TP/Stop)**:
```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "limit",
  "quantity": 0.7,
  "limitPrice": 2608.30,
  "reason": "TP1_70_percent"
}
```

---

## Support Resources

- **TradersPost Documentation**: [docs.traderspost.io](https://docs.traderspost.io)
- **TradingView Pine Script**: [pine-script-docs](https://www.tradingview.com/pine-script-docs)
- **Tradovate Support**: [tradovate.com/support](https://www.tradovate.com/support)

---

## Deployment Checklist

Use this checklist before going live:

```
INDICATOR SETUP
[ ] MGC_ALERT_ONLY_TRADERSPOST.pine loaded on MGC 5m chart
[ ] Indicator shows tables and plots correctly
[ ] "Enable TradersPost Alerts" is checked
[ ] Ticker symbol set correctly (MGC1!)
[ ] Fixed contracts set to desired quantity

TRADERSPOST SETUP
[ ] Account created and verified
[ ] Broker connected (Tradovate/TopstepX)
[ ] Strategy created with correct settings
[ ] Symbol mapping configured (MGC1! -> MGCX4)
[ ] Webhook URL copied

TRADINGVIEW ALERT
[ ] Alert created on MGC chart
[ ] Condition: "Any alert() function call"
[ ] Frequency: "Once Per Bar Close"
[ ] Webhook URL pasted correctly
[ ] Alert is active (not expired)

VERIFICATION
[ ] Test alert fired successfully
[ ] Webhook received in TradersPost
[ ] Test trade executed in broker
[ ] Stop and TP orders placed correctly

LIVE TRADING
[ ] Paper traded for at least 1 week
[ ] Comfortable with system behavior
[ ] Risk parameters set appropriately
[ ] Emergency flatten procedure understood
```

---

*System ready for automated trading when all boxes checked.*
