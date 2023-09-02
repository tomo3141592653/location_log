import json
import csv
from io import StringIO
from datetime import datetime

# 1. JSONデータの読み込み
with open("/mnt/data/Records.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)


# 2. JSONから必要なデータを抽出し、変換する関数
def extract_and_convert_data(json_data):
    records = []
    for location in json_data["locations"]:
        timestamp = location["timestamp"]
        latitude = float(location["latitudeE7"]) / 1e7
        longitude = float(location["longitudeE7"]) / 1e7
        records.append([timestamp, latitude, longitude])
    return records


converted_data = extract_and_convert_data(json_data)


# 3. 2018年以降のデータをフィルタリングする関数
def filter_from_2018(data):
    filtered_data = []
    for record in data:
        timestamp_str = record[0].replace("Z", "")  # Removing the 'Z' at the end
        timestamp_datetime = datetime.fromisoformat(timestamp_str)
        if timestamp_datetime.year >= 2018:
            filtered_data.append(record)
    return filtered_data


filtered_data = filter_from_2018(converted_data)


# 4. データをCSVフォーマットに変換して保存する関数
def save_to_csv(data, filename):
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(["datetime", "latitude", "longitude"])  # Writing the headers
    csv_writer.writerows(data)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(csv_output.getvalue())


save_to_csv(filtered_data, "/mnt/data/filtered_data_2018_onwards.csv")
