from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


from lighten_up_calgary_2022 import LightenUpCalgary2022


class LightenUpCalgary2023(LightenUpCalgary2022):
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
                address = inner_text.text.split("\n")[-1].replace("\xa0", "")
                lat, lng, address = LightenUpCalgary2023.get_geocode(
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
