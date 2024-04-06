import csv
import time
from datetime import datetime, timedelta
import re

# Initialize the accumulated total
accumulated_total = 0

with open('input.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    headers = next(reader)  # Skip the header row

    # Read all rows into a list
    rows = list(reader)

    # Open the output CSV file
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        # writer.writerow(['Epoch Unix Timestamp', 'Accumulated Sensor Value'])  # Write the header row

        # Process each row in the input file, except for the last one
        for row in rows[:-1]:
            print(row)
            # Skip empty rows
            if not row:
                continue

            date_str = row[0]
            date = datetime.strptime(date_str, '%Y-%m-%d')
            print(date)
            # Process each hour, stopping four columns earlier
            for i in range(1, len(headers) - 3):
                # Extract the hour and period from the header
                match = re.search(r'(\d+) (am|pm) kWh Consumption', headers[i].strip(), re.I)

                if match:
                    hour, period = match.groups()
                    hour = int(hour)
                    if period.lower() == 'pm' and hour != 12:
                        hour += 12
                    elif period.lower() == 'am' and hour == 12:
                        hour = 0
                    print(hour)
                    # Calculate the Unix timestamp for the current hour
                    timestamp = int((date + timedelta(hours=hour)).timestamp())

                    # Get the sensor value for the current hour and add it to the accumulated total
                    sensor_value = float(row[i])
                    accumulated_total += sensor_value
                    accumulated_total = round(accumulated_total, 2)

                    # Write the timestamp and accumulated total to the output file
                    writer.writerow([timestamp, accumulated_total])