## Trading bot Pine scripts (MNQ/MES 3m/5m)

This repo now contains the full TradingView Pine strategy script and a smaller patch file focused on fixing **late trade firing / wrong candle color entries**.

- **Full bot**: `pine/@MAIN-MNQ_3m5m_BOT_V71_FIXED.pine`
- **Patch-only reference**: `pine/TRADE_FIRING_FIX_PATCH.pine`

### What was fixed (core causes of your symptoms)

- **Late entries / “wrong candle color” entries**: enforced **bar-close fills** by using `process_orders_on_close=true` and a corrected **entry gating** model (bar-close only when enabled; intrabar only when explicitly enabled).
- **Missing the start of trends**: added **early trend-start entry priorities** that can fire on candle 1–2 instead of candle 4–5:
  - `P1:FLIP` (SuperTrend flip)
  - `P1:EMA_CROSS` (EMA9/EMA21 cross)
  - `P1:DI_CROSS` (ADX/DI ignition)
  - `P1:BREAKOUT` (Donchian breakout)
- **Doji/opposite-color misfires**: early-entry priorities are guarded by `isDojiBar` + `candleQualityOK` + minimum body ratio.

### Live trading notes

- If you want **signals that do not repaint intrabar**, keep `Enter ONLY on bar close` enabled.
- If you intentionally enable intrabar entries, **expect occasional “color mismatch by close”** in realtime (that is inherent to intrabar logic).

### Debugging missed trades

Turn on `Show debug labels (blocked entries + priorities)` to print:
- **BLOCKED:** why a signal did *not* become an entry (time window, HTF/MTF filters, candle confirm, etc.)
- **ENTRY:** which priority actually fired (P-1/P1/P2 label)
