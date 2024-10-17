from enum import Enum


class Fractal(Enum):
    THREE = 3
    FIVE = 5


class StopLoss(Enum):
    LAST_HTF_FRACTAL = 0
    LAST_LTF_FRACTAL = 1
    SWEEP = 2


API_KEY = 'oNKmJsFdyUF0vlM029zXAtiDf6ndz9CoWQEnklsavqLIfcSKjmMru8tAGILm4Ao7'
API_SECRET = 'dOKdybi7Uidh3bVyzgvM87nzqR4ExxdCdVczDWN831Gtl4f2irEoggB68YCZqvPD'

TICKER = 'BTCUSDT'
START_DATE = '2024-07-01'
END_DATE = '2024-10-01'

TIMEFRAMES = [
    ('4h', '1h'),
    # ('4h', '30m'),
    # ('4h', '15m'),
    # ('1h', '15m'),
    # ('1h', '5m'),
    # ('1h', '1m'),
]
COEFFICIENTS = [
    1,
    # 1.5,
    # 2,
    # 2.5,
    # 3
]

FRACTAL = Fractal.FIVE
EXCLUDE_IF_BOS_IS_LOWER_OR_HIGHER_THAN_SWEEP = True
STOP_LOSS = StopLoss.SWEEP
