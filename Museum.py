from pymongo import MongoClient
import urllib
import os




class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance


class Museum(Singleton):

    client = MongoClient()
    gallery = os.path.join(os.getenv("HOME"),"db")



    def setDatabase(self, name):
        print("setting database")
        self.db = Museum.client[name]
        self.gallery = os.path.join(os.getenv("HOME"),"db",name)

    def getCurrations(self):
        pass


class Curator(object):

    def __init__(self, name):
        self.Museum = Museum()
        self._collection = self.Museum.client[name].images
        self._gallery = os.path.join(self.Museum.gallery, name)


    def collect(self, url):

        location = os.path.join(self._gallery, url.split("/")[-1])

        post = {"url": url,
                "diskPath": location}

        if not self._collection.find_one({"url":url}):
            self._collection.images.insert_one(post)
            urllib.request.urlretrieve(url,location)

    @property
    def collection(self):
        return self._collection

    @property
    def gallery(self):
        return self._gallery





