from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime
from typing import Union
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError

from users import Users

Base = declarative_base()

class Friend(Base):
    __tablename__ = 'friend'
    uid = Column(Integer, primary_key=True)
    friend_id = Column(Integer, primary_key=True)

    def __init__(self, uid, friend_id):
        self.uid = uid
        self.friend_id = friend_id

    def __str__(self):
        return (f"friend(uid='{self.uid}', friend_id='{self.friend_id}')")
    
    '''
    TODO need to be able to unfollow/unfriend users. Need to be able to search for users
    to friend via email. Will still keep friend search via username because that seems useful.
    '''
    
    @classmethod
    def friend_user(cls, session, uid):
        # Need to update to allow search by email
        friending = True
        
        while(friending):
            friending = input("Who do you want to friend? ")
            try:
                friendResult, fcount = Users.search(session, username=friending)
                reply = input("Do you want to friend " + friendResult[0].username + "? [Y/N] ")
                if(reply == "Y" or reply == "YES"):
                    new_friend = cls(uid = uid, friend_id = friendResult[0].uid)
                    session.add(new_friend)
                    session.commit()
                    print("Friended " + friendResult[0].username + "!")
            except IntegrityError as e:
                print("Already friends with user!")
            except Exception as e:
                print("User does not exist!")
            again = input("Do you want to friend someone else? [Y/N] ")
            if(again=="N" or again=="NO"):
                friending = False

    @classmethod
    def unfriend(cls, session, uid):
        unfriending = input("Who would you like to unfriend? ")
        try:
            friendresult, fcount = Users.search(session, username=unfriending)
            fid = friendresult[0].uid
            confirm = input("Do you wish to unfriend " + friendresult[0].username + " ? [Y/N] ")
            if(confirm == "Y" or confirm == "YES"):
                query = session.query(Friend)
                query = query.filter(Friend.uid == uid)
                query = query.filter(Friend.friend_id == fid)

                session.delete(query[0])
                session.commit()
        except Exception as e:
            #print(e)
            print("User does not exist!")