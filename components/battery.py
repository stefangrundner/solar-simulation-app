class Battery:
    def __init__(self, capacity_kwh=10, soc=0.1, charge_eff=0.95, discharge_eff=0.95, max_depth=0.9):
        self.capacity = capacity_kwh
        self.soc = soc
        self.charge_eff = charge_eff
        self.discharge_eff = discharge_eff
        self.max_depth = max_depth

    def charge(self, energy_kwh):
        max_charge = (self.capacity - self.soc) / self.charge_eff
        actual_charge = min(energy_kwh, max_charge)
        self.soc += actual_charge * self.charge_eff
        return actual_charge

    def discharge(self, demand_kwh):
        available = (self.soc - self.capacity * (1 - self.max_depth)) * self.discharge_eff
        actual_discharge = min(demand_kwh, available)
        self.soc -= actual_discharge / self.discharge_eff
        return actual_discharge