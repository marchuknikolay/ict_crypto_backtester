from enum import Enum

class Fractal(Enum):
    THREE = 3
    FIVE = 5

class StopLoss(Enum):
    LAST_HTF_FRACTAL = 0
    LAST_LTF_FRACTAL = 1

API_KEY='oNKmJsFdyUF0vlM029zXAtiDf6ndz9CoWQEnklsavqLIfcSKjmMru8tAGILm4Ao7'
API_SECRET='dOKdybi7Uidh3bVyzgvM87nzqR4ExxdCdVczDWN831Gtl4f2irEoggB68YCZqvPD'

TICKER = 'BTCUSDT'
START_DATE = '2024-07-01'
END_DATE = '2024-10-01'

FRACTAL = Fractal.FIVE
EXCLUDE_IF_BOS_IS_LOWER_OR_HIGHER_THAN_SWEEP = False
STOP_LOSS = StopLoss.LAST_LTF_FRACTAL