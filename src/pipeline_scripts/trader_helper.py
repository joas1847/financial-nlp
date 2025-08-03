from datetime import datetime, timezone, timedelta
from typing import Literal

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.requests import LimitOrderRequest
from alpaca.data.requests import StockBarsRequest, CryptoBarsRequest
from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit


class AlpacaTrader:
    """
    A unified trader for stocks and crypto with threshold-based limit orders.
    Exposes `client` for direct TradingClient method access.
    """
    _unit_map = {
        "Min":  TimeFrameUnit.Minute,
        "Hour": TimeFrameUnit.Hour,
        "Day":  TimeFrameUnit.Day,
        "Week": TimeFrameUnit.Week,
        "Month": TimeFrameUnit.Month,
    }
    _delta_map = {
        "Min":   "minutes",
        "Hour":  "hours",
        "Day":   "days",
        "Week":  "weeks",
        "Month": "months",
    }

    def __init__(
        self,
        api_key: str,
        secret_key: str
    ):
        # Initializing the trader with API credentials.
        self.trading_client = TradingClient(api_key=api_key, secret_key=secret_key)
        self.stock_data_client = StockHistoricalDataClient(api_key=api_key, secret_key=secret_key)
        self.crypto_data_client = CryptoHistoricalDataClient(api_key=api_key, secret_key=secret_key)

    def execute_action(
        self,
        symbol: str,
        action: str,
        qty: float = 1.0,
        threshold_pct: float = 5.0,
        timeframe_unit: Literal["Min","Hour","Day","Week"] = "Hour",
        limit: int = None,
        asset_type: Literal["stock","crypto"] = "stock",       
    ) -> None:
        """
        Buys `qty` of `symbol` (stock or crypto) if price relies in the treshold specified by the user

        Args:
            symbol:           e.g. "AAPL" or "ETH/USD"
            qty:              shares or units
            threshold_pct:    max % above/below mean before aborting
            timeframe_unit:   one of "Min","Hour","Day","Week"
            limit:            number of time units to check 
            asset_type:       "stock" or "crypto"
        """
        if action.upper() == "HOLD":
            print(f"Holding {symbol} (no action taken).")
            return
   
        unit_enum = self._unit_map.get(timeframe_unit)
        delta_arg = self._delta_map.get(timeframe_unit)
        if timeframe_unit=="Min":
            start = datetime.now(timezone.utc) - timedelta(**{delta_arg: limit+2})
        else:
            start = datetime.now(timezone.utc) - timedelta(**{delta_arg: limit})

        # Choose client & request class
        if asset_type.lower() == "crypto":
            data_client = self.crypto_data_client
            query_data = CryptoBarsRequest(
                                    symbol_or_symbols=symbol,
                                    timeframe=TimeFrame(amount=1, unit=unit_enum),
                                    start=start,
                                    limit=limit)
            data = data_client.get_crypto_bars(query_data)

        else:
            data_client = self.stock_data_client
            try:
                query_data = StockBarsRequest(
                                        symbol_or_symbols=symbol,
                                        timeframe=TimeFrame(amount=1, unit=unit_enum),
                                        start=start,
                                        limit=limit)
                data = data_client.get_stock_bars(query_data)

                if len(data[symbol]) == 0:
                    print(f"No data found for {symbol} in the last {limit} {timeframe_unit.lower()}s. Market closed")
                    pass
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}, market closed")
                pass
        
                    
        bars = data[symbol]
        mean_price = sum(bar.close for bar in bars) / len(bars)
        last_bar   = bars[-1]
        latest_price = last_bar.close
        
        print(f"Latest price for {symbol} is {latest_price:.2f} (mean {mean_price:.2f})")
        
        ceiling = mean_price * (1 + threshold_pct / 100)
        floor = mean_price * (1 - threshold_pct / 100)

        if action == "BUY" and latest_price <= ceiling:
            side = OrderSide.BUY
            limit_price = ceiling
        
        elif action == "SELL" and latest_price >= floor:
            side = OrderSide.SELL
            limit_price = floor
            # qty = int(qty)
        else:
            print("No action taken, outside your price threshold, try to adjust the limit or market already moved.")
            return
        
        tif = TimeInForce.DAY if asset_type == "stock" else TimeInForce.GTC

        order_data = LimitOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    type=OrderType.LIMIT,
                    time_in_force=tif,
                    limit_price=round(limit_price,2),
                )

        self.trading_client.submit_order(order_data=order_data)
        print(f"{side.name} order placed for {qty}×{symbol} @ {limit_price:.2f}")

            
