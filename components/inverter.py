class Inverter:
    def __init__(self, max_power_kw, efficiency=0.96):
        self.max_power = max_power_kw
        self.efficiency = efficiency

    def convert(self, input_kw):
        return min(input_kw, self.max_power) * self.efficiency