import datetime
import uuid

from flask import session

from src.common.database import Database


class User(object):

    def __init__(self,email,password,name=None,_id=None,printdata="no",currentCart=0):
        self.email=email
        self.password=password
        self.name=name
        self._id=uuid.uuid4().hex if _id is None else _id
        self.printdata=printdata
        self.currentCart=currentCart

    @classmethod
    def get_by_email(cls,email):
        data=Database.find_one("users",{"email":email})
        if data is not None:
            return cls(**data)


    @classmethod
    def get_by_id(cls,_id):
        data=Database.find_one("users",{"_id":_id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email,password):
        user=User.get_by_email(email)
        if user is not None:
            print(user.email)
            if(user.password==password):
                return user.name
        return None


    @classmethod
    def register(cls,name,email,password):
        user=cls.get_by_email(email)
        if user is None:
            new_user=cls(email,password,name)
            new_user.save_to_mongo()
            session['email']=email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email']=user_email


    @staticmethod
    def logout():
        session['email']=None


    def json(self):
        return {
            "email":self.email,
            "_id":self._id,
            "printdata":self.printdata,
        "password":self.password,
        "name":self.name
        }

    def save_to_mongo(self):
        Database.insert("users",self.json())