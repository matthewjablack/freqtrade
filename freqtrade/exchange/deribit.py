"""Binance exchange subclass"""

import logging
from typing import List, Optional, Tuple

from freqtrade.enums import MarginMode, TradingMode
from freqtrade.exchange import Exchange
from freqtrade.exchange.types import Tickers


logger = logging.getLogger(__name__)


class Deribit(Exchange):
    _supported_trading_mode_margin_pairs: List[Tuple[TradingMode, MarginMode]] = [
        # TradingMode.SPOT always supported and not required in this list
        # (TradingMode.MARGIN, MarginMode.CROSS),
        # (TradingMode.FUTURES, MarginMode.CROSS),
        (TradingMode.FUTURES, MarginMode.ISOLATED)
    ]

    def get_tickers(self, symbols: Optional[List[str]] = None, cached: bool = False) -> Tickers:
        """
        :param symbols: List of symbols to fetch
        :param cached: Allow cached result
        :return: fetch_tickers result
        """
        tickers: Tickers = {}
        if cached:
            with self._cache_lock:
                tickers = self._fetch_tickers_cache.get("fetch_tickers")  # type: ignore
            if tickers:
                return tickers

        if not symbols:
            # If no symbols provided, use all available pairs
            symbols = list(self.markets.keys())

        for symbol in symbols:
            # Filter out complex instruments and options
            if "_" in symbol or symbol.endswith(("-C", "-P")):
                continue
            try:
                currency = symbol.split("/")[0]
                ticker_symbol = symbol if ":" in symbol else currency
                ticker = self._api.fetch_ticker(ticker_symbol, params={"currency": currency})
                tickers[symbol] = ticker
            except Exception as e:
                logger.warning(f"Could not fetch ticker for {symbol}: {e}")

        with self._cache_lock:
            self._fetch_tickers_cache["fetch_tickers"] = tickers

        return tickers
