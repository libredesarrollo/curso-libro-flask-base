# from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_

from my_app.auth import models
from my_app import db

def getById(id: int, show404=False):
    if show404:
        user = models.User.query.get_or_404(id)
    else:
        user = db.session.query(models.User).get(id)

    return user

def update(user):
    userdb = getById(id=user.id)

    userdb.first_name = user.first_name
    userdb.last_name = user.last_name
    userdb.email = user.email
    userdb.address_id = user.address_id
    userdb.avatar_id = user.avatar_id
    userdb.pwdhash = user.pwdhash
 
    db.session.add(userdb)
    db.session.commit()
    db.session.refresh(userdb)
    return userdb


#address
def getByIdAddress(id: int, show404=False):
    if show404:
        address = models.Address.query.get_or_404(id)
    else:
        address = db.session.query(models.Address).get(id)

    return address

def createAddress(address):
    addressdb = models.Address(address=address)
    db.session.add(addressdb)
    db.session.commit()
    db.session.refresh(addressdb)
    return addressdb

def updateAddress(id:int ,address: str):
    addressdb = getByIdAddress(id=id)

    addressdb.address = address

    db.session.add(addressdb)
    db.session.commit()
    db.session.refresh(addressdb)
    return addressdb

# social red
def getAllSocialNetwork():
    socialNetworks = db.session.query(models.SocialNetwork).all()
    return socialNetworks

def getSocialNetworkByUserId(userId: int):
    socialNetworks = db.session.query(models.UserSocialNetwork).filter(models.UserSocialNetwork.user_id == userId).all()
    return socialNetworks

def getSocialNetworkByUserIdAndSocialRedId(userId: int, socialNetworkId: int):
    socialNetwork = db.session.query(models.UserSocialNetwork).filter(and_(models.UserSocialNetwork.user_id == userId, models.UserSocialNetwork.social_network_id == socialNetworkId)).first()
    return socialNetwork

def saveSocialNetwork(userId: int, socialNetworkId: int, url: str):
    socialNetwork = getSocialNetworkByUserIdAndSocialRedId(userId=userId, socialNetworkId=socialNetworkId)

    if socialNetwork is None:
        # create
        createSocialNetwork(userId=userId,socialNetworkId=socialNetworkId,url=url)
    else:
        #update
        updateSocialNetwork(userId=userId,socialNetworkId=socialNetworkId,url=url)

def createSocialNetwork(userId: int, socialNetworkId: int, url: str):
    userSocialNetwork = models.UserSocialNetwork()
    userSocialNetwork.user_id = userId
    userSocialNetwork.social_network_id = socialNetworkId
    userSocialNetwork.url = url

    db.session.add(userSocialNetwork)
    db.session.commit()
    db.session.refresh(userSocialNetwork)
    return userSocialNetwork

def updateSocialNetwork(userId: int, socialNetworkId: int, url: str):
    userSocialNetwork = getSocialNetworkByUserIdAndSocialRedId(userId=userId, socialNetworkId=socialNetworkId)
    userSocialNetwork.url = url

    db.session.add(userSocialNetwork)
    db.session.commit()
    db.session.refresh(userSocialNetwork)
    return userSocialNetwork

def deleteSocialNetwork(userId: int, socialNetworkId: int):
    userSocialNetwork = getSocialNetworkByUserIdAndSocialRedId(userId=userId, socialNetworkId=socialNetworkId)
    if userSocialNetwork is not None:
        db.session.delete(userSocialNetwork)
        db.session.commit()