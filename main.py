import pandas as pd
import config
from data_loader import load_hourly_solar_data
from data_loader import load_hourly_load_data
from simulation import run_simulation
from components.battery import Battery

def main(solar_fields):
    # Load only selected solar fields
    hourly_data_dic = load_hourly_solar_data(
        #filename="data/hourly_data.json",
        #selected_fields=config.SELECTED_FIELD_NAMES
        solar_fields = solar_fields
    )

    # Combine the power from selected fields
    hourly_generation = hourly_data_dic
    for field_name, df in hourly_data_dic.items():
        num_panels = config.PANEL_FIELDS[field_name]['num_panels']
        df['power_kwh'] = df['power_kwh'] * num_panels * config.KWP / 1000
        hourly_generation[field_name] = df

    solar_df = sum(hourly_generation.values()).round(3)
    solar_df.columns = ["power_kwh"]

    # Load a load profile
    load_df = load_hourly_load_data("data/hourly_load_data_per_month.csv")

    # Create battery
    battery = Battery(capacity_kwh=config.BATTERY_CAPACITY_KWH)

    # Align dataframes
    start = max(solar_df.index.min(), load_df.index.min())
    end = min(solar_df.index.max(), load_df.index.max())
    solar_df = solar_df[start:end]
    load_df = load_df[start:end]

    # Run simulation
    results = run_simulation(solar_df, load_df, battery)

    # Save results or plot
    #results.to_csv("results/simulation_output.csv")

    # Return results
    return results


if __name__ == "__main__":
    main()