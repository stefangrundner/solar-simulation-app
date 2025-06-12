## Parameters of solar installation

import pandas as pd

# Location
LATTITUDE = 41.075
LONGITUDE = -8.466

# Data time window (must be between 2005 and 2023)
STARTYEAR = 2023
ENDYEAR = 2023

# Solar panel parameters
KWP = 0.45 # kwp in kwh

# Panel fields
PANEL_FIELDS = {
    'roof_southwest': {'azimuth': 240, 'tilt': 20, 'num_panels': 19},
    'roof_northeast': {'azimuth': 60, 'tilt': 20, 'num_panels': 14},
    'backwall_t90': {'azimuth': 230, 'tilt': 90, 'num_panels': 12},
    'street_wall': {'azimuth': 160, 'tilt': 90, 'num_panels': 8},
    'roof_southwest_opt_winter': {'azimuth': 150, 'tilt': 40, 'num_panels': 8}
}


# Field selection
selection_vector = [1, 0, 1, 1, 1]

SELECTED_FIELD_NAMES = [
    name for (name, include) in zip(PANEL_FIELDS.keys(), selection_vector) if include == 1
]

# Inverter parameters
INVERTER_DC_AC_EFFICIENCY = 0.98
INVERTER_AC_DC_EFFICIENCY = 0.98

# Battery parameters
BATTERY_CAPACITY_KWH = 15
BATTERY_CHARGE_EFFICIENCY = 0.95
BATTERY_DISCHARGE_EFFICIENCY = 0.95

# Example simulation inputs
HOURLY_SOLAR_INPUT_KWH = [6, 2, 8]   # Example solar energy per day
HOURLY_LOAD_KWH = [4, 5, 6]