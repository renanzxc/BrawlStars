from pymongo import MongoClient
import os


class DB:
    def __init__(self):
        self.session = None

    def __enter__(self):
        url = os.getenv("brawlMongoUrl")

        if self.session is not None:
            raise RuntimeError("Already connected")
        self.session = MongoClient(url)
        return self.session.brawl_stars

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None
