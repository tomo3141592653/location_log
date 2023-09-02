import json
import pandas as pd
import math


def haversine_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two points on the earth specified by latitude/longitude.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# Load the geojson data
with open("path_to_your_storyline.geojson", "r") as f:
    geojson_data = json.load(f)

features = geojson_data.get("features", [])

filtered_data_list = []

for feature in features:
    if feature["properties"]["type"] == "place":
        start_time = pd.to_datetime(feature["properties"]["startTime"], utc=True)
        end_time = pd.to_datetime(feature["properties"]["endTime"], utc=True)
        latitude = feature["geometry"]["coordinates"][1]
        longitude = feature["geometry"]["coordinates"][0]

        filtered_data_list.append([start_time, latitude, longitude])
        filtered_data_list.append([end_time, latitude, longitude])

for feature in features:
    if feature["properties"]["type"] == "move":
        segments = feature["geometry"]["coordinates"]
        start_time = pd.to_datetime(feature["properties"]["startTime"], utc=True)
        end_time = pd.to_datetime(feature["properties"]["endTime"], utc=True)

        total_coords = sum(len(segment) for segment in segments)
        time_diff = (end_time - start_time) / total_coords

        for segment in segments:
            if len(segment) > 1:  # Ensure segment has at least two points
                # Calculate the distance between the start and end points of the segment
                distance = haversine_distance(segment[0], segment[-1])
                # Only add the segment if the distance is <= 100km
                if distance <= 100000:
                    for coord in segment:
                        filtered_data_list.append([start_time, coord[1], coord[0]])
                        start_time += time_diff

filtered_distance_df = pd.DataFrame(
    filtered_data_list, columns=["datetime", "latitude", "longitude"]
)

filtered_distance_df.to_csv("timeline_resample.csv", index=False)
