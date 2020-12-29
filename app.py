import json
import os

import folium
import pandas as pd
import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from whitenoise import WhiteNoise

from forms import AddressForm
from lighten_up_calgary_2020 import LightenUpCalgary2020
from settings import mapquest_key

app = Flask(__name__)
Bootstrap(app)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "SECRET_KEY")
app.config["BOOTSTRAP_SERVE_LOCAL"] = True

yyc = (51.0447, -114.0719)
df = pd.read_json("data/2020.json")


@app.route("/", methods=["get", "post"])
def index():
    form = AddressForm(request.form)
    address = form.address.data
    number_of_locations = form.number_of_locations.data
    quadrant = form.quadrant.data

    if not address:
        m = folium.Map(location=yyc)
        for row in df[["lat", "lng", "address"]].to_dict("records"):
            custom_icon = folium.CustomIcon("./static/favicon.png", icon_size=(24, 24))
            folium.Marker(
                location=(row["lat"], row["lng"]),
                icon=custom_icon,
                tooltip=row["address"],
            ).add_to(m)

        start_location = None
        round_trip_time = None
        stops = None

    else:
        lat, lng, start_location = LightenUpCalgary2020.get_geocode(address)
        choices = df[df["quadrant"].isin(quadrant)].sample(number_of_locations)

        url = "http://www.mapquestapi.com/directions/v2/optimizedroute"
        params = {"key": mapquest_key}
        locations = [start_location] + choices["address"].to_list() + [start_location]
        resp = requests.post(
            url,
            params=params,
            data=json.dumps({"locations": locations}),
        ).json()

        round_trip_time = resp["route"]["formattedTime"]

        # %%
        ind = [int(j - 1) for j in resp["route"]["locationSequence"]][1:-1]
        ordered_stops = choices.reset_index().loc[ind]
        stops = ordered_stops["address"].to_list()

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

    result = {
        "map": m._repr_html_(),
        "address": start_location,
        "time": round_trip_time,
        "stops": stops,
    }

    return render_template("index.html", form=form, result=result)


if __name__ == "__main__":
    app.run(debug=True)
