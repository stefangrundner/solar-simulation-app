class Load:
    def __init__(self, load_series):
        self.load = load_series

    def get_demand(self, timestamp):
        return self.load.loc[timestamp]