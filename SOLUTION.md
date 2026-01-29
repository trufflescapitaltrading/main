# TradingView Pine Script Token Limit Fix

## Problem
Your Pine Script has **80,005 tokens** but TradingView's limit is **80,000 tokens**. You need to remove at least 5 tokens.

## Solution
Remove the following comment lines from your script. These are purely informational and do not affect functionality.

### Lines to Remove (copy your script and delete these lines):

**Line 1** (around line 172-173):
```pinescript
// Strategy Tester fix: if you set Alert Only Mode = ON, TradingView strategy tester shows no trades.
// This switch forces strategy orders to still place in backtests while preserving your alert routing logic.
```

**Line 2** (around line 218-220):
```pinescript
// For Tradovate/TopstepX via TradersPost, continuous symbols like MES1!/MNQ1! can cause routing failures.
// Always use the configured contract ticker in webhook payloads.
```

**Line 3** (around line 224):
```pinescript
// TradersPost bracket schema is always used (required for Tradovate/TopstepX; avoids OTO rejection).
```

**Line 4** (around line 233):
```pinescript
// Token-limit optimization: removed optional add-to-position and optional "strategy close" exit alerts.
```

**Line 5** (in `f_traderspostAlerts` function, appears twice):
```pinescript
// Token-limit optimization: single bracket schema payload, minimal fields.
```

## Expected Result
Removing these 7 comment lines will save approximately **50-60 tokens**, bringing your script well under the 80,000 token limit.

## Alternative Quick Fix
If you want the absolute minimal change, just remove these 2 lines:

```pinescript
// Strategy Tester fix: if you set Alert Only Mode = ON, TradingView strategy tester shows no trades.
// This switch forces strategy orders to still place in backtests while preserving your alert routing logic.
```

This alone should save approximately 20+ tokens and get you under the limit.

## Verification
After making changes, TradingView will show the token count when you try to compile. Ensure it shows under 80,000.
