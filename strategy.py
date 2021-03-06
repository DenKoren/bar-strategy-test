import const
import math
import datetime
from bars import calc_trend


class TrendDetector:
    """
    :type history: list<Bar>
    """
    def __init__(self, quorum):
        self.default_quorum = quorum

        self.history = []
        self.last_trend = const.TREND_NONE
        self._use_fast_detection = False

        self.strategy = None

    def add_bar(self, bar):
        self.history.append(bar)
        self.history = self.history[-self.quorum:]

    @property
    def quorum(self):
        if self.strategy is None:
            return self.default_quorum

        return self.default_quorum + round(self.strategy.loss_step/3)

    @property
    def trend(self):
        if self.fast_trend_detect():
            return self.last_trend

        if self.stable_trend_detect():
            return self.last_trend

        return self.last_trend

    def fast_trend_detect(self):
        if not self._use_fast_detection:
            return False

        if len(self.history) < 2:
            return False

        bar1 = self.history[-2]
        bar2 = self.history[-1]

        if (bar1.trend == bar2.trend) or (const.TREND_NONE in [bar1.trend, bar2.trend]):
            return False

        combined = bar1.join(bar2)
        if combined.trend == bar1.trend:
            # means that bar1.close and bar2.close are on the same side of bar1.open. No trend change.
            return False

        self.last_trend = combined.trend
        self._use_fast_detection = False
        return True

    def stable_trend_detect(self):
        if len(self.history) < self.quorum:
            return False

        first = self.history[0]

        trends_same = True
        for bar in self.history[1:]:
            if first.trend != bar.trend:
                trends_same = False

        if not trends_same:
            return False

        self.last_trend = first.trend
        return True

    def change_quorum(self, new_quorum):
        self.default_quorum = new_quorum

    def use_fast_detection(self):
        self._use_fast_detection = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "trend={}".format(self.trend)


class Strategy:
    def __init__(self, basic_deal_size, trade_start, trade_end, profit_factor):
        self.basic_deal_size = basic_deal_size
        self.profit_factor = profit_factor

        self.trade_start = trade_start
        self.trade_end = trade_end

        self.default_skip_from = 4

        self.losses = []
        self.skip_from = 0

        self.reset_risk_level()

    def close_deal(self, deal, price):
        """
        :type deal: Deal
        :type price: int
        :rtype int
        """
        profit = 0

        deal.close(price)

        if deal.result == const.DEAL_RESULT_PROFIT:
            profit = deal.size * (1 + self.profit_factor)
            self.reset_risk_level()
        elif deal.result == const.DEAL_RESULT_RETURN:
            profit = deal.size
        else:
            self.inc_risk_level(deal.size)

        return profit

    def inc_risk_level(self, loss_size):
        self.losses.append(loss_size)

    def reset_risk_level(self):
        self.losses = []
        self.skip_from = self.default_skip_from

    @property
    def next_deal_size(self):
        size = self.basic_deal_size * self.profit_factor
        for loss in self.losses:
            size += loss

        return math.ceil(size / self.profit_factor)

    @property
    def has_losses(self):
        return len(self.losses) > 0

    @property
    def loss_step(self):
        return len(self.losses)

    @property
    def should_skip(self):
        result = self.loss_step >= self.skip_from

        if result:
            self.skip_from += 1

        return result

    def can_trade(self, bar):
        return self.has_losses or self.is_trade_time(bar)

    def is_trade_time(self, bar):
        if bar.date.weekday() >= 5:
            return False

        if self.trade_start < self.trade_end:
            return self.trade_start < bar.time < self.trade_end
        elif self.trade_start > self.trade_end:
            return (self.trade_start < bar.time) or (bar.time < self.trade_end)


class Deal:
    def __init__(self, start_time, open_price, predicted_trend, size):
        """
        :type start_time: datetime.datetime
        :type open_price: float
        :type predicted_trend: int
        :type size: float
        """

        self.open_time = start_time
        self.open_price = open_price
        self.close_price = 0
        self.trend = predicted_trend
        self.size = size
        self.result = None

    def is_closed(self):
        return self.close_price != 0

    def close(self, price):
        self.close_price = price
        actual_trend = calc_trend(self.open_price, self.close_price)

        self.result = self.trend * actual_trend

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "date={}, size={}, open_price={}, close_price={}, trend={}, result={}".format(
            self.open_time, self.size, self.open_price, self.close_price, self.trend, self.result
        )

    @property
    def is_loss(self):
        return self.result < 0

    @property
    def is_profit(self):
        return self.result > 0

    @property
    def is_return(self):
        return self.result == 0