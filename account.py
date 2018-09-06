class Cash:
    def __init__(self, initial_amount):
        self.cash = initial_amount
        self.log = []

    def operation(self, dt, amount):
        # if (self.cash + amount) < 0:
        #     raise UserWarning("Account drained at {}. cash={}, amount to get={}".format(dt, self.cash, amount))

        self.cash += amount
        self.log.append(
            (dt, amount, self.cash)
        )
