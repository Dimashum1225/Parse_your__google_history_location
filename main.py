import json
import pandas as pd

# путь к твоему JSON-файлу
input_file = 'Хронология.json'
output_file = 'parsed_locations.xlsx'
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

segments = data.get("semanticSegments", [])  # берём именно список сегментов

rows = []
for item in segments:
    start_time = item.get('startTime')
    end_time = item.get('endTime')

    # timelinePath
    for p in item.get("timelinePath", []):
        latlng = p.get("point")
        time = p.get("time")
        if latlng:
            lat, lon = latlng.replace("°", "").split(",")
            rows.append({
                "context": "timelinePath",
                "latitude": lat.strip(),
                "longitude": lon.strip(),
                "time": time,
                "segment_start": start_time,
                "segment_end": end_time
            })

    activity = item.get("activity")
    if activity:
        # start
        start = activity.get("start", {}).get("latLng")
        if start:
            lat, lon = start.replace("°", "").split(",")
            rows.append({
                "context": "activity_start",
                "latitude": lat.strip(),
                "longitude": lon.strip(),
                "time": start_time,
                "segment_start": start_time,
                "segment_end": end_time
            })

        # end
        end = activity.get("end", {}).get("latLng")
        if end:
            lat, lon = end.replace("°", "").split(",")
            rows.append({
                "context": "activity_end",
                "latitude": lat.strip(),
                "longitude": lon.strip(),
                "time": end_time,
                "segment_start": start_time,
                "segment_end": end_time
            })

        # parking
        parking = activity.get("parking", {}).get("location", {}).get("latLng")
        parking_time = activity.get("parking", {}).get("startTime")
        if parking:
            lat, lon = parking.replace("°", "").split(",")
            rows.append({
                "context": "parking_location",
                "latitude": lat.strip(),
                "longitude": lon.strip(),
                "time": parking_time,
                "segment_start": start_time,
                "segment_end": end_time
            })

df = pd.DataFrame(rows)
df.to_excel(output_file, index=False)
print(f"Сохранено в {output_file}")
