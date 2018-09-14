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
        self.skip_steps = 0
        self.fast_detect_step = 4000
        self.strategy_scale = 5

        self.active_deal = None
        self.to_skip = 0

        self.story = Story()
        self.account = Cash(initial_cash)
        self.detector = TrendDetector(2)
        self.strategy = Strategy(
            30,
            start,
            stop,
            0.80
        )

        self.detector.strategy = self.strategy

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

    def manage_risks(self):
        if self.strategy.should_skip:
            self.to_skip = self.skip_steps

        if self.strategy.loss_step > self.fast_detect_step:
            self.detector.use_fast_detection()

    def can_open_deal(self):
        if self.to_skip > 0:
            self.to_skip -= 1
            return False

        if self.detector.trend == const.TREND_NONE:
            return False

        return True

    def open_new_deal(self, bar):
        if not self.strategy.can_trade(bar):
            return

        self.manage_risks()

        if not self.can_open_deal():
            return

        deal_size = self.strategy.next_deal_size

        self.account.operation(bar.datetime, -deal_size)
        new_deal = Deal(bar.datetime, bar.open, self.detector.trend, deal_size)

        self.active_deal = new_deal
        self.story.add_deal(new_deal)

    def step(self, bar):
        self.close_active_deal(bar)
        self.open_new_deal(bar)

        self.story.add_bar(bar)
        self.detector.add_bar(bar)

    def start(self, chart_data):
        aggregate = Trader.parse_chart_row(next(chart_data))

        bar = None
        for row in chart_data:
            bar = Trader.parse_chart_row(row)

            if aggregate.scale != self.strategy_scale:
                aggregate = aggregate.join(bar)
                continue

            self.step(aggregate)
            aggregate = bar

        if bar is not None:
            self.close_active_deal(bar)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return """
        strategy scale: {scale} min
        fast detect from: {fast_detect_step} step""".format(
            scale=self.strategy_scale,
            fast_detect_step=self.fast_detect_step
        )
