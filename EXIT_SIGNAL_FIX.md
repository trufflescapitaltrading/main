# TradersPost Exit Signal Rejection Fix

## Problem Summary

The strategy is sending "exit" signals to TradersPost when there's no position open at the broker, resulting in rejections like:

```
Trade Rejected
No MNQH2026 orders open to cancel.
No MNQH2026 position open to exit.
Cannot enter a new MNQH2026 position because the signal is an exit only signal.
```

## Root Causes Identified

### 1. Exit Alert Logic Uses Wrong State in Alert-Only Mode
The current code checks `strategy.position_size == 0 and strategy.position_size[1] != 0` to detect position close, but in `alertOnlyMode`, `strategy.position_size` is always 0 because no actual strategy trades are placed.

### 2. Simulated State Synchronization Issues
The simulated position tracking (`tpPosDir`, `tpPosBar`, `tpPosQty`) can get out of sync with the broker if:
- An entry is sent but rejected by the broker
- The strategy sends an exit based on simulated state, but broker has no position

### 3. Reverse Signal Exit Logic
The `tpExitOnReverseSignal` logic sends an exit before reversing direction, but this can fire when there's no actual position.

## Solution: Code Changes

Add these changes to your Pine Script strategy:

### Step 1: Add New Safety Input Parameters

Add this section after the existing TradersPost Router inputs (around line 500):

```pinescript
// ==================== 🔧 FIX: EXIT SIGNAL SAFETY ====================
exitSafetyGroup = "🔧 Exit Signal Safety (NEW)"
tpRequireConfirmedEntry = input.bool(true, "Only send EXIT if entry was confirmed sent", group=exitSafetyGroup)
tpExitCooldownBars = input.int(1, "Min bars after entry before sending EXIT", minval=0, maxval=10, group=exitSafetyGroup)
tpSuppressOrphanedExits = input.bool(true, "Suppress EXIT signals when no tracked position", group=exitSafetyGroup)
```

### Step 2: Add Entry Confirmation Tracking

Add these variables after the existing TradersPost state variables (around line 750):

```pinescript
// 🔧 FIX: Track whether we've actually sent an entry alert
var bool tpEntrySentConfirmed = false
var int tpLastEntrySentBar = na
```

### Step 3: Fix the Entry Alert Section

When sending entry alerts, set the confirmation flag. Update the long entry alert section (around line 1530):

```pinescript
if entryOK and longCondition and tpFlat and allowEntryLong and finalContractQty > 0 and enableTradersPostAlerts
    // ... existing entry message building code ...
    alert(longEntryMessage, enterOnBarClose ? alert.freq_once_per_bar_close : alert.freq_once_per_bar)
    if tpUseSim
        tpPosDir := 1
        tpPosBar := bar_index
        tpPosQty := finalContractQty
    // 🔧 FIX: Mark entry as confirmed sent
    tpEntrySentConfirmed := true
    tpLastEntrySentBar := bar_index
```

Do the same for short entry alerts.

### Step 4: Fix the Main Exit Alert Logic

Replace the existing exit alert section (around line 1650) with this fixed version:

```pinescript
// 🔧 FIXED: Exit alert logic that properly handles alert-only mode
// Use simulated state (tpPosDir) instead of strategy.position_size for alert-only mode
bool shouldSendExitAlert = false
int exitQty = 0
string exitDir = "FLAT"

if tpUseSim
    // In alert-only / simulated mode, check if simulated position just closed
    // This happens when strategy logic would close (EOD, SL/TP hit, reversal)
    bool simPosJustClosed = (tpPosDir != 0) and 
                            ((strategy.position_size == 0 and strategy.position_size[1] != 0) or
                             (useEndOfDayExits and isEndOfDay) or
                             exitIssuedThisBar)
    
    // Safety checks
    bool hasConfirmedEntry = not tpRequireConfirmedEntry or tpEntrySentConfirmed
    bool pastCooldown = not tpRequireConfirmedEntry or na(tpLastEntrySentBar) or (bar_index - tpLastEntrySentBar) >= tpExitCooldownBars
    bool notOrphaned = not tpSuppressOrphanedExits or tpPosDir != 0
    
    if simPosJustClosed and hasConfirmedEntry and pastCooldown and notOrphaned and enableTradersPostAlerts
        shouldSendExitAlert := true
        exitQty := tpPosQty
        exitDir := tpPosDir == 1 ? "LONG" : "SHORT"
else
    // Normal mode: use actual strategy position
    if strategy.position_size == 0 and strategy.position_size[1] != 0 and enableTradersPostAlerts
        shouldSendExitAlert := true
        exitQty := int(math.abs(strategy.position_size[1]))
        exitDir := strategy.position_size[1] > 0 ? "LONG" : "SHORT"

if shouldSendExitAlert and not tookTradeThisBar
    exitSigId = tpSignalId("exit", exitDir)
    exitMessage = '{' +
         '"ticker":"' + actualTicker + '",' +
         '"action":"exit",' +
         '"quantity":' + tpNumInt(exitQty) + ',' +
         '"strategy":"' + tpStrategyName + '",' +
         '"timeframe":"' + timeframe.period + '",' +
         '"instrument":"' + instrumentName + '",' +
         '"signal_id":"' + exitSigId + '",' +
         '"timestamp":"' + str.tostring(time) + '"' +
         '}'
    alert(exitMessage, alert.freq_once_per_bar)
    
    // Reset simulated state
    if tpUseSim
        tpPosDir := 0
        tpPosBar := bar_index
        tpPosQty := 0
        tpEntrySentConfirmed := false
        tpLastEntrySentBar := na
    
    tookTradeThisBar := true
```

### Step 5: Fix the Reverse Signal Exit Logic

Update the reverse signal exit section (around line 1490) with safety checks:

```pinescript
// 🔧 FIXED: Reverse signal exit with safety checks
if tpExitOnReverseSignal and enableTradersPostAlerts and entryOK and not tpFlat and not tookTradeThisBar
    // Additional safety: ensure we have a confirmed entry before sending exit
    bool canSendReverseExit = (not tpRequireConfirmedEntry or tpEntrySentConfirmed) and
                               (not tpSuppressOrphanedExits or tpPosDir != 0)
    
    if canSendReverseExit and ((longCondition and tpShort) or (shortCondition and tpLong))
        exitDir = tpShort ? "SHORT" : tpLong ? "LONG" : "FLAT"
        exitQty = tpQty
        exitSigId = tpSignalId("exit", exitDir)
        exitNowMessage = '{' +
             '"ticker":"' + actualTicker + '",' +
             '"action":"exit",' +
             '"quantity":' + tpNumInt(exitQty) + ',' +
             '"strategy":"' + tpStrategyName + '",' +
             '"timeframe":"' + timeframe.period + '",' +
             '"instrument":"' + instrumentName + '",' +
             '"signal_id":"' + exitSigId + '",' +
             '"timestamp":"' + str.tostring(time) + '"' +
             '}'
        alert(exitNowMessage, alert.freq_once_per_bar)
        if tpUseSim
            tpPosDir := 0
            tpPosBar := bar_index
            tpPosQty := 0
            tpEntrySentConfirmed := false
        tookTradeThisBar := true
```

### Step 6: Fix EOD Exit Logic

Update the EOD exit section with safety checks:

```pinescript
// 🔧 FIXED: EOD exit with safety checks
if tpSendEODExitAlert and useEndOfDayExits and isEndOfDay and enableTradersPostAlerts and tpUseSim and tpPosDir != 0 and not tookTradeThisBar
    // Safety check: only send if we have a confirmed entry
    bool canSendEODExit = (not tpRequireConfirmedEntry or tpEntrySentConfirmed) and
                          (not tpSuppressOrphanedExits or tpPosDir != 0)
    
    if canSendEODExit
        exitSigId = tpSignalId("exit", tpPosDir == 1 ? "LONG" : "SHORT")
        eodExitMessage = '{' +
             '"ticker":"' + actualTicker + '",' +
             '"action":"exit",' +
             '"quantity":' + tpNumInt(tpPosQty) + ',' +
             '"strategy":"' + tpStrategyName + '",' +
             '"timeframe":"' + timeframe.period + '",' +
             '"instrument":"' + instrumentName + '",' +
             '"signal_id":"' + exitSigId + '",' +
             '"timestamp":"' + str.tostring(time) + '"' +
             '}'
        alert(eodExitMessage, alert.freq_once_per_bar)
        tpPosDir := 0
        tpPosBar := bar_index
        tpPosQty := 0
        tpEntrySentConfirmed := false
        tookTradeThisBar := true
```

## Alternative Quick Fix

If you want a simpler fix without modifying too much code, you can:

1. **Disable exit-on-reverse-signal**: Set `tpExitOnReverseSignal = false` in the TradersPost Router settings

2. **Disable alert-only simulated position**: Set `tpSimulateBrokerPosition = false` 

3. **Use TradersPost's built-in position management**: Configure TradersPost webhook to handle position reconciliation

## Testing the Fix

After applying the fix:

1. Set the strategy to Alert Only Mode
2. Watch for entry signals - verify they fire correctly
3. Wait for exit conditions - verify exits only fire when an entry was previously sent
4. Check TradersPost logs for any remaining rejections

## Why This Happens

The original code sends exit alerts based on `strategy.position_size` transitions, but:

1. In Alert Only Mode, `strategy.position_size` is always 0 (no actual trades)
2. The simulated state (`tpPosDir`) was updated when entries were *sent*, but the broker might have rejected them
3. When the strategy tries to exit, it sends an exit signal for a position that never existed at the broker

The fix ensures:
- Exit signals only fire if an entry was confirmed as sent (`tpEntrySentConfirmed`)
- A minimum cooldown between entry and exit (`tpExitCooldownBars`)
- Exit signals are suppressed if no tracked position exists (`tpSuppressOrphanedExits`)
