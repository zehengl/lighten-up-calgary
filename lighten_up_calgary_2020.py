from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from settings import gcp_key
from source import LightenUpCalgary


class LightenUpCalgary2020(LightenUpCalgary):
    @classmethod
    def get_addresses(self):
        pages = ["calgary-nw", "calgary-ne", "calgary-sw", "calgary-se", "surroundings"]

        records = []
        last_updated = datetime.now().isoformat()
        for location in pages:
            url = urljoin(self.base_url, location)
            markup = requests.get(url).text
            soup = BeautifulSoup(markup, "html.parser")

            divs = soup.find_all("div", class_="et_pb_section")

            for div in tqdm(divs[:-1], desc=f"{location}"):
                inner_text = div.find("div", class_="et_pb_text_inner")
                address = inner_text.find_all("p")[-1].text.replace("\xa0", "")
                lat, lng, address = LightenUpCalgary2020.get_geocode(
                    f"{address}, Calgary"
                )
                if not lat or not lng or not address:
                    continue
                record = dict(
                    address=address,
                    quadrant=location,
                    lat=lat,
                    lng=lng,
                    last_updated=last_updated,
                )
                records.append(record)

        return records

    @classmethod
    def get_geocode(self, address):
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"key": gcp_key, "address": address}
        try:
            resp = requests.get(url, params=params).json()
            lat = resp["results"][0]["geometry"]["location"]["lat"]
            lng = resp["results"][0]["geometry"]["location"]["lng"]
            address = resp["results"][0]["formatted_address"]
        except:
            lat, lng, address = None, None, None
        return lat, lng, address
