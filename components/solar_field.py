class SolarField:
    def __init__(self, name, peak_power_kw, efficiency=0.85):
        """
        :param name: Identifier for the solar field
        :param peak_power_kw: Installed peak capacity (kWp)
        :param efficiency: Overall efficiency (e.g., 0.85 accounts for inverter, cabling losses etc.)
        """
        self.name = name
        self.peak_power = peak_power_kw
        self.efficiency = efficiency

    def simulate_generation(self, irradiance_kwh_per_kw):
        """
        Simulates energy output based on irradiance per kW installed.
        :param irradiance_kwh_per_kw: e.g., 4.5 means 4.5 kWh per kWp
        :return: Energy generated in kWh
        """
        return self.peak_power * irradiance_kwh_per_kw * self.efficiency