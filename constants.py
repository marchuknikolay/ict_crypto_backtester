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

FRACTAL = Fractal.THREE
STOP_LOSS = StopLoss.LAST_HTF_FRACTAL

# For STOP_LOSS == StopLoss.LAST_HTF_FRACTAL or STOP_LOSS == StopLoss.LAST_LTF_FRACTAL
# For STOP_LOSS == StopLoss.SWEEP is always True
EXCLUDE_IF_BOS_IS_LOWER_OR_HIGHER_THAN_SWEEP = False

# For STOP_LOSS == StopLoss.SWEEP
EXCLUDE_IF_MANIPULATION_WAS_RESWEPT = False
