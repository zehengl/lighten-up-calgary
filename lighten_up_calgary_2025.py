from datetime import datetime
from urllib.parse import urljoin

import pyap
import usaddress
from bs4 import BeautifulSoup
from seleniumbase import Driver
from tqdm import tqdm

from lighten_up_calgary_2023 import LightenUpCalgary2023


def check_address(address_string):
    try:
        # tag() splits the string and determines the type ('Street Address', 'Ambiguous', etc.)
        parsed_data, address_type = usaddress.tag(address_string)
        return address_type == "Street Address"
    except usaddress.RepeatedLabelError:
        # Throws an error if the layout doesn't resemble a standard address format
        return False


class LightenUpCalgary2025(LightenUpCalgary2023):
    @classmethod
    def get_addresses(self):
        pages = ["calgary-nw", "calgary-ne", "calgary-sw", "calgary-se", "surroundings"]

        records = []
        last_updated = datetime.now().isoformat()
        driver = Driver(browser="chrome", guest_mode=True)
        for location in pages:
            url = urljoin(self.base_url, location)
            driver.get(url)
            markup = driver.get_page_source()
            soup = BeautifulSoup(markup, "html.parser")

            divs = soup.find_all("div", class_="et_pb_section")

            for div in tqdm(divs, desc=f"{location}"):
                inner_text = div.find("div", class_="et_pb_text_inner")
                if not inner_text:
                    continue
                ps = div.find_all("p")
                address = None
                for p in ps:
                    text = p.text.replace("\xa0", "")

                    if check_address(text):
                        address = text
                        break

                if not address:
                    continue

                lat, lng, address = LightenUpCalgary2023.get_geocode(address)
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
