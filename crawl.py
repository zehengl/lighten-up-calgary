import json
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(description="crawl LightenUpCalgary")
parser.add_argument(
    "year",
    type=int,
    help="year",
)
args = parser.parse_args()
year = args.year

data = Path("data")
data.mkdir(exist_ok=True)

module_name = f"lighten_up_calgary_{year}"
class_name = f"LightenUpCalgary{year}"

try:
    module = __import__(module_name)
    my_class = getattr(module, class_name)
    records = my_class.get_addresses()
    with open(data / f"{year}.json", "w") as f:
        json.dump(records, f, indent=2)
except ImportError:
    print(f"module not found: {module_name}")
except AttributeError:
    print(f"class not found: {class_name}")
except Exception as e:
    print(e)
else:
    print(f"{len(records)} records found")
