import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient

if os.path.exists(".env"):
    load_dotenv(override=True)
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")

uri = f"mongodb+srv://{user}:{password}@openscouting.xsr04sk.mongodb.net/?retryWrites=true&w=majority&appName=OpenScouting"
client = MongoClient(uri)

schema_db = client.schemas
data_schema_db = schema_db.data
app_schema_db = schema_db.app
entries_db = client.entries
security_db = client.security
keys_db = security_db.keys
alliances_db = security_db.alliances
rate_db = security_db.rate