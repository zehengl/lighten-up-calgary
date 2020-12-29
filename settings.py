from os import getenv

from dotenv import load_dotenv

load_dotenv()

gcp_key = getenv("GCP_KEY")
assert gcp_key, "GCP_KEY not configured"

mapquest_key = getenv("MAPQUEST_KEY")
assert mapquest_key, "MAPQUEST_KEY not configured"
