class Story:
    def __init__(self):
        self.deals = []
        self.bars = []

    def add_bar(self, bar):
        self.bars.append(bar)

    def get_last_bar(self):
        if len(self.bars) == 0:
            return None

        return self.bars[-1]

    def add_deal(self, deal):
        self.deals.append(deal)