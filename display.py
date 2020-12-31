# %%
import json
from pathlib import Path

import folium
import pandas as pd
import requests

from lighten_up_calgary_2020 import LightenUpCalgary2020
from settings import mapquest_key


def show_all(base, df):
    m = folium.Map(location=base)
    for row in df[["lat", "lng", "address"]].to_dict("records"):
        custom_icon = folium.CustomIcon("./static/favicon.png", icon_size=(24, 24))
        folium.Marker(
            location=(row["lat"], row["lng"]),
            icon=custom_icon,
            popup=row["address"],
        ).add_to(m)
    return m


def get_route(base, choices, address):
    lat, lng, start_location = LightenUpCalgary2020.get_geocode(address)

    url = "http://www.mapquestapi.com/directions/v2/optimizedroute"
    params = {"key": mapquest_key}
    locations = [start_location] + choices["address"].to_list() + [start_location]
    resp = requests.post(
        url,
        params=params,
        data=json.dumps({"locations": locations}),
    ).json()

    round_trip_time = resp["route"]["formattedTime"]

    ind = [int(j - 1) for j in resp["route"]["locationSequence"]][1:-1]
    ordered_stops = choices.reset_index().loc[ind]
    m = folium.Map(location=base)

    folium.Marker(location=(lat, lng), tooltip="Home").add_to(m)

    rows = ordered_stops[["lat", "lng", "address"]].to_dict("records")
    for ind, row in enumerate(rows):
        custom_icon = folium.CustomIcon(
            f"./static/numbers/{ind+1}.png", icon_size=(32, 32)
        )
        folium.Marker(
            location=(row["lat"], row["lng"]),
            icon=custom_icon,
            tooltip=row["address"],
        ).add_to(m)

    return m, round_trip_time, ordered_stops["address"].to_list(), start_location


# %%
if __name__ == "__main__":
    output = Path("output")
    output.mkdir(exist_ok=True)

    yyc = (51.0447, -114.0719)
    df = pd.read_json("data/2020.json")

    m = show_all(yyc, df)
    m.save(str(output / "display.html"))

    choices = df.sample(20)
    address = "800 Macleod Trail SE, Calgary, AB T2P 2M5"

    m, round_trip_time, stops, _ = get_route(yyc, choices, address)
    print(f"Estimated time: {round_trip_time}")
    print("Order of stops:")
    for ind, address in enumerate(stops):
        print(f"#{ind} - {address}")
    m.save(str(output / "route.html"))
