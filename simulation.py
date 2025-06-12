import pandas as pd
from components.battery import Battery
import config

def run_simulation(solar_df, load_df, battery: Battery):
    solar_df = solar_df.rename(columns={"power_kwh": "solar_kwh"}).copy()
    load_df = load_df.rename(columns={"power_kwh": "load_kwh"}).copy()
    df = pd.concat([solar_df, load_df], axis=1).dropna()

    results = []

    for timestamp, row in df.iterrows():
        solar = row["solar_kwh"]
        load = row["load_kwh"]
        record = {
            "timestamp": timestamp,
            "solar": solar,
            "load": load,
            "battery_soc": battery.soc
        }

        solar_ac = solar * config.INVERTER_DC_AC_EFFICIENCY

        if solar_ac >= load:
            # 1. Cover load
            remaining = solar - load / config.INVERTER_DC_AC_EFFICIENCY

            # 2. Charge battery
            charged = battery.charge(remaining)
            remaining -= charged

            # 3. Feed remaining into grid
            record["grid_export"] = remaining * config.INVERTER_DC_AC_EFFICIENCY
            record["grid_import"] = 0.0
            record["battery_charge"] = charged
            record["battery_discharge"] = 0.0

        else:
            # 1. Use solar for part of load
            deficit = load - solar_ac

            # 2. Try to cover deficit from battery
            discharged = battery.discharge(deficit)
            unmet = deficit - discharged

            # 3. Draw unmet from grid
            record["grid_export"] = 0.0
            record["grid_import"] = unmet
            record["battery_charge"] = 0.0
            record["battery_discharge"] = discharged

        record["battery_soc"] = battery.soc
        results.append(record)

    result_df = pd.DataFrame(results).round(2).set_index("timestamp")
    return result_df