import sys
import csv
import pprint
import datetime

from trader import Trader
from statistics import Stat


file_path = sys.argv[1]

file = open(file_path, "r")
history = csv.reader(file)

trader = Trader(
    10000,
    datetime.time(14),
    datetime.time(16)
)

try:
    trader.start(history)
except UserWarning as e:
    pprint.pprint(e)

# pprint.pprint(trader.story.deals[-20:])
# pprint.pprint(trader.account.log[-20:])
# pprint.pprint(trader.account.cash)

statistics = Stat(
    trader.story.deals,
    trader.account.log,
)

statistics.calc()

print(trader)
print(statistics)

# except UserWarning as e:
#     pprint.pprint(bars[-100:])
#     # pprint.pprint(account.history)
#     pprint.pprint(deals[-30:])
#     # pprint.pprint(account.cash)
#     pprint.pprint(trend_detector)
#     pprint.pprint(e)
