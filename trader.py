import datetime

from bars import Bar
from strategy import TrendDetector
from strategy import Strategy
from strategy import Deal
from account import Cash
from story import Story
import const


class Trader:
    def __init__(
            self,
            initial_cash,
            start,
            stop
         ):
        self.active_deal = None
        self.skip_steps = 0
        self.strategy_scale = 1

        self.story = Story()
        self.account = Cash(initial_cash)
        self.detector = TrendDetector(2)
        self.strategy = Strategy(
            30,
            start,
            stop,
            0.80
        )

    @staticmethod
    def parse_chart_row(row):
        date = datetime.datetime.strptime(row[0], '%Y.%m.%d').date()
        time = datetime.datetime.strptime(row[1], '%H:%M').time()

        return Bar(
            date,
            time,
            float(row[2]),
            float(row[3]),
            float(row[4]),
            float(row[5]),
            1
        )

    def close_active_deal(self, bar):
        if self.active_deal is None:
            return

        profit = self.strategy.close_deal(self.active_deal, bar.open)

        if profit != 0:
            self.account.operation(bar.datetime, profit)

        self.active_deal = None

    def open_new_deal(self, bar):
        if self.strategy.loss_step > 4:
            self.detector.use_fast_detection()

        if self.detector.trend == const.TREND_NONE:
            return

        deal_size = self.strategy.next_deal_size

        self.account.operation(bar.datetime, -deal_size)
        new_deal = Deal(bar.datetime, bar.open, self.detector.trend, deal_size)

        self.active_deal = new_deal
        self.story.add_deal(new_deal)

    def step(self, bar):
        prev_bar = self.story.get_last_bar()
        self.story.add_bar(bar)

        if prev_bar is not None:
            self.detector.add_bar(prev_bar)

        self.close_active_deal(bar)

        if not self.strategy.can_trade(bar):
            return

        # if self.strategy.loss_step > 3:
        #     self.skip_steps = 10
        #     self.strategy.reset_losses()
        #
        # if self.skip_steps > 0:
        #     self.skip_steps -= 1
        #     return

        self.open_new_deal(bar)

    def start(self, chart_data):
        aggregate = Trader.parse_chart_row( next(chart_data) )

        for row in chart_data:
            bar = Trader.parse_chart_row(row)

            if aggregate.scale != self.strategy_scale:
                aggregate = aggregate.join(bar)
                continue

            self.step(aggregate)
            aggregate = bar
