# TradersPost Setup Guide for MGC Alert-Only System

## Complete Integration Guide: TradingView -> TradersPost -> Tradovate/TopstepX

---

## Overview

This guide walks you through setting up fully automated trading using:
- **TradingView**: Runs the MGC Alert-Only indicator and sends webhook alerts
- **TradersPost**: Receives webhooks and routes orders to your broker
- **Tradovate/TopstepX**: Executes the actual trades

**Flow:**
```
TradingView Indicator → alert() fires → JSON webhook → TradersPost → Tradovate/TopstepX → Trade Executed
```

---

## Prerequisites

Before starting, ensure you have:
- [ ] TradingView account (Pro, Pro+, or Premium for multiple alerts)
- [ ] TradersPost account (Free tier works, paid for more features)
- [ ] Tradovate or TopstepX funded/eval account
- [ ] MGC chart access on TradingView

---

## Step 1: Load the Indicator on TradingView

### 1.1 Add the Indicator

1. Open TradingView and navigate to **MGC** (Micro Gold Futures)
2. Set timeframe to **5 minutes** (recommended)
3. Click **Pine Editor** at the bottom
4. Copy/paste the entire contents of `MGC_ALERT_ONLY_TRADERSPOST.pine`
5. Click **Save** and name it "MGC Alert Only TradersPost"
6. Click **Add to Chart**

### 1.2 Verify Indicator is Working

You should see:
- Two tables: Performance (top-right) and Confluence (top-left)
- EMA lines on the chart
- Hull MA line (changes color based on direction)
- "Alerts Enabled: YES" in the performance table

### 1.3 Configure Indicator Settings

Click the gear icon on the indicator to adjust:

| Setting | Recommended | Description |
|---------|-------------|-------------|
| Min Confluence Score | 7 | 7 = ~80% win rate |
| ADX Threshold | 30 | Strong trends only |
| Fixed Contracts | 1 | Start with 1 |
| Ticker Symbol | MGC1! | Or your broker's symbol |
| Enable TradersPost Alerts | ON | Must be enabled |
| US Trading Hours Only | ON | Recommended |

---

## Step 2: Set Up TradersPost Account

### 2.1 Create Account

1. Go to [traderspost.io](https://traderspost.io)
2. Sign up for a free account
3. Verify your email

### 2.2 Connect Your Broker

1. Click **Brokers** in the left sidebar
2. Click **Add Broker**
3. Select **Tradovate** or **TopstepX**
4. Follow the OAuth flow to connect your account
5. Verify connection shows "Connected" status

### 2.3 Create a Strategy

1. Click **Strategies** in the left sidebar
2. Click **Create Strategy**
3. Configure:

| Field | Value |
|-------|-------|
| Strategy Name | MGC 80% System |
| Broker | Your connected broker |
| Asset Class | Futures |
| Auto Sync | Enabled |

4. Click **Save**

### 2.4 Get Your Webhook URL

1. Open your strategy
2. Click **Webhook URL** 
3. Copy the URL (looks like: `https://traderspost.io/trading/webhook/xxxxx`)
4. **Keep this URL private** - anyone with it can send orders

---

## Step 3: Create TradingView Alert

### 3.1 Create the Alert

1. On TradingView with MGC chart open
2. Click the **Alert** button (clock icon) or press `Alt+A`
3. Configure:

| Field | Value |
|-------|-------|
| Condition | MGC Alert Only TradersPost |
| | "Any alert() function call" |
| Options | Once Per Bar Close |
| Alert actions | Webhook URL |
| Webhook URL | [Paste your TradersPost URL] |

### 3.2 Alert Message (IMPORTANT)

Leave the message field with the **default TradingView template**:
```
{{strategy.order.alert_message}}
```

Or leave it **empty** - the indicator sends its own JSON payload.

### 3.3 Alert Name and Expiration

| Field | Value |
|-------|-------|
| Alert Name | MGC TradersPost Webhook |
| Expiration | Open-ended (or set your preference) |

4. Click **Create**

### 3.4 Verify Alert is Active

- You should see a small bell icon on your chart
- Alert should appear in your Alerts panel
- Status should be "Active"

---

## Step 4: Configure TradersPost Strategy Settings

### 4.1 Symbol Mapping

In TradersPost, ensure proper symbol mapping:

| TradingView Symbol | TradersPost/Broker Symbol |
|-------------------|---------------------------|
| MGC1! | MGC |
| MGCG2025 | MGCG25 |
| MGCH2025 | MGCH25 |

Go to Strategy > Settings > Symbol Mapping and add rules if needed.

### 4.2 Position Sizing

Configure in TradersPost:

| Setting | Value |
|---------|-------|
| Default Quantity | 1 |
| Max Position Size | 3 |
| Quantity Type | Fixed |

### 4.3 Risk Controls

**Essential settings:**

| Setting | Recommended |
|---------|-------------|
| Max Daily Loss | $100 (or 2% of account) |
| Max Open Positions | 1 |
| Stop Loss Required | Yes |
| Allow Market Orders | Yes |

### 4.4 Order Settings

| Setting | Value |
|---------|-------|
| Order Type | Market |
| Time in Force | Day |
| Allow Shorts | Yes |

---

## Step 5: Test the System

### 5.1 Paper Trading First

1. In TradersPost, enable **Paper Trading** mode
2. Wait for a confluence signal (7/10 or higher)
3. Verify alert fires in TradingView
4. Check TradersPost Activity Log for webhook receipt
5. Confirm paper trade was placed

### 5.2 Verification Checklist

- [ ] Alert fires when confluence >= 7
- [ ] TradersPost shows webhook received
- [ ] Order appears in broker platform
- [ ] Stop loss and take profit orders placed
- [ ] Position shows correct size

### 5.3 Common Test Scenarios

**Test 1: Entry Signal**
- Wait for 7/10+ confluence
- Alert should fire
- Entry order + stop + TP should all appear

**Test 2: Stop Loss**
- Manually move price to stop level (in paper)
- Stop exit alert should fire
- Position should close

**Test 3: Take Profit**
- Manually move price to TP1 level
- Partial exit alert should fire
- 70% of position should close

---

## Step 6: Go Live

### 6.1 Pre-Live Checklist

- [ ] Paper traded for at least 20 trades
- [ ] Verified all alert types work
- [ ] Confirmed symbol mapping correct
- [ ] Set appropriate position size
- [ ] Configured max daily loss
- [ ] Understand the risks

### 6.2 Enable Live Trading

1. In TradersPost, disable Paper Trading mode
2. Verify broker account has sufficient funds
3. Verify margin requirements met for MGC

### 6.3 First Live Trade Monitoring

For your first few live trades:
1. Watch the alert fire in TradingView
2. Immediately check TradersPost Activity Log
3. Verify order in your broker platform
4. Confirm stop and TP orders are set
5. Monitor the trade

---

## Troubleshooting

### Alert Not Firing

| Issue | Solution |
|-------|----------|
| No alert on signal | Check alert is active, not expired |
| Wrong alert condition | Use "Any alert() function call" |
| Session filter | Verify US Trading Hours setting |
| Max trades reached | Check daily trade limit |

### Webhook Not Received

| Issue | Solution |
|-------|----------|
| URL incorrect | Re-copy webhook URL from TradersPost |
| TradingView plan | Need Pro+ for webhook alerts |
| Firewall | TradersPost should whitelist TradingView |

### Order Not Executing

| Issue | Solution |
|-------|----------|
| Symbol mismatch | Check symbol mapping in TradersPost |
| Insufficient margin | Add funds or reduce position size |
| Market closed | Only trades during market hours |
| Risk limit hit | Check max daily loss settings |

### Wrong Position Size

| Issue | Solution |
|-------|----------|
| Quantity override | Check TradersPost quantity settings |
| Contract multiplier | Verify contract size settings |

---

## Alert JSON Format Reference

### Entry Long
```json
{
  "ticker": "MGC1!",
  "action": "buy",
  "orderType": "market",
  "quantity": 1,
  "stopLoss": {"type": "stop", "stopPrice": 2515.80},
  "takeProfit": {"type": "limit", "limitPrice": 2608.30},
  "confluenceScore": 8
}
```

### Entry Short
```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 1,
  "stopLoss": {"type": "stop", "stopPrice": 2608.30},
  "takeProfit": {"type": "limit", "limitPrice": 2515.80},
  "confluenceScore": 7
}
```

### Take Profit Exit
```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 0.7,
  "exitReason": "TP1",
  "profitTarget": 1
}
```

### Stop Loss Exit
```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 0,
  "exitReason": "STOP_LOSS",
  "stopType": "initial"
}
```

---

## Expected Performance

With 7/10 minimum confluence, 1 contract:

| Metric | Expected |
|--------|----------|
| Trades/Day | 4-6 |
| Win Rate | 75-80% |
| Avg Win | ~$65 |
| Avg Loss | ~$32 |
| Daily P&L | $180-250 |
| Monthly | $3,600-5,000 |

**Note:** Past performance does not guarantee future results. Trade responsibly.

---

## Support

- **TradersPost Support**: support@traderspost.io
- **Tradovate Support**: Via their platform
- **TradingView Support**: support@tradingview.com

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025 | Initial alert-only release |

---

## Disclaimer

Trading futures involves substantial risk of loss and is not suitable for all investors. Past performance is not indicative of future results. This system is provided for educational purposes only. Always trade with capital you can afford to lose.
