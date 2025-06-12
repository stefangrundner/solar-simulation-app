import json
import pandas as pd
import config

def get_hourly_data (field):
    field_dic = {}
    field_dic[field['name']], metadata, inputs = pvlib.iotools.get_pvgis_hourly(latitude=latitude,
                               longitude=longitude,
                               start=startyear,
                               end=endyear,
                               raddatabase=None,
                               components=True,
                               surface_tilt=field['tilt'],
                               surface_azimuth=field['azimuth'],
                               outputformat='json',
                               usehorizon=True,
                               userhorizon=None,
                               pvcalculation=True,
                               peakpower=1,
                               pvtechchoice='crystSi',
                               mountingplace='building',
                               loss=14,
                               trackingtype=0,
                               optimal_surface_tilt=False,
                               optimalangles=False,
                               url='https://re.jrc.ec.europa.eu/api/',
                               map_variables=True,
                               timeout=30)
    return field_dic

def load_hourly_solar_data(filename="data/hourly_data.json", solar_fields=None):
    with open(filename, "r") as f:
        raw_data = json.load(f)

    selected_fields = {field: props for field, props in solar_fields.items() if props.get('enabled')}

    hourly_data_dic = {
        field: pd.DataFrame({
            "power_kwh": data["power_kwh"]
        }, index=pd.to_datetime(data['timestamp']).floor('h'))
        for field, data in raw_data.items()
        if solar_fields is None or field in selected_fields
    }

    return hourly_data_dic

def load_hourly_load_data(filename="data/hourly_load_data_per_month.csv"):
    raw_data = pd.read_csv(filename, sep=";")

    date_range = pd.date_range(start=f'{config.STARTYEAR}-01-01', end=f'{config.ENDYEAR}-12-31 23:00', freq='h')
    months = date_range.month
    month_profiles = raw_data.set_index('Month').T.to_dict('list')
    consumptions = [month_profiles[m][dt.hour] for dt, m in zip(date_range, months)]
    hourly_load_data = pd.DataFrame({'power_kwh': consumptions}, index=date_range)

    return hourly_load_data 

