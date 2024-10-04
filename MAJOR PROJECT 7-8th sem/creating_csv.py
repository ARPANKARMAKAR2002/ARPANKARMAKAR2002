import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
num_days = 28  # Number of days to generate data for
num_spaces = 6  # Number of parking spaces
start_date = '2024-07-01'  # Start date for the data

# Generate date range
start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
end_datetime = start_datetime + timedelta(days=num_days)
date_range = pd.date_range(start=start_datetime, end=end_datetime, freq='H')

# Initialize lists to hold data
data = []

# Generate data for each parking space
for space_id in range(1, num_spaces + 1):
    for timestamp in date_range:
        occupancy_status = np.random.choice([0, 1], p=[0.7, 0.3])  # Randomly generate occupancy
        day_of_week = timestamp.dayofweek
        hour_of_day = timestamp.hour
        data.append([timestamp, space_id, occupancy_status, day_of_week, hour_of_day])

# Create DataFrame
df = pd.DataFrame(data, columns=['timestamp', 'parking_space_id', 'occupancy_status', 'day_of_week', 'hour_of_day'])

# Save to CSV
csv_filename = 'synthetic_parking_occupancy_data1.csv'
df.to_csv(csv_filename, index=False)

print(f"Data generation complete. File saved as '{csv_filename}'.")
