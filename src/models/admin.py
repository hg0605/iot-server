import datetime
import uuid
import xml.etree.ElementTree,json
from flask import session

from src.common.database import Database


class Admin(object):

    def __init__(self,email,password,name=None,_id=None,printdata="no"):
        self.email=email
        self.password=password
        self.name=name
        self._id=uuid.uuid4().hex if _id is None else _id
        self.printdata=printdata

    @classmethod
    def get_by_email(cls,email):
        data=Database.find_one("admin",{"email":email})
        if data is not None:
            return cls(**data)


    @classmethod
    def get_by_id(cls,_id):
        data=Database.find_one("admin",{"_id":_id})
        if data is not None:
            return cls(**data)


    @staticmethod
    def fetchDelivery():
        e = xml.etree.ElementTree.parse('thefile2.xml').getroot()
        materials=[]
        for elem in e.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
            material=elem.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Material').text
            quantity=elem.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}OriginalDeliveryQuantity').text
            materials.append(json.loads('{"Material":"'+material+'","Quantity":"'+quantity+'"}'))
        return materials

    @staticmethod
    def assignDelivery(user_email):
        e = xml.etree.ElementTree.parse('thefile2.xml').getroot()
        materials=[]
        for elem in e.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
            material=elem.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Material').text
            quantity=elem.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}OriginalDeliveryQuantity').text
            materials.append(json.loads('{"Material":"'+material+'","Quantity":"'+quantity+'"}'))
        if(user_email is not None):
            Database.update("delivery",{"user_email":user_email},{"materials":materials})
            return True
        else:
            return False


    @staticmethod
    def fetchUsers(email):
        users=Database.find("users",{})
        return users
    
    @staticmethod
    def login_valid(email,password):
        admin=Admin.get_by_email(email)
        if admin is not None:
            print(admin.email)
            if(admin.password==password):
                session['adminname']=admin.name
                return admin.name
        return None


    @classmethod
    def register(cls,name,email,password):
        admin=cls.get_by_email(email)
        if admin is None:
            new_admin=cls(email,password,name)
            new_admin.save_to_mongo()
            session['adminemail']=email
            session['adminname']=name
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['adminemail']=user_email



    @staticmethod
    def logout():
        session['adminemail']=None


    def json(self):
        return {
            "email":self.email,
            "_id":self._id,
            "printdata":self.printdata,
        "password":self.password,
        "name":self.name
        }

    def save_to_mongo(self):
        Database.insert("admin",self.json())