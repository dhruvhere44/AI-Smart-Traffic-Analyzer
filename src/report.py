import pandas as pd
from datetime import datetime

def generate_report(
    cars,
    bikes,
    buses,
    trucks,
    density,
    occupancy,
    congestion
):

    data = {
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Cars": [cars],
        "Bikes": [bikes],
        "Buses": [buses],
        "Trucks": [trucks],
        "Density (%)": [density],
        "Occupancy (%)": [occupancy],
        "Congestion": [congestion]
    }

    df = pd.DataFrame(data)

    filename = "../reports/traffic_report.xlsx"

    df.to_excel(filename, index=False)

    print(f"\nReport Saved: {filename}")