# LuxAlgo Upstox NIFTY Options Bot

Production-grade automated trading bot for **NIFTY 50 options** using Upstox API.

It implements two complementary strategies on **3-minute candles**:

1. **Trendline Breakouts** (LuxAlgo-style "B" labels)
2. **Support & Resistance Bounces** (mean-reversion)

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

Both repositories now use the **same GitHub secret name**:

| Priority | Source |
|----------|--------|
| 1 | `UPSTOX_TOKEN` (GitHub secret / preferred) |
| 2 | `UPSTOX_ACCESS_TOKEN` (legacy env var) |
| 3 | `--token` CLI flag |

### Add the secret once

1. Go to **Settings → Secrets and variables → Actions** in this repo  
   (or in the Final repo — same secret name works for both)
2. Create / update secret named **`UPSTOX_TOKEN`**
3. Paste your fresh Upstox access token

---

## Quick Start

### Local run

```bash
export UPSTOX_TOKEN="your_token_here"   # preferred
# or: export UPSTOX_ACCESS_TOKEN="your_token_here"

python luxalgo_upstox_production.py --mode paper   # test first
python luxalgo_upstox_production.py --mode live --qty 65
```

### GitHub Actions (recommended)

1. Ensure secret `UPSTOX_TOKEN` is set
2. Go to **Actions → LuxAlgo NIFTY Bot → Run workflow**
3. Choose `paper` or `live` and quantity

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
| `.github/workflows/luxalgo_nifty.yml` | GitHub Actions runner |
| `bot_state.json` | Runtime position & trade counter (auto-created) |
| `luxalgo_live_production.log` | Log file |
| `requirements.txt` | Dependencies |

---

## Disclaimer

This is experimental software for educational purposes. Trading options involves substantial risk of loss. Use at your own risk. The author is not responsible for any financial losses.
