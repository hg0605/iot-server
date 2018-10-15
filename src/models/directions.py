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

    @staticmethod        
    def getCartPosition(cartID):
        data=Database.find_one_queue("cartPosition",{"cartID":str(cartID)})
        
        return data
    @classmethod
    def push(cls,cartID,direction,distance):       
            new_data=cls(str(cartID),direction,distance)
            new_data.save_to_mongo()
            positionData=Database.find_one("cartPosition",{"cartID":str(cartID)})
            position=positionData['position']
            x=int(positionData['x'])
            y=int(positionData['y'])
            distance=int(distance)
            if(position=='+x'):
                if(direction=='Right'):
                    y=y-distance
                    position="-y"

                elif(direction=='Left'):
                    y=y+distance
                    position="+y"

                elif(direction=='Straight'):
                    x=x+distance

            elif(position=='-x'):
                if(direction=='Right'):
                    y=y+distance
                    position="+y"

                elif(direction=='Left'):
                    y=y-distance
                    position="-y"

                elif(direction=='Straight'):
                    x=x-distance

            elif(position=='+y'):
                if(direction=='Right'):
                    x=x+distance
                    position="+x"

                elif(direction=='Left'):
                    x=x-distance
                    position="-x"

                elif(direction=='Straight'):
                    y=y+distance

            elif(position=='-y'):
                if(direction=='Right'):
                    x=x-distance
                    position="-x"

                elif(direction=='Left'):
                    x=x+distance
                    position="+x"

                elif(direction=='Straight'):
                    y=y-distance

            positionData=Database.update("cartPosition",positionData,{"position":position,"x":x,"y":y})
            return True

    @staticmethod
    def stopCart(cartID):
        data=Database.update("directions",{"cartID":str(cartID),"sentStatus":"false"},{"sentStatus":"true"})
        return data

    @staticmethod                    
    def startCart(email,cartID):
        data=Database.find_one("cartPosition",{"cartID":str(cartID)})
        if(data is not None):
            data1=Database.update("cartPosition",{"cartID":str(cartID)},{"position":"+y","x":0,"y":0,"email":email})
        else:
            data1=Database.insert("cartPosition",{"cartID":str(cartID),"position":"+y","x":0,"y":0,"email":email})
        
        data=Database.remove("directions",{"cartID":str(cartID)})
        return True

    @staticmethod
    def requestNewCart(email,prevCartID,cartID):
        data=Database.update("users",{"email":email},{"currentCart":cartID})
        if(str(prevCartID)=="0"):
            print(email)
            print(cartID)
            if Directions.startCart(email,cartID):
                return True
        else:
            if(Directions.startCart(email,cartID)):
                directions=Database.find("directions",{"cartID":str(prevCartID)})
                if(directions is not None):
                    for direction in directions:
                        new_data=Directions(cartID,direction['direction'],direction['distance'])
                        new_data.push(cartID,direction['direction'],direction['distance'])
            return True
        return False
   
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

   