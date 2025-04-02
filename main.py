from fastapi import FastAPI, WebSocket
import json
import numpy as np
import math
from collections import defaultdict

app = FastAPI()

# Global Data Storage
sorted_data = defaultdict(lambda: defaultdict(lambda: {"pixelCount": 0, "numberOfFrames": 0}))
color_data = defaultdict(lambda: {"pixelCount": 0, "numberOfFrames": 0})

# Precompute NumPy arrays for value mapping
range_bounds = np.array([
    -0.1, 3.8, 4.6, 5.4, 6.2, 6.9, 7.7, 8.5, 9.2, 10.0, 10.7, 11.5, 12.3, 13.1, 13.8, 14.6, 15.4, 16.2,
    16.9, 17.7, 18.5, 19.2, 20.0, 20.7, 21.5, 22.3, 23.1, 23.8, 24.6, 25.4, 26.2, 26.9, 27.7, 28.5, 29.2,
    30.0, 30.7, 31.5, 32.3, 33.1, 33.8, 34.6, 35.4, 36.2, 36.9, 37.7, 38.5, 39.2, 40.0, 40.8, 41.5, 42.3,
    43.1, 43.8, 44.6, 45.4, 46.2, 46.9, 47.7, 48.5, 49.9, 50.8, 51.5, 52.3, 53.1, 53.8, 54.6, 55.4, 56.2,
    56.9, 57.7, 58.5, 59.2, 60.0, 60.8, 61.5, 62.3, 63.1, 63.8, 64.6, 65.4, 66.2, 66.9, 67.7, 68.5, 69.2,
    70.0, 70.8, 71.5, 72.3, 73.1, 73.8, 74.6, 75.4, 76.2, 76.9, 77.7, 78.5, 79.2, 80.0, 80.8, 81.5, 82.3,
    83.1, 83.8, 84.6, 85.4, 86.2, 86.9, 87.7, 88.5, 89.2, 90.0, 90.8, 91.5, 92.3, 93.1, 93.8, 94.6, 95.4, 100
])

range_values = np.array([np.round(i, 1) for i in np.linspace(-6, 6, len(range_bounds)) if np.round(i, 1) != 0])

def value_from_range(average_percentage):
    """Optimized mapping using NumPy searchsorted with boundary checks."""
    index = np.searchsorted(range_bounds, average_percentage, side="right") - 1
    if average_percentage in range_bounds:
        index -= 1

    # Ensure the index is within valid range
    if index < 0:
        return range_values[0]  # Return the lowest value
    elif index >= len(range_values):
        return range_values[-1]  # Return the highest value

    return range_values[index]

def calculate_statistics(sorted_data, color_data):
    """
    This function is intentionally left blank.
    The logic used for psychological result calculations is proprietary and protected under patent.
    """
    pass
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()


    try:
        while True:
            receivedData = await websocket.receive_json()
            if receivedData == { "type": "ping" }:  # Handle keepalive pings
                continue  # Do nothing, just prevent disconnection
            if receivedData == { "type": "finish" }:  
                break 
            
            topic = receivedData.get("topic")
            data = receivedData.get("data")

            # Initialize topic if it doesn't exist
            if topic not in sorted_data:
                sorted_data[topic] = {}

            # Check if frame0 (canvas cleared or inactive)
            if "frame0" in data:
                if "frame0" not in sorted_data[topic]:
                    sorted_data[topic]["frame0"] = 0
                sorted_data[topic]["frame0"] += 1  # Count how many times frame0 is sent
            # Check if rating (canvas cleared or inactive)
            if "rating" in data:
                sorted_data[topic]["rating"] = data["rating"]  # Extract and store the rating value
            else:
                # Process color data
                for color, count in data.items():
                    if color not in sorted_data[topic]:
                        sorted_data[topic][color] = {"pixelCount": 0, "numberOfFrames": 0}
                    if color not in color_data:
                        color_data[color] = {"pixelCount": 0, "numberOfFrames": 0}
                    # Update pixel count
                    sorted_data[topic][color]["pixelCount"] += count
                    color_data[color]["pixelCount"] += count
                    # Increment numberOfFrames when new pixels are added
                    sorted_data[topic][color]["numberOfFrames"] += 1
                    color_data[color]["numberOfFrames"] += 1

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        results = calculate_statistics(sorted_data, color_data)
        # Send the entire dictionary only once when the connection is closing
        await websocket.send_text(json.dumps(results))
        #time.sleep(1)
        await websocket.close()
