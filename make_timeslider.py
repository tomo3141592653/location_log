# 必要なライブラリのインポート
import pandas as pd
import folium
from folium import plugins
import datetime
from folium.plugins import HeatMapWithTime

# データの読み込み
data = pd.read_csv("timeline_resample.csv")

# タイムスタンプの列をdatetime型に変換
data["timestamp"] = pd.to_datetime(data["datetime"])


# 地図の生成
m = folium.Map(location=[35.6895, 139.6917], zoom_start=12)


# ピンを線でつなぐためのGeoJSON形式のデータを生成
geojson_features_line = [
    {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [lon, lat] for lat, lon in zip(data["latitude"], data["longitude"])
            ],
        },
        "properties": {
            "times": data["timestamp"].astype(str).tolist(),
            "popup": [str(ts) for ts in data["timestamp"]],
            "id": "line",
        },
    }
]

# タイムスタンプ付きのGeoJSONを追加（線の表示）
plugins.TimestampedGeoJson(
    {"type": "FeatureCollection", "features": geojson_features_line},
    period="PT2H",  # 2時間ごとにデータを表示
    duration="P7D",  # 1日間のデータを表示
    add_last_point=True,  # 最後のポイントを表示
    auto_play=False,  # 自動再生しない
    loop=False,  # ループしない
    max_speed=64,  # 最大スピードを64倍に設定
    loop_button=True,  # ループボタンの表示
    date_options="YYYY-MM-DD HH:mm:ss",  # 日付の表示形式
    time_slider_drag_update=True,  # スライダーをドラッグしたときに地図を更新
).add_to(m)


# 地図を表示
m.save("timeline.html")
