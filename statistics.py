from strategy import Deal


class DealsStat:
    def __init__(self, deals):
        """
        :type deals: list of Deal
        """
        self.deals = deals

        self.profit_deals_count = 0
        self.loss_deals_count = 0
        self.return_deals_count = 0

        self.series = {}

    @property
    def deals_count(self):
        return len(self.deals)

    def calc(self):
        prev_deal = self.deals[0]
        loss_series = False
        loss_series_start = None
        loss_series_size = 0

        self.count_profit_loss(prev_deal)

        for deal in self.deals[1:]:
            self.count_profit_loss(deal)

            if prev_deal.is_loss and deal.is_loss:
                if not loss_series:
                    loss_series = True
                    loss_series_start = prev_deal.open_time
                    loss_series_size = 1

                loss_series_size += 1

            if deal.is_profit and loss_series:
                if loss_series_size not in self.series:
                    self.series[loss_series_size] = []

                self.series[loss_series_size].append(
                    (loss_series_start, loss_series_size, prev_deal.size)
                )
                loss_series = False
                loss_series_size = 0

            prev_deal = deal

    def count_profit_loss(self, deal):
        if deal.is_loss:
            self.loss_deals_count += 1
        elif deal.is_profit:
            self.profit_deals_count += 1
        else:
            self.return_deals_count += 1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = """
        deals total: {total}
        profit count: {prc} ({prp}%)
        loss count: {lsc} ({lsp}%)
        return count: {rtc} ({rtp}%)
        series:
            """.format(
            total=self.deals_count,
            prc=self.profit_deals_count,
            prp=round(self.profit_deals_count/self.deals_count * 100, 2),
            lsc=self.loss_deals_count,
            lsp=round(self.loss_deals_count/self.deals_count * 100, 2),
            rtc=self.return_deals_count,
            rtp=round(self.return_deals_count/self.deals_count * 100, 2),
        )

        for series_size in self.series:
            last_series_of_size = self.series[series_size][-1]

            result += """size={s}, count={c}, last_deal=({start}, {money})
            """.format(
                s=series_size,
                c=len(self.series[series_size]),
                start=last_series_of_size[0],
                money=last_series_of_size[2],
            )

        return result


class AccountStat:
    def __init__(self, account):
        self.account = account

    def calc(self):
        return

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ""


class Stat:
    def __init__(self, deals, account):
        self.deals = DealsStat(deals)
        self.account = AccountStat(account)

    def calc(self):
        self.deals.calc()
        self.account.calc()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return """
        {}
        {}
        """.format(
            self.deals.__str__(),
            self.account.__str__(),
        )