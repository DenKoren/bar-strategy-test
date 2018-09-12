import datetime


def calc_trend(start_price, end_price):
    if end_price > start_price:
        return 1
    elif end_price == start_price:
        return 0
    else:
        return -1


class Bar:
    """
    Currency quotes history simplest element
    """

    def __init__(self, date, time, price_open, price_max, price_min, price_close, scale):
        """
        :type date:         datetime.date
        :type time:         datetime.time
        :type price_open:   float
        :type price_max:    float
        :type price_min:    float
        :type price_close:  float
        :type scale:        int - bar scale in minutes
        """
        self.date = date
        self.time = time
        self.open = price_open
        self.min = price_min
        self.max = price_max
        self.close = price_close
        self.scale = scale

    def __sub__(self, other):
        return BarDiff(self, other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "date={}, time={}, open={}, min={}, max={}, close={}, trend={}".format(
            self.date, self.time, self.open, self.min, self.max, self.close, self.trend
        )

    @property
    def trend(self):
        return calc_trend(self.open, self.close)

    @property
    def datetime(self):
        return datetime.datetime.combine(self.date, self.time)

    @property
    def is_closed(self):
        return self.close != 0

    def join(self, bar2):
        """
        :type bar2: Bar
        :rtype: Bar
        """
        return Bar(
            self.date,
            self.time,
            self.open,
            max(self.max, bar2.max),
            min(self.min, bar2.min),
            bar2.close,
            self.scale + bar2.scale
        )


class BarDiff:
    """
    Difference between two bars in history
    """
    def __init__(self, bar1, bar2):
        """
        :type bar1: Bar
        :type bar2: Bar
        :return:
        """
        first = bar1
        second = bar2

        if bar1.date > bar2.date:
            first = bar2
            second = bar1

        self.bar1 = first
        self.bar2 = second

    @property
    def date(self):
        return self.bar2.date - self.bar1.date

    @property
    def open(self):
        return self.bar2.open - self.bar1.open

    @property
    def max(self):
        return self.bar2.max - self.bar1.max

    @property
    def min(self):
        return self.bar2.min - self.bar1.min

    @property
    def close(self):
        return self.bar2.close - self.bar1.close

    @property
    def trend(self):
        if self.open > 0:
            return 1
        elif self.open == 0:
            return 0
        else:
            return -1
