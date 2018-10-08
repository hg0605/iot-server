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
        self.sentStatus="false"

    @staticmethod
    def get():
        data=Database.find("directions",{})
        if data is not None:
            return data
    @staticmethod        
    def getCartDirections(cartID):
        data=Database.find_one_queue("directions",{"cartID":str(cartID),"sentStatus":"false"})
        if data is not None:
            data1=Database.update("directions",data,{"sentStatus":"true"})
            return data

    @classmethod
    def push(cls,cartID,direction,distance):       
            new_data=cls(cartID,direction,distance)
            new_data.save_to_mongo()
            return True

    def stopCart(cartID):
        data=Database.update("directions",{"cartID":str(cartID),"sentStatus":"false"},{"sentStatus":"true"})
        return data

    def json(self):
        return {
            "cartID":self.cartID,
            "_id":self._id,
            "printdata":self.printdata,
            "direction":self.direction,
            "distance":self.distance,
            "sentStatus":self.sentStatus
        }

    def save_to_mongo(self):
        print(self.json())
        Database.insert("directions",self.json())

   