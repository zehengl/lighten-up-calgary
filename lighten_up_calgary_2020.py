from urllib.parse import urljoin
from datetime import datetime

import requests
from bs4 import BeautifulSoup

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

            for div in divs[:-1]:
                inner_text = div.find("div", class_="et_pb_text_inner")
                address = inner_text.find_all("p")[-1].text
                record = dict(
                    address=address.replace("\xa0", ""),
                    quadrant=location,
                    last_updated=last_updated,
                )
                records.append(record)

        return records
