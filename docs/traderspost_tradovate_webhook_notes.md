## TradersPost → Tradovate webhook notes (practical)

This is not official documentation. It’s a **deployment sanity checklist** meant to prevent the exact failures you reported (missing SL orders, “wrong unit” stops, and catastrophic market slippage).

### 1) Decide what you want to control with the webhook

- **Entry slippage control**
  - Best control: **`limit`** entry (may miss trades)
  - Balanced: **`stop_limit`** entry (caps worst fill but can still miss trades if limit too tight)
  - Worst control: **`market`** entry (fills fast, can slip badly)

- **Stop-loss reliability**
  - Best: broker-native bracket orders created at entry
  - Risky: “exit on alert” (market exits can slip, and alerts can fail)

### 2) Pick ONE stop/TP interpretation and enforce it

Some automations accept:

- Price-based: `stop_loss`, `take_profit`
- Dollar-based: `stop_loss_amount`, `take_profit_amount`

If the platform interprets `*_amount` incorrectly (ticks vs dollars vs points), it can place extremely tight stops (e.g., a few points) even though your Pine logic “expected” a wide ATR stop.

### 3) Validate with a single live test

Do a one-contract, one-trade test in a quiet period and verify:

- Entry order type in Tradovate matches what you intended (market/limit/stop-limit)
- A **real stop order exists immediately** after entry
- The stop price equals the JSON `stop_loss` (or corresponds exactly to your `stop_loss_amount` if you use amount mode)

### 4) Deduplication / race conditions

If you have multiple bots or multiple alerts on the same symbol:

- Ensure only one can fire per bar (TradingView alert frequency + bot cooldown)
- Use a unique `signal_id`/`client_order_id` and configure TradersPost to dedupe if possible

### 5) If you still see “132 points in 2 seconds”

That pattern is usually one of:

- **Wrong symbol/contract mapping** (continuous vs a specific contract, or micro vs mini)
- **Market orders during a gap/volatility burst**
- **Stop-limit too loose** (effectively behaves like market in fast moves)
- **Your alert is on bar close but the broker is using a later time** (latency + fast move)

