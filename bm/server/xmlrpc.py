# register XML-RPC functions
from bm.django_xmlrpc.decorators import xmlrpc_func, permission_required
from bm.server.models import User, Map, Message, Ship, ShipModel, Upgrade,\
    UserProfile
from django.db import models
from django.db.models.manager import Manager

def resolve_dotted_attribute(obj, attr, value_to_set = None):
    """resolve_dotted_attribute(a, 'b.c.d') => a.b.c.d"""
    attrs = attr.split('.')

    for i in attrs:
        last_obj = obj
        obj = getattr(last_obj, i)
        
    if value_to_set is not None:
        return setattr(last_obj, i, value_to_set)
    
    return obj

def getPublicFields(model, max_level = 1):
    if isinstance(model, models.Model):
        if max_level:
            return {field.split(".")[-1]:getPublicFields(resolve_dotted_attribute(model, field), max_level-1) for field in ("id",)+model.PUB_FIELDS}
        else:
            return {"id":str(model.id), "name": str(model)}
    elif isinstance(model, Manager):
        return getObjectList(model.all())
    else:
        return model

def setPublicFields(model, data):
    for field in model.RW_FIELDS:
        short_name = field.split(".")[-1]
        if short_name in data:
            resolve_dotted_attribute(model, field, data[short_name])
    
    model.save()
    return True

def getObjectList(objects):
    return [{"id":str(object.id), "name": str(object)} for object in objects]


####################
## User functions
####################
@xmlrpc_func(returns='int', category="User")
def CreateUser(username, email, password):
    """Create new user.
    
    @return: New user ID"""
    newUser = User.objects.create_user(username, email, password)
    newUser.save()
    return newUser.id

@permission_required()
@xmlrpc_func(returns='bool', category="User")
def deleteUser(user):
    """Delete user account
    
    @return: True if success"""
    return user.delete()

@permission_required()
@xmlrpc_func(returns='bool', category="User")
def setUserPassword(user, new_pass):
    """Set new user password
    
    @return: True if success"""
    return user.set_password(new_pass)

@permission_required()
@xmlrpc_func(returns='array', category="User")
def getUserDetail(user):
    """Get detailed information of my account
    
    @return: dictionary of information"""
    return getPublicFields(user.get_profile())

@permission_required()
@xmlrpc_func(returns='bool', category="User", args=["array"])
def setUserDetail(user, data):
    """Set detailed information of my account
    
    @return: True if success"""
    ret = setPublicFields(user.get_profile(), data)
    user.save()
    return ret


######################
## Messaging functions
######################

@permission_required()
@xmlrpc_func(returns='bool', category="Messaging", args = ["int", "string", "string"])
def sendMessage(user, user_to, subject, text):
    """Send message to user @user_to
    
    @return: True if success"""
    message = Message.objects.create(user_from = user, user_to = User.objects.get(id=user_to), 
                                  subject = subject, text = text)
    message.save()
    return True

@permission_required()
@xmlrpc_func(returns='array', category="Messaging", args=["bool"])
def listMessages(user, only_new = True):
    """Return list of all messages to user
    
    @param only_new: If True, return only not viewed messages
    @return: list of messages"""
    messages = Message.objects.filter(user_to=user).only("id")
    if only_new:
        messages = messages.filter(viewed=False)
    
    return getObjectList(messages.all())
    
@permission_required()
@xmlrpc_func(returns='array', category="Messaging", args=["int"])
def getMessageDetail(user, message_id):
    """Return complete message
    
    @return: detailed message"""
    message = Message.objects.get(id=message_id, user_to=user)
    ret = getPublicFields(message)
    if not message.viewed:
        message.viewed = True
        message.save()
        
    return ret


######################
## Ship management
######################

@permission_required()
@xmlrpc_func(returns='array', category="Ships")
def listShips(user):
    """Return list of players ships
    
    @return: array of ships"""
    return getObjectList(Ship.objects.filter(user=user).only("id"))

@permission_required()
@xmlrpc_func(returns='array', category="Ships", args=["int"])
def getShipDetail(user, ship_id):
    """Return detailed information about ship
    
    @return: array of details"""
    return getPublicFields(Ship.objects.get(id=ship_id, user=user))

@permission_required()
@xmlrpc_func(returns='bool', category="Ships", args=["int", "array"])
def setShipDetail(user, ship_id, data):
    """Set detailed information of ship
    
    @return: True if success"""
    return setPublicFields(Ship.objects.get(id=ship_id, user=user), data)

@permission_required()
@xmlrpc_func(returns='int', category="Ships", args=["int", "string"])
def buyShip(user, model_id, name = None):
    """Buy new ship
    
    @param model_id: ID of ship model to buy 
    @param name: Name of new ship
    @return: ID of new ship"""
    model = ShipModel.objects.get(id=model_id)
    user.get_profile().spentMoney(model.price)
    newShip = Ship.objects.create(user=user, name = (name if name else model.name))
    newShip.save()
    return newShip.id

@permission_required()
@xmlrpc_func(returns='bool', category="Ships", args=["int", "int"])
def buyUpgrade(user, ship_id, upgrade_id):
    """Buy new upgrade to the ship
    
    @param model_id: ID of ship model to buy 
    @param name: Name of new ship
    @return: ID of new ship"""
    upgrade = Upgrade.objects.get(id=upgrade_id)
    ship = Ship.objects.get(id=ship_id, user=user)
    user.get_profile().spentMoney(upgrade.price)
    ship.upgrades.add(upgrade)
    ship.save()
    return True


######################
## Shop
######################

@xmlrpc_func(returns='array', category="Shop")
def listShipModels():
    """List all ship models available
    
    @return: Array of models"""
    return getObjectList(ShipModel.objects.all())

@xmlrpc_func(returns='array', category="Shop", args=["int"])
def getShipModelDetail(user, model_id):
    """Return detailed information about ship model
    
    @return: array of details"""
    return getPublicFields(ShipModel.objects.get(id=model_id))

@xmlrpc_func(returns='bool', category="Shop")
def listShipUpgrades():
    """List all ship upgrades available
    
    @return: Array of upgrades"""
    return getObjectList(Upgrade.objects.all())

@xmlrpc_func(returns='array', category="Shop", args=["int"])
def getShipUpgradeDetail(user, upgrade_id):
    """Return detailed information about ship upgrade
    
    @return: array of details"""
    return getPublicFields(Upgrade.objects.get(id=upgrade_id))

######################
## Players
######################

@xmlrpc_func(returns='array', category="Players", args=["array"])
def listPlayers(search_criteria):
    """List all players, filter by given @search_criteria
    
    @param search_criteria: dictionary. Every key,value pair means: search in field "key" for "value". 
    Key names can be in form of Django filter parameters - http://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups
    For example:
    search_criteria = {username__contains:"joe"} find all players containing "joe" in name
    search_criteria = {reputation__gt:5} find all players with reputation greater than 5
    @return: Array of players"""
    
    search = {}
    for field, value in search_criteria.items():
        pub_fields = list(map(lambda x:x.split(".")[-1], UserProfile.PUB_FIELDS))
        matches = [pub_field for pub_field in pub_fields if field.find(pub_field) == 0]
        if len(matches):
            search[matches[0]+field[len(matches[0]):]] =  value

    return getObjectList(User.objects.filter(**search).all())

@xmlrpc_func(returns='array', category="Players", args=["int"])
def getPlayerDetail(user, player_id):
    """Return detailed information about player
    
    @return: array of details"""
    return getPublicFields(User.objects.get(id=player_id))

@xmlrpc_func(returns='array', category="Players", args=["int"])
def ratePlayer(user, player_id, positive = True):
    """Return detailed information about player
    
    @return: array of details"""
    return getPublicFields(User.objects.get(id=player_id))

######################
## Maps
######################

@permission_required()
@xmlrpc_func(returns='array', category="Maps", args = ["int"])
def getMapDetails(map_id):
    """Get detailed information of map
    
    @return: dictionary of information"""
    return getPublicFields(Map.objects.get(id=map_id))


@xmlrpc_func(returns='string', args=['string'])
def test_xmlrpc(text):
    """Simply returns the args passed to it as a string"""
    return "Here's a response! %s" % str(text)
