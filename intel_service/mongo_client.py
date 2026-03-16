from pymongo import MongoClient
import time


class Mongo:
    def __init__(self, mongo_uri: str, db_name: str, col_name: str):
        client = MongoClient(mongo_uri)
        db = client[db_name]
        self.col = db[col_name]

    def find_is_exists(self, id: str):
        return self.col.find_one({"entity_id": id},{"_id": 0})

    def insert_doc(self, data: dict):
        self.col.insert_one(data)

    def update_doc(self, lat: float, lon: float, distance: float, id: str):
        filter_ = {"entity_id": id}
        new_val = {
            "$set": {"reported_lat": lat, "reported_lon": lon, "distance": distance}
        }
        self.col.update_one(filter=filter_, update=new_val, upsert=True)

