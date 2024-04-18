from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError

from users import Users

Base = declarative_base()

class Friend(Base):
    '''
    Defines friend
    '''
    __tablename__ = 'friend'
    uid = Column(Integer, primary_key=True)
    friend_id = Column(Integer, primary_key=True)
    '''
    friend constructor
    '''
    def __init__(self, uid, friend_id):
        self.uid = uid
        self.friend_id = friend_id
    '''
    To-string for friend
    '''
    def __str__(self):
        return (f"friend(uid='{self.uid}', friend_id='{self.friend_id}')")
    
    '''
    Creates a new entry in the friend table where the current user is the uid and
    the person they are following is the friend_id
    '''
    @classmethod
    def friend_user(cls, session, uid):
        friending = True
        uore = True
        
        while(friending):
            while(uore):
                user_or_email = input("Do you want to search by username or by email? ")
                if(user_or_email != "email" and user_or_email != "username"):
                    print("Please specify either username or email")
                else:
                    uore = False

            friending = input("Who do you want to friend? ")
            try:
                if(user_or_email == "email"):
                    friendResult, fcount = Users.search(session, email=friending)
                elif (user_or_email=="username"):
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
    '''
    Deletes an entry in the friend table where the current user is
    the uid and the person they are unfollowing is the friend_id
    '''
    @classmethod
    def unfriend(cls, session, uid):
        uore = True
        while(uore):
                user_or_email = input("Do you want to search by username or by email? ")
                if(user_or_email != "email" and user_or_email != "username"):
                    print("Please specify either username or email")
                else:
                    uore = False
        unfriending = input("Who would you like to unfriend? ")
        try:
            if(user_or_email == "email"):
                friendresult, fcount = Users.search(session, email=unfriending)
            elif(user_or_email == "username"):
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
    '''
    List all users that the current user is following/has friended.
    '''
    def listFriends(session, uid):
        query = session.query(Friend)
        query = query.filter(Friend.uid == uid)

        count = query.count()
        if(count == 0):
            print("You don't follow anyone!")
        else:
            for entry in query:
                friendName, fcount = Users.search(session, uid=entry.friend_id)
                print(friendName[0].username)
        print("\nFolliwng: " + str(count))
        queryFollow = session.query(Friend)
        queryFollow = queryFollow.filter(Friend.friend_id == uid)
        countFollow = queryFollow.count()
        print("Followers: " + str(countFollow))
