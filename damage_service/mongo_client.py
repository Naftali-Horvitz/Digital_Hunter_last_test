from pymongo import MongoClient
import time


class Mongo:
    def __init__(self, mongo_uri: str, db_name: str, col_name: str):
        client = MongoClient(mongo_uri)
        db = client[db_name]
        self.col = db[col_name]

    def find_is_exists(self, id: str):
        return self.col.find_one({"entity_id": id}, {"_id": 0})

    def insert_doc(self, data: dict):
        self.col.insert_one(data)
        
    def update_doc(
        self, timestamp_attack: str, attack_id: str, entity_id: str, weapon_type: str
    ):
        filter_ = {"entity_id": entity_id}
        new_val = {
            "$set": {
                "attack_id": attack_id,
                "timestamp_attack": timestamp_attack,
                "weapon_type": weapon_type,
            }
        }
        self.col.update_one(filter=filter_, update=new_val, upsert=True)
