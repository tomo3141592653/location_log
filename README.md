# location_log
**行動ログの可視化**

**作成者**: 平田朋義  
**作成目的**: [2023年夏の自由研究発表会](https://sites.google.com/site/hiratatomogi/Home/announce/2023%E5%B9%B4%E5%A4%8F%E4%BC%91%E3%81%BF%E8%87%AA%E7%94%B1%E7%A0%94%E7%A9%B6%E7%99%BA%E8%A1%A8%E4%BC%9A)

## 動機

2014年から、iPhoneのGPSを利用して移動ログを記録してきた。
- 2014年から2018年まで: **Moves**という移動ログアプリ  
- サービス終了後は**Google Maps**を利用
- データ活用の動機: [**Breath of the Wild**の足跡機能](https://www.youtube.com/watch?v=xYV_OyFK4dA)を参考に自身の移動を可視化したい

## 成果物

1. [移動ログビジュアライゼーション](https://tomo3141592653.github.io/location_log/) - 行った場所をドットで表示
2. [週間時系列移動ビジュアライゼーション](https://tomo3141592653.github.io/location_log/timeline.html) - 移動をアニメーションで表示


## データ処理

### Moves

- Moves終了時にデータを一括ダウンロード可能
- データの中身の詳細説明は省略
- 課題:
  - 場所と移動のデータが別々に記録されていた
  - 移動データの途中に時刻情報がないため、出発・到着時刻から推定必要
  - 飛行機の移動は一直線に記録される問題
  - 一度の移動が100km以上のデータは削除(やりすぎたか)

### Google Maps

- Google TakeoutできれいなJSONフォーマットのデータが取得可能
- データ処理は、データをChatGPTに入力して「日時、緯度経度のCSV」として出力するだけ
### データの縮小
- 抽出データは約100万ポイントで、処理・表示のためにデータを削減
  - ドット表示のためのデータは150m以内のデータは同一とみなして重複を削除
    - これは他人のプライバシーのためでもある   
  - アニメーション表示のために10万件にリサンプル

## ChatGPTの活用

実際のデータ処理はほぼChatGPTにさせた。HTMLとJavaScriptもChatGPTでの指示に基づき作成。


- [Google Mapのログ解析](https://chat.openai.com/share/9897a844-ac52-43a2-913f-ef6095a1b393)
- [Movesのログ解析](https://chat.openai.com/c/0467c853-903c-4809-be4c-f3fe34714dc9)
- [データ処理](https://chat.openai.com/share/298c69cd-bc45-4b79-b6ed-46bb71cee837)
- [アニメーションの作成](https://chat.openai.com/share/50db1571-034b-46fb-a0da-03f8761cecce)
- [サイト作成](https://chat.openai.com/share/0e1e6012-ed10-4dbe-9e86-7357ef2a1403)

## 技術的解説
簡単に地図を作れるpythonのパッケージfoliumを使用している。  

行った場所をドットで表示する処理
```python
import folium

# データの読み込み
data = pd.read_csv("data.csv")

# タイムスタンプの列をdatetime型に変換
data["timestamp"] = pd.to_datetime(data["datetime"])

# 地図の生成
m = folium.Map(location=[35.6895, 139.6917], zoom_start=12)
# 訪れた場所の周囲をハイライトするためのマーカーを追加
for _, row in data.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=4,
        color='blue',
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

# 地図をHTMLファイルとして保存
m.save("dot_map.html")
```

移動をアニメーションでする処理
```python
import folium

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
    auto_play=True,  # 自動再生しない
    loop=False,  # ループしない
    max_speed=256,  # 最大スピードを64倍に設定
    loop_button=False,  # ループボタンの表示
    date_options="YYYY-MM-DD HH:mm:ss",  # 日付の表示形式
    time_slider_drag_update=True,  # スライダーをドラッグしたときに地図を更新
    speed_slider=True,  # スピードスライダーを表示
).add_to(m)

# 地図をhtmlで保存
m.save("timeline.html")
```

## 移動ログの感想

- この10年で福井県には訪れていないことに気付いた
- 南伊豆に行っていなかったのは意外だった
- 伊能忠敬のように、本州の海岸線を一周したら面白そう。
- 四国は一周している
- 九州は長崎あたりが面倒そう
- 一部の移動ログが途切れているエリアがある (例: 宮崎、鹿児島、島根)
- 飛行機での移動中に電波をオフに忘れた結果、マダガスカル周辺での飛行機移動が記録されていた
- データ処理、コーディングはchatGPTでかなり楽になったが工夫は必要。なんかダメそうなら遡って会話やりなおしとか。
- 飛行機データ削除は300km以上とかで速度も見たほうが良かったか。

## その他の考察

- 2014年以前のログデータは入手は不可能か？
- ログを自動更新するには？
## Issues
- google mapのlog入れたら自動でできるようにしたい。
- 現時点で大量データをgitで管理してしまっているが、データは外部で管理したい。
