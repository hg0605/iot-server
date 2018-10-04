import datetime
import uuid


from src.common.database import Database

class Directions(object):

    def __init__(self,cartID,direction,distance,_id=None,printdata="Yes"):
        self.cartID=cartID
        self.direction=direction
        self.distance=distance
        self._id=uuid.uuid4().hex if _id is None else _id
        self.printdata=printdata

    @staticmethod
    def get():
        data=Database.find("directions",{})
        if data is not None:
            return data
    @staticmethod        
    def getCartDirections(cartID):
        data=Database.find_one("directions",{"cartID":str(cartID)})
        if data is not None:
            return data

    @classmethod
    def push(cls,cartID,direction,distance):       
            new_data=cls(cartID,direction,distance)
            new_data.save_to_mongo()
            return True

    def json(self):
        return {
            "cartID":self.cartID,
            "_id":self._id,
            "printdata":self.printdata,
            "direction":self.direction,
            "distance":self.distance
        }

    def save_to_mongo(self):
        Database.insert("directions",self.json())

   