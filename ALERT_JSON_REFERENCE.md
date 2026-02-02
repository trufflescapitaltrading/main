# Alert JSON Reference for MGC Alert-Only System

## Complete Technical Documentation for TradersPost Webhook Integration

---

## Overview

This document provides complete technical specifications for all JSON alert formats sent by the MGC Alert-Only indicator to TradersPost.

**Alert Types:**
1. Entry Alerts (Long/Short)
2. Take Profit Exits (TP1, TP2, TP3)
3. Stop Loss Updates (Breakeven, Trailing)
4. Stop Loss Exits
5. Manual Flatten

---

## Entry Alerts

### Long Entry

Sent when confluence score >= minimum threshold and all conditions met.

```json
{
  "ticker": "MGC1!",
  "action": "buy",
  "orderType": "market",
  "quantity": 1,
  "stopLoss": {
    "type": "stop",
    "stopPrice": 2515.80
  },
  "takeProfit": {
    "type": "limit",
    "limitPrice": 2608.30
  },
  "confluenceScore": 8
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| ticker | string | Symbol for TradersPost routing |
| action | string | "buy" for long entry |
| orderType | string | "market" for immediate execution |
| quantity | integer | Number of contracts |
| stopLoss.type | string | "stop" for stop-market order |
| stopLoss.stopPrice | float | Initial stop loss price |
| takeProfit.type | string | "limit" for limit order |
| takeProfit.limitPrice | float | TP1 target price |
| confluenceScore | integer | Score that triggered entry (7-10) |

### Short Entry

```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 1,
  "stopLoss": {
    "type": "stop",
    "stopPrice": 2608.30
  },
  "takeProfit": {
    "type": "limit",
    "limitPrice": 2515.80
  },
  "confluenceScore": 7
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| action | string | "sell" for short entry |
| stopLoss.stopPrice | float | Stop above entry for shorts |
| takeProfit.limitPrice | float | TP below entry for shorts |

---

## Take Profit Exit Alerts

### TP1 Exit (70% of position)

Sent when price reaches TP1 level (2.5 ATR from entry).

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

**For short positions:**
```json
{
  "ticker": "MGC1!",
  "action": "buy",
  "orderType": "market",
  "quantity": 0.7,
  "exitReason": "TP1",
  "profitTarget": 1
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| action | string | Opposite of position direction |
| quantity | float | 0.7 = 70% of original position |
| exitReason | string | "TP1" identifies the exit type |
| profitTarget | integer | 1 = first take profit level |

### TP2 Exit (25% of position)

Sent when price reaches TP2 level (4.0 ATR from entry).

```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 0.25,
  "exitReason": "TP2",
  "profitTarget": 2
}
```

**Note:** Quantity is calculated as 25% of remaining position after TP1.

### TP3 Exit (Final 5% - Flatten)

Sent when price reaches TP3 level (6.0 ATR from entry).

```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 0,
  "exitReason": "TP3_FLATTEN",
  "profitTarget": 3
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| quantity | integer | 0 = flatten/close all remaining |
| exitReason | string | "TP3_FLATTEN" = final exit |

---

## Stop Loss Update Alerts

### Breakeven Stop Update

Sent when profit reaches breakeven trigger (1.5 ATR).

```json
{
  "ticker": "MGC1!",
  "action": "update_stop",
  "stopLoss": {
    "type": "stop",
    "stopPrice": 2550.02
  },
  "reason": "breakeven"
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| action | string | "update_stop" for stop modification |
| stopLoss.stopPrice | float | New stop at entry + tiny buffer |
| reason | string | "breakeven" identifies update type |

### Trailing Stop Update

Sent when trailing stop activates (3.0 ATR profit) and price moves.

```json
{
  "ticker": "MGC1!",
  "action": "update_stop",
  "stopLoss": {
    "type": "trailing_stop",
    "stopPrice": 2565.50
  },
  "reason": "trailing"
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| stopLoss.type | string | "trailing_stop" for trail type |
| reason | string | "trailing" identifies update type |

---

## Stop Loss Exit Alerts

### Initial Stop Hit

Sent when price hits initial stop loss.

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

### Breakeven Stop Hit

Sent when price returns and hits breakeven stop.

```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 0,
  "exitReason": "STOP_LOSS",
  "stopType": "breakeven"
}
```

### Trailing Stop Hit

Sent when price reverses and hits trailing stop.

```json
{
  "ticker": "MGC1!",
  "action": "sell",
  "orderType": "market",
  "quantity": 0,
  "exitReason": "STOP_LOSS",
  "stopType": "trailing"
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| quantity | integer | 0 = close entire remaining position |
| exitReason | string | "STOP_LOSS" for stop exits |
| stopType | string | "initial", "breakeven", or "trailing" |

---

## Manual Flatten Alert

Sent when user toggles the FLATTEN ALL POSITIONS input.

```json
{
  "ticker": "MGC1!",
  "action": "exit",
  "orderType": "market",
  "quantity": 0,
  "exitReason": "MANUAL_FLATTEN"
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| action | string | "exit" for manual close |
| quantity | integer | 0 = flatten all |
| exitReason | string | "MANUAL_FLATTEN" for manual exit |

---

## TradersPost Action Mapping

### Supported Actions

| JSON Action | TradersPost Interpretation |
|-------------|---------------------------|
| "buy" | Open long or close short |
| "sell" | Open short or close long |
| "exit" | Close position |
| "update_stop" | Modify stop order |

### Quantity Handling

| Quantity Value | Behavior |
|----------------|----------|
| Integer > 0 | Exact contracts |
| Float 0-1 | Percentage of position |
| 0 | Close entire position |

---

## Alert Frequency

### Expected Daily Alerts

| Alert Type | Frequency |
|------------|-----------|
| Entry | 4-6 per day |
| TP1 | 3-5 per day |
| TP2 | 2-3 per day |
| TP3 | 1-2 per day |
| Stop Updates | 5-10 per day |
| Stop Exits | 1-2 per day |

**Total: ~15-25 alerts per day** for a typical session.

---

## TradingView Alert Configuration

### Recommended Settings

| Setting | Value |
|---------|-------|
| Condition | "Any alert() function call" |
| Frequency | "Once Per Bar Close" |
| Webhook URL | Your TradersPost URL |
| Message | Leave default or empty |

### Alert Frequency Options

| Option | Behavior | Recommended |
|--------|----------|-------------|
| Once Per Bar Close | Fires at bar close | Yes |
| Once Per Bar | Fires on first trigger | No |
| Every Time | Can cause duplicates | No |

---

## Common Issues and Solutions

### Issue: Duplicate Orders

**Cause:** Alert firing multiple times
**Solution:** Use "Once Per Bar Close" frequency

### Issue: Wrong Symbol

**Cause:** Symbol mapping mismatch
**Solution:** Configure symbol mapping in TradersPost:
```
MGC1! → MGC
MGCG2025 → MGCG25
```

### Issue: Stop Not Updating

**Cause:** TradersPost not receiving update_stop
**Solution:** Some brokers don't support stop modification via API. Configure bracket orders instead.

### Issue: Partial Exit Not Working

**Cause:** Broker doesn't support fractional contracts
**Solution:** Use integer quantities or configure TradersPost to round.

### Issue: Alert Not Firing

**Cause:** Session filter or max trades reached
**Solution:** Check:
- US Trading Hours setting
- Daily trade limit
- Confluence score threshold

---

## Testing Alerts

### Manual Test Method

1. In TradingView, right-click the indicator
2. Click "Send Test Alert"
3. Check TradersPost Activity Log
4. Verify webhook received

### Paper Trade Test

1. Enable Paper Trading in TradersPost
2. Wait for real signal
3. Verify full flow works
4. Test all exit scenarios

### Webhook Testing Tools

- **Webhook.site**: Free webhook testing
- **RequestBin**: Alternative testing tool
- **TradersPost Logs**: Built-in activity log

---

## Price Calculation Reference

### Stop Loss Prices

| Position | Formula |
|----------|---------|
| Long Initial | Entry - (ATR × 1.2) |
| Short Initial | Entry + (ATR × 1.2) |
| Breakeven | Entry ± (2 × mintick) |
| Trailing | Current - (ATR × 1.5) |

### Take Profit Prices

| Level | Formula |
|-------|---------|
| TP1 Long | Entry + (ATR × 2.5) |
| TP1 Short | Entry - (ATR × 2.5) |
| TP2 Long | Entry + (ATR × 4.0) |
| TP2 Short | Entry - (ATR × 4.0) |
| TP3 Long | Entry + (ATR × 6.0) |
| TP3 Short | Entry - (ATR × 6.0) |

---

## JSON Validation

### Required Fields by Alert Type

| Alert Type | Required Fields |
|------------|-----------------|
| Entry | ticker, action, orderType, quantity, stopLoss, takeProfit |
| TP Exit | ticker, action, orderType, quantity, exitReason |
| Stop Update | ticker, action, stopLoss, reason |
| Stop Exit | ticker, action, orderType, quantity, exitReason, stopType |
| Flatten | ticker, action, orderType, quantity, exitReason |

### JSON Schema (Entry)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["ticker", "action", "orderType", "quantity"],
  "properties": {
    "ticker": {"type": "string"},
    "action": {"enum": ["buy", "sell", "exit", "update_stop"]},
    "orderType": {"enum": ["market", "limit", "stop"]},
    "quantity": {"type": "number", "minimum": 0},
    "stopLoss": {
      "type": "object",
      "properties": {
        "type": {"type": "string"},
        "stopPrice": {"type": "number"}
      }
    },
    "takeProfit": {
      "type": "object",
      "properties": {
        "type": {"type": "string"},
        "limitPrice": {"type": "number"}
      }
    }
  }
}
```

---

## Version Compatibility

| System | Version | Compatibility |
|--------|---------|---------------|
| TradingView | Pine Script v5 | Full |
| TradersPost | Current API | Full |
| Tradovate | REST API v1 | Full |
| TopstepX | Via TradersPost | Full |

---

## Support Contacts

- **TradersPost**: support@traderspost.io
- **Documentation**: docs.traderspost.io
- **API Reference**: api.traderspost.io

---

## Changelog

| Version | Changes |
|---------|---------|
| 1.0 | Initial alert-only system release |
