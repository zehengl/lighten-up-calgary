import os

import pandas as pd
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from whitenoise import WhiteNoise

from display import show_all, get_route
from forms import AddressForm

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
        m, round_trip_time, stops, start_location = show_all(yyc, df), None, None, None

    else:
        choices = df[df["quadrant"].isin(quadrant)].sample(number_of_locations)
        m, round_trip_time, stops, start_location = get_route(yyc, choices, address)

    result = {
        "map": m._repr_html_(),
        "address": start_location,
        "time": round_trip_time,
        "stops": stops,
    }

    return render_template("index.html", form=form, result=result)


if __name__ == "__main__":
    app.run(debug=True)
