import csv
from dataclasses import dataclass, asdict
from collections import defaultdict
import matplotlib.pyplot as plt

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
        # Extract timestamps and values for plotting
        timestamps = [record.timestamp for record in records]
        values = [record.value for record in records]
        
        # Convert timestamps to a suitable format if necessary
        # For simplicity, we assume timestamps are in a format directly usable
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, values, marker='o', linestyle='-')
        
        # Customize the plot
        plt.title(f"{measurement_type} Over Time")
        plt.xlabel("Timestamp")
        plt.ylabel("Value")
        plt.xticks(rotation=45)
        plt.grid(True)
        
        # Save or show the plot
        plt.tight_layout()
        plt.savefig(f"{measurement_type}.png")  # Save as a PNG file
        plt.show()  # Display the plot

# plot_measurements(data)