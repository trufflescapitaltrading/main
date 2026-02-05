# RUN V14.1 Strategy (TradingView Pine v5)

This repository contains a Pine v5 strategy intended for TradingView alerts routed to
TradersPost/Tradovate/TopstepX. The script is **alert-first**: alerts are the only
automation signal, while `strategy.*` calls exist solely for state tracking and
backtesting.

## Files

- `strategy.pine` — the full strategy with alert JSON, regime gating, MTF confirmation,
  slippage controls, and post-breakeven trailing stops.

## Recommended Live Setup (Alert-Only Automation)

1. Add `strategy.pine` to a TradingView chart.
2. In the Inputs:
   - **Enable TradersPost Alerts**: ON
   - **Enable Strategy Orders (state/backtest)**: ON  
     (required to keep internal position state so exit alerts fire)
   - **Alert Entry Order Type**: `Limit`
   - **Entry Limit Offset (ticks)**: 1–3
   - **Max Entry Slippage (ticks)**: 4–10
   - **Stop/Trail Slippage Buffer (ticks)**: 1–3
   - **Require Trend/Continuation Regime**: ON
   - **Allow Breakout Trades in Range**: ON
   - **MTF Mode**: `Confirmation`
   - **Enable Multi-Timeframe Checks**: ON
3. Create a TradingView alert with:
   - Condition: **Any alert() function call**
   - Webhook URL: your TradersPost endpoint
4. In TradersPost, confirm that it maps:
   - `stop_loss`, `take_profit`
   - `stop_loss_amount`, `take_profit_amount`
   - `order_type`, `limit_price`

## Notes on Risk & Expectations

- **No strategy can guarantee 80% win rates or $1500/day**.  
  Actual results depend on market regime, liquidity, slippage, data feed,
  instrument, broker execution, and routing.
- Use **backtests + forward tests** on each instrument/timeframe to estimate
  expected trades/day, win rate, and PnL. This must be done on your own data.

## Perfect Trade Setup (Qualitative Guide)

The strategy is tuned to favor:

- **Trend or continuation regimes**
- **Momentum alignment across MTFs**
- **Volume confirmation**
- **Breakout/impulse trades** when the market is otherwise ranging

Avoid:

- Sideways/ranging conditions with weak volume
- Signal conflicts (long/short at the same time)
- Sessions outside your configured windows

## Troubleshooting Execution Issues

If you see large slippage or stops not triggering:

1. Verify TradersPost is receiving and applying `stop_loss`/`take_profit` fields.
2. Check if orders are sent as **Market** instead of **Limit**.
3. Confirm Tradovate is placing **Stop** (not Stop-Limit) unless intentionally set.
4. Review order logs for rejected stop orders.

## Disclaimer

This strategy is for research and educational use only. Trading futures carries
significant risk. Always test thoroughly and consult your broker’s execution
specifications.