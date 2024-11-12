import csv
from dataclasses import dataclass, asdict
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

# Define a dataclass for each row entry
@dataclass
class MeasurementRecord:
    index: int
    start_time: str
    end_time: str
    timestamp: str
    value: float
    measurement: str
    source: str
    user_terminal_id: str

def parse_file(file_path):
    # Use defaultdict to create a dictionary with a list for each measurement type
    data = defaultdict(list)

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        
        # Iterate over each row in the file
        for row in csv_reader:
            if len(row) < 10:  # Ensure row has enough columns to avoid errors
                continue
            
            try:
                # Parse fields with appropriate error handling
                index = int(row[2])
                start_time = row[3]  # Keep as string
                end_time = row[4]    # Keep as string
                timestamp = row[5]   # Keep as string
                value = float(row[6])
                measurement = row[7]
                source = row[8]
                user_terminal_id = row[9]
                
                # Create a record and add it to the dictionary under its measurement type
                record = MeasurementRecord(
                    index=index,
                    start_time=start_time,
                    end_time=end_time,
                    timestamp=timestamp,
                    value=value,
                    measurement=measurement,
                    source=source,
                    user_terminal_id=user_terminal_id
                )
                data[measurement].append(record)
            
            except ValueError as e:
                print(f"Skipping row due to error: {e} - Row data: {row}")
                continue  # Skip rows with data conversion errors

    return data

# Usage example
file_path = "2024-10-29_14_24_influxdb_data.csv"
data = parse_file(file_path)

# Print each measurement type and its corresponding records
for measurement_type, records in data.items():
    print(f"Measurement Type: {measurement_type}")
    for record in records:
        print(asdict(record))  # Convert to dictionary for easier readability


#TODO fix plots

def plot_measurements(data):
    for measurement_type, records in data.items():
        # Convert timestamps to datetime objects with the correct format
        timestamps = [
            datetime.strptime(record.timestamp, '%Y-%m-%dT%H:%M:%SZ') 
            for record in records
        ]
        values = [record.value for record in records]
        
        # Create a DataFrame for easier manipulation
        df = pd.DataFrame({"timestamp": timestamps, "value": values})
        
        # Apply a rolling mean to smooth data (e.g., window of 5)
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['value'], color="blue", alpha=0.4, label="Original Value")

        # Customize the plot
        plt.title(f"{measurement_type} Over Time")
        plt.xlabel("Minute")
        plt.ylabel("Value")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Set x-axis to show minutes only
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%M'))

        # Add legend and save the plot
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{measurement_type}_cleaned.png")
        plt.show()

plot_measurements(data)

def calculate_statistics(data):
    # Dictionary to store statistics for each measurement type
    stats = {}

    for measurement_type, records in data.items():
        # Extract values for calculation
        values = [record.value for record in records]

        # Calculate statistics
        mean_value = sum(values) / len(values) if values else float('nan')
        median_value = sorted(values)[len(values) // 2] if values else float('nan')
        std_dev = (sum((x - mean_value) ** 2 for x in values) / len(values)) ** 0.5 if values else float('nan')
        min_value = min(values) if values else float('nan')
        max_value = max(values) if values else float('nan')
        count = len(values)

        # Store the results in a dictionary
        stats[measurement_type] = {
            "Mean": mean_value,
            "Median": median_value,
            "Standard Deviation": std_dev,
            "Minimum": min_value,
            "Maximum": max_value,
            "Count": count
        }

    return stats

# Usage example
statistics = calculate_statistics(data)

# Print the statistics for each measurement type
for measurement_type, stats in statistics.items():
    print(f"Statistics for {measurement_type}:")
    for stat_name, stat_value in stats.items():
        print(f"\t{stat_name}: {stat_value}")
    print()
