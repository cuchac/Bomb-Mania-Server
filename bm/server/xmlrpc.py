# register XML-RPC functions
from bm.django_xmlrpc.decorators import xmlrpc_func, permission_required
from bm.server.models import User, Map, Message, Ship, ShipModel, Upgrade,\
    UserProfile, Battle
from django.db import models
from django.db.models.manager import Manager
from collections import OrderedDict
from django.db.models.fields.files import FieldFile

def resolve_dotted_attribute(obj, attr, value_to_set = None):
    """resolve_dotted_attribute(a, 'b.c.d') => a.b.c.d"""
    attrs = attr.split('.')

    for i in attrs:
        last_obj = obj
        try:
            obj = getattr(last_obj, i)
        except:
            return ""
        
    if value_to_set is not None:
        return setattr(last_obj, i, value_to_set)
    
    return obj

def getPublicFields(model, max_level = 1, fields = None):
    if isinstance(model, models.Model):
        if max_level:
            if not fields:
                fields = model.PUB_FIELDS
            fields = ("id",)+fields
            return OrderedDict([(field.split(".")[-1], getPublicFields(resolve_dotted_attribute(model, field), max_level-1)) for field in fields])
        else:
            return OrderedDict((("id", str(model.id)), ("name", str(model)), ("object", model.__class__.__name__)))
    elif isinstance(model, Manager):
        return getObjectList(model.all(), max_level-1)
    elif isinstance(model, FieldFile):
        try:
            return model.url
        except:
            return ""
    else:
        return model

def setPublicFields(model, data):
    for field in model.RW_FIELDS:
        short_name = field.split(".")[-1]
        if short_name in data:
            resolve_dotted_attribute(model, field, data[short_name])
    
    model.save()
    return True

def getObjectList(objects, max_level = 0):
    if max_level < 1:
        ret = [OrderedDict((("id",str(object.id)), ("name", str(object)), ("object",object.__class__.__name__))) for object in objects]
        if hasattr(objects.model, "LIST_FIELDS"):
            for index,object in dict(enumerate(objects)).items():
                ret[index].update(getPublicFields(object, fields=object.LIST_FIELDS))
        return ret
    else:
        return [getPublicFields(object, max_level) for object in objects]


####################
## User functions
####################
@xmlrpc_func(returns='int', category="User")
def createUser(username, email, password):
    """Create new user.
    
    @return: New user ID"""
    if User.objects.filter(username=username).exists():
        raise Exception("User already exists")
    
    newUser = User.objects.create_user(username, email, password)
    newUser.save()
    return newUser.id

@permission_required()
@xmlrpc_func(returns='bool', category="User")
def deleteUser(user):
    """Delete user account
    
    @return: True if success"""
    user.delete()
    return True

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
    return getPublicFields(user.get_profile(), fields = UserProfile.LOGGED_FIELDS)

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

@permission_required()
@xmlrpc_func(returns='bool', category="Messaging", args=["int"])
def deleteMessage(user, message_id):
    """Delete message of id=@message_id
    
    @return: true if deleted successfully"""
    Message.objects.get(id=message_id).delete()
        
    return True


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
    
    @return: dictionary of details"""
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
    return model.buyShip(user, name)

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
def getShipModelDetail(model_id):
    """Return detailed information about ship model
    
    @return: dictionary of details"""
    return getPublicFields(ShipModel.objects.get(id=model_id))

@xmlrpc_func(returns='bool', category="Shop")
def listShipUpgrades():
    """List all ship upgrades available
    
    @return: Array of upgrades"""
    return getObjectList(Upgrade.objects.all())

@xmlrpc_func(returns='array', category="Shop", args=["int"])
def getShipUpgradeDetail(upgrade_id):
    """Return detailed information about ship upgrade
    
    @return: dictionary of details"""
    return getPublicFields(Upgrade.objects.get(id=upgrade_id))

######################
## Players
######################

@xmlrpc_func(returns='array', category="Players", args=["array", "string", "int"])
def listPlayers(search_criteria = {}, order_by = "id", limit = None):
    """List all or @limit players, filter by given @search_criteria and order them by @order_by
    
    @param search_criteria: dictionary. Every key,value pair means: search in field "key" for "value". 
    Key names can be in form of Django filter parameters - http://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups
    For example: 
    search_criteria = {username__contains:"joe"} find all players containing "joe" in name
    search_criteria = {reputation__gt:5} find all players with reputation greater than 5
    @param order_by: name of field to use for sorting of result
    @param limit: return only @limit players
    @return: Array of players"""
    
    search = {}
    for field, value in search_criteria.items():
        pub_fields = list(map(lambda x:x.split(".")[-1], UserProfile.PUB_FIELDS))
        matches = [pub_field for pub_field in pub_fields if field.find(pub_field) == 0]
        if len(matches):
            search[matches[0]+field[len(matches[0]):]] =  value

    return getObjectList(User.objects.order_by(order_by).filter(**search)[:limit])

@xmlrpc_func(returns='array', category="Players", args=["int"])
def getPlayerDetail(player_id):
    """Return detailed information about player
    
    @return: dictionary of details"""
    return getPublicFields(User.objects.get(id=player_id).get_profile())

@permission_required()
@xmlrpc_func(returns='array', category="Players", args=["int", "bool"])
def ratePlayer(user, player_id, positive = True):
    """Rate players
    
    @param player_id: ID of player to rate
    @param positive: True to rate positive, False to rate negative
    @return: True if success"""
    return User.objects.get(id=player_id).get_profile().rate((1 if positive else -1))

######################
## Maps
######################

@xmlrpc_func(returns='array', category="Maps")
def listMaps():
    """Get list of available maps
    
    @return: list of maps"""
    return getObjectList(Map.objects.all())

@xmlrpc_func(returns='array', category="Maps", args = ["int"])
def getMapDetail(map_id):
    """Get detailed information of map
    
    @return: dictionary of details"""
    return getPublicFields(Map.objects.get(id=map_id))

@xmlrpc_func(returns='array', category="Maps", args = ["int"])
def downloadMap(map_id):
    """Download map
    
    @return: dictionary of details and map data"""
    map = Map.objects.get(id=map_id)
    mapDetail = getPublicFields(map)
    mapDetail["data"] = "MAP_DATA_FILE"
    return mapDetail

@xmlrpc_func(returns='array', category="Maps", args = ["int"])
def uploadMap(name, number_of_players, mapData):
    """Upload new map
    
    @return: ID of uploaded map"""
    newMap = Map.objects.create(name=name, players=number_of_players)
    newMap.save()
    return newMap.id

@permission_required()
@xmlrpc_func(returns='array', category="Maps", args=["int", "bool"])
def rateMap(user, map_id, positive = True):
    """Rate map
    
    @param map_id: ID of map to rate
    @param positive: True to rate positive, False to rate negative
    @return: True if success"""
    return Map.objects.get(id=map_id).rate((1 if positive else -1))

######################
## Battles
######################

@xmlrpc_func(returns='array', category="Battles")
def listBattles():
    """List all played battles
    
    @return: Array of battles"""
    return getObjectList(Battle.objects.all())

@xmlrpc_func(returns='array', category="Battles", args=["int"])
def getBattleDetail(battle_id):
    """Return detailed information about battle
    
    @return: dictionary of details"""
    battle = Battle.objects.get(id=battle_id)
    ret = getPublicFields(battle)
    print("Battle ships:",battle.ships.through.objects.filter(battle=battle).all())
    ret["result"] = getObjectList(battle.ships.through.objects.filter(battle=battle), 1)
    print(ret)
    return ret

@xmlrpc_func(returns='bool', category="Battles")
def listPlayerBattles(player_id):
    """List all battles that player already encountered
    
    @return: Array of battles"""
    return getObjectList(Battle.objects.filter(ships__user=player_id).all())

@permission_required()
@xmlrpc_func(returns='int', category="Battles", args=["array", "int", "int"])
def announceBattle(user, ship_ids, map_id, rounds):
    """Announce creation of new battle. @ship_ids are participating in the battle.
    
    @param ship_ids: array of ships IDs
    @param map_id: ID of used map
    @param rounds: number of rounds of battle
    @return: ID of created battle"""
    if len(ship_ids) < 2:
        raise Exception("Too few players")
    
    ships = [Ship.objects.get(id=ship_id) for ship_id in ship_ids]
    
    map = Map.objects.get(id=map_id)
    
    newBattle = Battle.objects.create(ships=ships, map=map, rounds=rounds)
    newBattle.save()
    return newBattle.id

@permission_required()
@xmlrpc_func(returns='bool', category="Battles", args=["array"])
def confirmBattle(user, battle_id, results):
    """Confirm results of battle.
    
    @param battle_id: ID of battle
    @param results: array containing dictionaries of ship_id, lives and kills for each ship in battle.
    Example: results = [{ship_id:5, kills:2, lives:0}, {ship_id:2, kills:5, lives:3}]
    @return: True if results was confirmed"""
    if len(results) < 2:
        raise Exception("Too few results")
    
    battle = Battle.objects.get(id = battle_id)
    
    owner_ship = battle.ships.through.objects.get(ship__user = user)
    
    if owner_ship.user_confirmed:
        raise Exception("Already confirmed results!")
    
    owner_ship.user_confirmed = True

    return battle.setResults(results)

######################
## Testing
######################

@xmlrpc_func(returns='string', args=['string'])
def test_xmlrpc(text):
    """Simply returns the args passed to it as a string"""
    return "Here's a response! %s" % str(text)
