import unittest
from datetime import datetime, timedelta

from luxalgo_upstox_production import Resampler


class ResamplerTests(unittest.TestCase):
    def test_emits_ohlc_bar_after_interval(self):
        start = datetime(2026, 11, 16, 9, 15)
        resampler = Resampler(interval_sec=180, raw_candles=[])

        # 9 ticks inside the first 3-minute bar (0s .. 160s)
        prices = [100.0, 102.0, 99.0, 101.0, 103.0, 100.0, 102.0, 101.0, 104.0]
        for i, price in enumerate(prices):
            emitted = resampler.on_tick(start + timedelta(seconds=20 * i), price)
            self.assertIsNone(emitted)

        # First tick of the next bar closes the previous one
        emitted = resampler.on_tick(start + timedelta(seconds=180), 98.0)
        self.assertIsNotNone(emitted)
        self.assertEqual(emitted["time"], start)
        self.assertEqual(emitted["open"], 100.0)
        self.assertEqual(emitted["high"], 104.0)
        self.assertEqual(emitted["low"], 99.0)
        self.assertEqual(emitted["close"], 104.0)
        self.assertFalse(emitted["stale"])

    def test_marks_bar_stale_after_long_tick_gap(self):
        start = datetime(2026, 11, 16, 9, 15)
        resampler = Resampler(interval_sec=180, raw_candles=[])
        resampler.on_tick(start, 100.0)
        resampler.on_tick(start + timedelta(seconds=31), 101.0)

        emitted = resampler.on_tick(start + timedelta(seconds=180), 102.0)
        self.assertIsNotNone(emitted)
        self.assertTrue(emitted["stale"])

    def test_seeds_and_aggregates_one_minute_candles(self):
        start = datetime(2026, 11, 16, 9, 15)
        raw = [
            {"time": start, "open": 100, "high": 103, "low": 99, "close": 102},
            {"time": start + timedelta(minutes=1), "open": 102, "high": 105, "low": 101, "close": 104},
            {"time": start + timedelta(minutes=2), "open": 104, "high": 106, "low": 100, "close": 101},
        ]

        resampler = Resampler(interval_sec=180, raw_candles=raw)
        self.assertEqual(len(resampler.candles), 1)
        self.assertEqual(resampler.candles[0], {
            "time": start,
            "open": 100,
            "high": 106,
            "low": 99,
            "close": 101,
        })


if __name__ == "__main__":
    unittest.main()
