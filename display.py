# %%
import json
from pathlib import Path

import folium
import pandas as pd
import requests

from lighten_up_calgary_2020 import LightenUpCalgary2020
from settings import mapquest_key


output = Path("output")
output.mkdir(exist_ok=True)

yyc = (51.0447, -114.0719)
df = pd.read_json("data/2020.json")


# %%
m = folium.Map(location=yyc)
for row in df[["lat", "lng", "address"]].to_dict("records"):
    custom_icon = folium.CustomIcon("./static/favicon.png", icon_size=(24, 24))
    folium.Marker(
        location=(row["lat"], row["lng"]),
        icon=custom_icon,
        popup=row["address"],
    ).add_to(m)

m.save(str(output / "display.html"))
m


# %%
choices = df.sample(20)
start_location = "800 Macleod Trail SE, Calgary, AB T2P 2M5"

url = "http://www.mapquestapi.com/directions/v2/optimizedroute"
params = {"key": mapquest_key}
locations = [start_location] + choices["address"].to_list() + [start_location]
resp = requests.post(
    url,
    params=params,
    data=json.dumps({"locations": locations}),
).json()

print(f"Estimated time: {resp['route']['formattedTime']}")


# %%
ind = [int(j - 1) for j in resp["route"]["locationSequence"]][1:-1]
ordered_stops = choices.reset_index().loc[ind]
m = folium.Map(location=yyc)

lat, lng, _ = LightenUpCalgary2020.get_geocode(start_location)
folium.Marker(location=(lat, lng), tooltip="Home").add_to(m)

leg_number = 1
for row in ordered_stops[["lat", "lng", "address"]].to_dict("records"):
    html = f"""
    <div style="font-size: 10pt; color: black; ">
        <strong>#{leg_number}</strong>
    </div>
    """
    folium.Marker(
        location=(row["lat"], row["lng"]),
        icon=folium.DivIcon(html=html),
        tooltip=row["address"],
    ).add_to(m)
    folium.CircleMarker(
        location=(row["lat"], row["lng"]),
        radius=12,
    ).add_to(m)
    leg_number += 1

m.save(str(output / "route.html"))
m

# %%
