import pandas as pd
import math
import json

# 1. CSVファイルの読み込み
df = pd.read_csv("/mnt/data/combined_data_filtered_sorted.csv")

# 2. 東京の緯度と経度における150mの変化の計算
LATITUDE_PER_DEGREE = 111000  # in meters
LONGITUDE_PER_DEGREE_AT_TOKYO = LATITUDE_PER_DEGREE * math.cos(math.radians(35))
delta_lat = 150 / LATITUDE_PER_DEGREE
delta_lon = 150 / LONGITUDE_PER_DEGREE_AT_TOKYO

# 3. データの縮小
df["quantized_latitude"] = (df["latitude"] / delta_lat).astype(int)
df["quantized_longitude"] = (df["longitude"] / delta_lon).astype(int)
df_unique = df.drop_duplicates(subset=["quantized_latitude", "quantized_longitude"])

# 4. 縮小後のデータを元の緯度経度の形式でJSONに変換
json_data_original = df_unique[["latitude", "longitude"]].values.tolist()

# 5. JSONデータをファイルに保存
json_file_path = "/mnt/data/unique_data.json"
with open(json_file_path, "w") as f:
    json.dump(json_data_original, f)
