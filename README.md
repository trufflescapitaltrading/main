# TradersPost Exit Signal Fix for MNQ/MES 5-Star Scalper Strategy

## Problem

The strategy was sending "exit" signals to TradersPost when there was no position open at the broker, resulting in rejections:

```
Trade Rejected
No MNQH2026 orders open to cancel.
No MNQH2026 position open to exit.
Cannot enter a new MNQH2026 position because the signal is an exit only signal.
```

## Solution

This repository contains the fix for the exit signal synchronization issue.

### Files

- `EXIT_SIGNAL_FIX.md` - Detailed documentation of the fix with code snippets to apply to your existing strategy
- `MNQ_5Star_Scalper_V71_EXIT_FIX.pine` - Simplified Pine Script demonstrating the fixed exit signal logic

### Key Changes

1. **Entry Confirmation Tracking**: Added `tpEntrySentConfirmed` flag to track whether an entry alert was actually sent
2. **Exit Cooldown**: Added minimum bar count between entry and exit to prevent immediate spurious exits
3. **Orphaned Exit Suppression**: Exit signals are only sent if a tracked position exists
4. **Proper State Reset**: When exits are sent, all tracking variables are properly reset

### New Input Parameters

```
🔧 Exit Signal Safety (FIX)
├── Only send EXIT if entry was confirmed sent (default: true)
├── Min bars after entry before sending EXIT (default: 1)
└── Suppress EXIT signals when no tracked position (default: true)
```

## How to Apply

### Option 1: Use the provided Pine Script
Copy the code from `MNQ_5Star_Scalper_V71_EXIT_FIX.pine` and adapt it to your full strategy.

### Option 2: Apply the patches manually
Follow the instructions in `EXIT_SIGNAL_FIX.md` to add the fix to your existing strategy.

### Option 3: Quick workaround
If you need an immediate fix without code changes:
- Set `tpExitOnReverseSignal = false` in TradersPost Router settings
- Set `tpSimulateBrokerPosition = false`

## Root Cause Analysis

The original code sent exit alerts based on `strategy.position_size` transitions, but:

1. In Alert Only Mode, `strategy.position_size` is always 0 (no actual trades)
2. The simulated state (`tpPosDir`) was updated when entries were *sent*, but the broker might have rejected them
3. When the strategy tried to exit, it sent exit signals for positions that never existed at the broker

The fix ensures:
- Exit signals only fire if an entry was confirmed as sent
- A minimum cooldown between entry and exit
- Exit signals are suppressed if no tracked position exists