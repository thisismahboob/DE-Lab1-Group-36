import requests
import csv
import datetime

# Define the API endpoint
URL = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&past_days=10&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

### Part 1. Read Operation (Extract)
def fetch_weather_data():
    """Fetches weather data for the past 10 days."""
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

### Part 2. Write Operation (Load)
def save_to_csv(data, filename):
    """Saves weather data to a CSV file."""
    with open(filename, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Writing header row
        writer.writerow(["Timestamp", "Temperature", "Humidity", "Wind Speed"])

        # Writing data rows
        for i in range(len(data["hourly"]["time"])):
            timestamp = data["hourly"]["time"][i]
            temp = data["hourly"]["temperature_2m"][i]
            humidity = data["hourly"]["relative_humidity_2m"][i]
            wind_speed = data["hourly"]["wind_speed_10m"][i]
            writer.writerow([timestamp, temp, humidity, wind_speed])

### Part 3. Cleaning Operation (Transform)
def clean_data(input_file, output_file):
    """Cleans the data based on given conditions."""
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header row
        headers = next(reader)
        writer.writerow(headers)

        # Filtering data
        for row in reader:
            temp, humidity, wind_speed = float(row[1]), float(row[2]), float(row[3])
            if 0 <= temp <= 60 and 0 <= humidity <= 80 and 3 <= wind_speed <= 150:
                writer.writerow(row)
    print("Cleaned data saved to", output_file)

### Part 4. Aggregation Operation
def summarize_data(filename):
    """Summarizes weather data including averages and extremes."""
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read header row
        data = list(reader)  # Convert CSV data to list

        if not data:
            print("No data available to summarize.")
            return

        # Extract values from columns
        temperatures = [float(row[1]) for row in data if row[1]]
        humidity_values = [float(row[2]) for row in data if row[2]]
        wind_speeds = [float(row[3]) for row in data if row[3]]

        # Compute statistics
        total_records = len(temperatures)
        avg_temp = sum(temperatures) / total_records
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        avg_humidity = sum(humidity_values) / total_records
        avg_wind_speed = sum(wind_speeds) / total_records

        # Print summary
        print("\n📊 Weather Data Summary 📊")
        print(f"Total Records: {total_records}")
        print(f"🌡️ Average Temperature: {avg_temp:.2f}°C")
        print(f"🔥 Max Temperature: {max_temp:.2f}°C")
        print(f"❄️ Min Temperature: {min_temp:.2f}°C")
        print(f"💧 Average Humidity: {avg_humidity:.1f}%")
        print(f"💨 Average Wind Speed: {avg_wind_speed:.2f} m/s")

if __name__ == "__main__":
    weather_data = fetch_weather_data()
    if weather_data:
        save_to_csv(weather_data, "weather_data.csv")
        print("Weather data saved to weather_data.csv")
        clean_data("weather_data.csv", "cleaned_data.csv")
        summarize_data("cleaned_data.csv")
