import datetime
import uuid


from src.common.database import Database

class Readings(object):

    def __init__(self,cartID,latitude,longitude,ir1,ir2,_id=None,printdata="Yes"):
        self.cartID=cartID
        self.latitude=latitude
        self.longitude=longitude
        self.ir1=ir1
        self.ir2=ir2
        self._id=uuid.uuid4().hex if _id is None else _id
        self.printdata=printdata

    @classmethod
    def get(cls):
        data=Database.find("readings",{})
        if data is not None:
            return data
    def getCartReading(cartID):
        data=Database.find_one("readings",{"cartID":str(cartID)})
        if data is not None:
            return data

    @classmethod
    def push(cls,cartID,latitude,longitude,ir1,ir2):       
            new_data=cls(cartID,latitude,longitude,ir1,ir2)
            new_data.save_to_mongo()
            return True

    def json(self):
        return {
            "cartID":self.cartID,
            "_id":self._id,
            "printdata":self.printdata,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "ir1":self.ir1,
            "ir2":self.ir2
        }

    def save_to_mongo(self):
        Database.insert("readings",self.json())

   