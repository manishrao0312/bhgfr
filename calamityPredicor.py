from flask import Flask, render_template_string, request
import datetime
from collections import defaultdict

# Flask app setup
app = Flask(__name__)

# Simulated calamity data
calamity_data = {
    "earthquake": [
        {"date": "2024-11-25", "location": "California"},
        {"date": "2024-11-22", "location": "California"},
        {"date": "2024-11-15", "location": "Japan"},
        {"date": "2024-10-28", "location": "Mexico"},
    ],
    "flood": [
        {"date": "2024-11-20", "location": "Florida"},
        {"date": "2024-11-18", "location": "Bangladesh"},
        {"date": "2024-10-30", "location": "India"},
    ],
    "cyclone": [
        {"date": "2024-11-10", "location": "Philippines"},
        {"date": "2024-11-05", "location": "India"},
        {"date": "2024-10-25", "location": "Australia"},
    ],
}

# Convert string dates to datetime objects
for calamity, events in calamity_data.items():
    for event in events:
        event["date"] = datetime.datetime.strptime(event["date"], "%Y-%m-%d")

# Group calamities by location
calamity_intervals = {}
for calamity, events in calamity_data.items():
    locations = defaultdict(list)
    for event in events:
        locations[event["location"]].append(event["date"])

    # Calculate average time intervals for each calamity in each location
    averages = {}
    for location, dates in locations.items():
        dates.sort(reverse=True)
        intervals = [abs((dates[i] - dates[i + 1]).days) for i in range(len(dates) - 1)]
        average_interval = sum(intervals) / len(intervals) if intervals else 0
        averages[location] = average_interval

    calamity_intervals[calamity] = averages


# Function to predict calamity based on location and calamity type
def predict_calamity(calamity_type, location, current_date):
    if calamity_type not in calamity_intervals:
        return f"Calamity type '{calamity_type}' not recognized."

    if location not in calamity_intervals[calamity_type]:
        return f"No data available for {calamity_type} in {location}."

    most_recent_event = max(
        [e["date"] for e in calamity_data[calamity_type] if e["location"] == location]
    )
    days_since_last_event = (current_date - most_recent_event).days
    average_interval = calamity_intervals[calamity_type].get(location, 0)

    if average_interval == 0:
        return f"Not enough data to predict {calamity_type} in {location}."

    if days_since_last_event <= average_interval:
        return f"High chance of {calamity_type} in {location} in the coming days."
    else:
        return f"Low chance of {calamity_type} in {location} in the coming days."


@app.route("/calamity-prediction", methods=["GET", "POST"])
def calamity_prediction():
    prediction = ""
    if request.method == "POST":
        calamity_type = request.form["calamity_type"].strip().lower()
        location = request.form["location"].strip()
        current_date = datetime.datetime.now()
        prediction = predict_calamity(calamity_type, location, current_date)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calamity Prediction</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 50%;
                margin: 50px auto;
                padding: 20px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .form-group {
                margin: 20px 0;
            }
            label {
                display: block;
                font-size: 16px;
                margin-bottom: 5px;
            }
            input, select {
                width: 100%;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .prediction {
                margin-top: 30px;
                padding: 15px;
                background-color: #e7f7e7;
                border-radius: 5px;
                text-align: center;
                font-size: 18px;
                color: #333;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Calamity Prediction</h1>
            <form method="POST">
                <div class="form-group">
                    <label for="calamity_type">Select Calamity Type:</label>
                    <select id="calamity_type" name="calamity_type" required>
                        <option value="earthquake">Earthquake</option>
                        <option value="flood">Flood</option>
                        <option value="cyclone">Cyclone</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="location">Enter the Location:</label>
                    <input type="text" id="location" name="location" required>
                </div>
                <button type="submit">Predict Calamity</button>
            </form>

            {% if prediction %}
                <div class="prediction">
                    <p>{{ prediction }}</p>
                </div>
            {% endif %}
        </div>

    </body>
    </html>
    """, prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)  