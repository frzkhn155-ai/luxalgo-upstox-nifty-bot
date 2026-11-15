# LuxAlgo Upstox NIFTY Options Bot

Automated trading bot for **NIFTY 50 options** using Upstox API.

It implements two complementary strategies on **3-minute candles**:

1. **Trendline Breakouts** (LuxAlgo-style "B" labels)
2. **Support & Resistance Bounces** (mean-reversion)

> **Important:** This repository provides a **local / manual runner**.  
> GitHub Actions is intended for testing and short paper sessions only —  
> **not** a reliable always-on production host. For real trading, run the  
> script on a persistent machine (VPS, home server, Termux with wake-lock, etc.).

---

## Features

- Real-time 1-minute tick → 3-minute bar resampling
- Closed-bar signal evaluation (bounce strategies work correctly)
- Dynamic ATR-based trendlines + support/resistance detection
- ATM CE / PE selection
- Marketable limit orders with progressive slippage on exits
- Order fill verification + partial fill handling
- Breakeven + trailing stop management
- Force exit at 15:15 IST
- State persistence (`bot_state.json`) — survives restarts
- Stale-bar protection (data gaps > 30s ignored for entries)
- Paper trading mode
- Heartbeat logging every 30 seconds
- Unit tests for resampling logic

---

## Requirements

- Python 3.10+
- Upstox account + API access token
- `requests` library

```bash
pip install -r requirements.txt
```

---

## Token Setup (same secret name as Final repo)

| Priority | Source |
|----------|--------|
| 1 | `UPSTOX_TOKEN` (GitHub secret / preferred) |
| 2 | `UPSTOX_ACCESS_TOKEN` (legacy env var) |
| 3 | `--token` CLI flag |

### Add the secret

1. Go to **Settings → Secrets and variables → Actions** in **this** repo
2. Create / update secret named **`UPSTOX_TOKEN`**
3. Paste your fresh Upstox access token

> Note: GitHub secrets are **per-repository**. Setting the secret only in the Final repo does **not** make it available here.

---

## Quick Start

### Local run (recommended for real use)

```bash
export UPSTOX_TOKEN="your_token_here"

python luxalgo_upstox_production.py --mode paper   # test first
python luxalgo_upstox_production.py --mode live --qty 65
```

### GitHub Actions (manual test runner only)

1. Ensure secret `UPSTOX_TOKEN` is set in **this** repo
2. Go to **Actions → LuxAlgo NIFTY Bot → Run workflow**
3. Choose `paper` or `live` and quantity

Logs are uploaded as workflow artifacts (not committed back to the repo).

---

## Running tests

```bash
python -m unittest discover -s tests -v
```

Unit tests cover the `Resampler` (OHLC aggregation and stale-gap detection).  
They do **not** test live broker connectivity, order execution, or strategy profitability.

---

## Command-line Options

| Argument | Default | Description |
|----------|---------|-------------|
| `--interval` | 3 | Candle interval in minutes |
| `--length` | 14 | Pivot lookback period |
| `--mode` | live | `paper` or `live` |
| `--qty` | 65 | Quantity (NIFTY lot size) |
| `--sl` | 15.0 | Initial stop-loss % |
| `--be-at` | 6.0 | Move SL to breakeven at +X% |
| `--trail-at` | 8.0 | Start trailing at +X% |
| `--giveback` | 20.0 | Trailing giveback % |
| `--fill-timeout` | 8 | Seconds to wait for order fill |
| `--token` | (env) | Upstox access token |

---

## Important Safety Notes

- **Never commit your real access token** to the repository.
- Always test thoroughly in `--mode paper` first.
- The bot uses product type `"D"` (Delivery/Normal) to avoid MIS restrictions.
- Force-exit runs at **15:15 IST** regardless of spot feed status.
- On ambiguous order state the bot **halts** and requires manual inspection.
- GitHub Actions is **not** a production host — use a persistent machine for live trading.

---

## Termux / Android Tips

```bash
termux-wake-lock
# Also disable battery optimization for Termux in Android settings
```

---

## Files

| File | Purpose |
|------|---------|
| `luxalgo_upstox_production.py` | Main bot |
| `tests/test_resampler.py` | Unit tests for bar resampling |
| `.github/workflows/luxalgo_nifty.yml` | Manual GitHub Actions runner |
| `bot_state.json` | Runtime position & trade counter (auto-created) |
| `luxalgo_live_production.log` | Log file |
| `requirements.txt` | Dependencies |
| `.env.example` | Token template |

---

## Disclaimer

This is experimental software for educational purposes. Trading options involves substantial risk of loss. Use at your own risk. The author is not responsible for any financial losses.
