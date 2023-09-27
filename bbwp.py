import pandas as pd
import pandas_ta as ta

"""Bollinger Band Width Percentile based on The_Caretaker's work, converted to Python.
Please refer to the original work for more information:
 https://www.tradingview.com/script/tqitSsyG-Bollinger-Band-Width-Percentile/"""


def calculate_bbwp(price, bbwLen, bbwpLen):
    """Calculate the Bollinger Bands Width Percentile (BBWP) of a given close price series.
    :param price: Series of close prices.
    :param bbwLen: The time period to be used in calculating the Moving average
     which creates the Basis for the BBW component of the BBWP.
    :param bbwpLen: The lookback period to be used in calculating the BBWP itself"""
    # Convert price to a Series if it is not already
    close = pd.Series(price)

    if len(close) < bbwLen:
        return None

    # Calculate the BBW
    bbw = ta.bbands(close=close, length=bbwLen, std=2)["BBB_20_2.0"]

    # Initialize variables
    bbwSum = 0.0
    length = min(len(price), bbwpLen)

    # Calculate the sum of values below the bbw threshold
    for i in range(1, length + 1):
        bbwSum += 0 if bbw.iloc[-i] > bbw.iloc[-1] else 1

    # Calculate the percentile
    if len(price) >= bbwLen:
        return (bbwSum / length) * 100
    else:
        return None


def bbwp(data, bbwLen, bbwpLen):
    """Calculate the rolling BBWP of a given close price series."""
    rolling_bbwp = []

    i = 0
    while i < len(data):
        rolling_bbwp.append(calculate_bbwp(data[:i + 1], bbwLen, bbwpLen))
        i += 1

    return pd.Series(rolling_bbwp)
