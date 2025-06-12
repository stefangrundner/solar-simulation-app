import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import config
from main import main

st.title("Solar Panel Field Configuration")

# Initialize session state to store fields
if "solar_fields" not in st.session_state:
    st.session_state.solar_fields = {}

# --- Field Creation UI ---
with st.form("Add Field"):
    field_name = st.text_input("Field name")
    azimuth = st.number_input("Azimuth (degrees, north=0, south=180)", min_value=0, max_value=360, value=180)
    tilt = st.number_input("Tilt angle (degrees)", min_value=0, max_value=90, value=30)
    num_panels = st.number_input("Number of panels", min_value=1, value=10)
    kwp_per_panel = st.number_input("kWp per panel", min_value=0.01, value=0.4)

    submitted = st.form_submit_button("Add Field")
    if submitted:
        if field_name in st.session_state.solar_fields:
            st.warning("Field name already exists.")
        else:
            st.session_state.solar_fields[field_name] = {
                "azimuth": azimuth,
                "tilt": tilt,
                "num_panels": num_panels,
                "kwp_per_panel": kwp_per_panel,
                "enabled": True,
            }
            st.success(f"Field '{field_name}' added!")

# --- Display and Select Fields ---
st.subheader("Configured Fields")
enabled_fields = []
for name, props in st.session_state.solar_fields.items():
    cols = st.columns([1, 3])
    with cols[0]:
        enabled = st.checkbox("Include", value=props["enabled"], key=f"{name}_checkbox")
    with cols[1]:
        st.markdown(f"**{name}** – Azimuth: {props['azimuth']}°, Tilt: {props['tilt']}°, "
                    f"Panels: {props['num_panels']}, kWp/panel: {props['kwp_per_panel']}")
    # Update status
    st.session_state.solar_fields[name]["enabled"] = enabled
    if enabled:
        enabled_fields.append(name)

# --- Run Simulation ---
if st.button("Run Simulation"):
    st.write("Running simulation with these fields:")
    st.json({name: props for name, props in st.session_state.solar_fields.items() if props["enabled"]})

    # You'd call your simulation function here
    # simulation_results = run_simulation(active_fields_dict)

    # Load simulation results
    #df = pd.read_csv("results/simulation_output.csv", parse_dates=["timestamp"])
    df = main(st.session_state.solar_fields)
    df['timestamp'] = df.index

    # Extract month and hour
    df['month'] = df['timestamp'].dt.month
    df['hour'] = df['timestamp'].dt.hour
    df['battery_perc'] = df['battery_soc']/config.BATTERY_CAPACITY_KWH*100

    # Streamlit app title
    st.title("Solar Power Installation Simulator")

    # Set up figure and axes for 12 months (4x3 grid)
    fig, axes = plt.subplots(4, 3, figsize=(20, 12), sharey=True)
    axes = axes.flatten()

    # Determine common y-axis limits for load/solar
    max_y = max(df['load'].max(), df['solar'].max()) * 1.1

    # Create subplots for each month
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        ax = axes[month - 1]
        monthly_data = df[df['month'] == month]

        if monthly_data.empty:
            continue
        
        # Compute monthly totals and max solar power
        solar_total = monthly_data['solar'].sum()
        load_total = monthly_data['load'].sum()
        import_total = monthly_data['grid_import'].sum()
        export_total = monthly_data['grid_export'].sum()
        max_solar = monthly_data['solar'].max()

        # Format as string to add to title
        summary_text = (
            f"Solar: {solar_total:.1f} kWh | "
            f"Load: {load_total:.1f} kWh\n"
            f"Grid Import: {import_total:.1f} kWh | "
            f"Grid Export: {export_total:.1f} kWh | "
            f"Solar Peak: {max_solar:.1f} kWh"
        )

        # Group by hour and calculate average
        hourly_avg = monthly_data.groupby('hour').mean(numeric_only=True)

        ax.plot(hourly_avg.index, hourly_avg['load'], label='Load (kWh)', color='red')
        ax.plot(hourly_avg.index, hourly_avg['solar'], label='Solar Power (kWh)', color='green')
        ax.plot(hourly_avg.index, hourly_avg['grid_export'], label='Grid Export (kWh)', color='black', linestyle='--')
        ax.plot(hourly_avg.index, hourly_avg['grid_import'], label='Grid Import (kWh)', color='orange', linestyle='--')

        # Secondary y-axis for SoC
        ax2 = ax.twinx()
        ax2.plot(hourly_avg.index, hourly_avg['battery_perc'], label="Battery SoC (%)", color='blue', linestyle='--')
        ax2.set_ylim(0, 100)

        ax.set_ylim(0, max_y)
        ax.set_title(f"{month_name}\n{summary_text}", fontsize=10)
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Power (kWh)")
        ax2.set_ylabel("SoC (%)")
        ax.set_xticks(range(0, 24))
        ax.grid(True)

        # Combined legend only in first subplot
        if month == 1:
            legend_lines, legend_labels = ax.get_legend_handles_labels()
            legend_lines2, legend_labels2 = ax2.get_legend_handles_labels()
            combined_lines = legend_lines + legend_lines2
            combined_labels = legend_labels + legend_labels2

    fig.legend(combined_lines, combined_labels,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.05),
            ncol=3,
            frameon=False)

    # Tight layout and render the full grid
    plt.tight_layout()
    st.pyplot(fig)