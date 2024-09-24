"""Binance exchange subclass"""

import logging
from typing import List, Tuple

from freqtrade.enums import MarginMode, TradingMode
from freqtrade.exchange import Exchange


logger = logging.getLogger(__name__)


class Deribit(Exchange):
    _supported_trading_mode_margin_pairs: List[Tuple[TradingMode, MarginMode]] = [
        # TradingMode.SPOT always supported and not required in this list
        # (TradingMode.MARGIN, MarginMode.CROSS),
        # (TradingMode.FUTURES, MarginMode.CROSS),
        (TradingMode.FUTURES, MarginMode.ISOLATED)
    ]
