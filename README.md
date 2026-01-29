# main

## Pine Script token-limit fix

If your script fails with `Compiled code contains too many tokens`, remove any
accidental error text appended to the last line, then strip comments/blank
lines to drop the token count.

Example cleanup:

- Before:
  `tookTradeThisBar := newTookTmp3:41:32 PM Compiled code contains too many tokens: 80005. The limit is 80000;`
- After:
  `tookTradeThisBar := newTookTmp`

Then compact the script:

```bash
python pine_compact.py path/to/input.pine -o path/to/output.pine
```