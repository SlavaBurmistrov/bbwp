import pandas as pd
import pandas_ta as ta

"""Bollinger Band Width Percentile based on The_Caretaker's work, converted to Python.
Please refer to the original work for more information:
 https://www.tradingview.com/script/tqitSsyG-Bollinger-Band-Width-Percentile/"""


def calculate_bbwp(price, bbwLen, bbwpLen):
    # Calculate the moving average (basis)
    close = pd.Series(price)

    if len(close) < bbwLen:
        return None

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


def bbwp(data):
    rolling_bbwp = []

    i = 0
    while i < len(data):
        print(i)
        rolling_bbwp.append(calculate_bbwp(data[:i + 1], 20, 252))
        i += 1

    return pd.Series(rolling_bbwp)
