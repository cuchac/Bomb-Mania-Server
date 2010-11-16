from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Rating():
    def rate(self, rating):
        self.reputation=self.reputation+rating
        self.save()

# User management
class UserProfile(models.Model, Rating):
    PUB_FIELDS = ("user.id", "user.username", "user.first_name", "user.last_name", "user.email", "credit", "experience", "reputation")
    RW_FIELDS = ("user.username", "user.first_name", "user.last_name", "user.email")
    user = models.ForeignKey(User, unique=True)
    credit = models.IntegerField("Credits", default=0, help_text="Amount of credits user has available")
    experience = models.IntegerField("Experience", default=0, help_text="Numerically expressed user skills")
    reputation = models.IntegerField("Reputation", default=0, help_text="Number of positive reputation points")
    
    def __str__(self):  
        return "{0}'s profile".format(self.user);
    
    def spentMoney(self, amount):
        if amount > self.credit:
            raise Exception("Not enough credits. Needs {0} but has only {1}".format(amount, self.credit))
        self.credit-=amount
        self.save()

    
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
        UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User) 
    

## Attributes
class ShipAttributes(models.Model):
    PUB_FIELDS = ("weight", "speed", "acceleration", "sockets", "bombs")
 
    weight = models.IntegerField("Weight", default=100, help_text="Weight of the ship alone")
    speed = models.IntegerField("Speed", default=10, help_text="Maximum speed of the ship")
    acceleration = models.IntegerField("Acceleration", default=1, help_text="Acceleration of the ship")
    sockets = models.IntegerField("Sockets", default=0, help_text="Number of available sockets for upgrades")
    bombs = models.IntegerField("Bombs", default=1, help_text="Number of bombs ship can plant")
    bombRange = models.IntegerField("Bomb Range", default=1, help_text="Range of bombs explosion")

## Players ships and upgrades
class ShipModel(ShipAttributes):
    PUB_FIELDS = ("name", "price", "image") + ShipAttributes.PUB_FIELDS
    LIST_FIELDS = ("name", "price", "image")
    name = models.CharField("Model Name", default="", max_length=30, help_text="Name of ship model")
    price = models.IntegerField("Price", default=0, help_text="Price of the ship")
    image = models.FileField("Model Image", help_text="Image of the ship", upload_to="server/ship_models", null=True, blank=True)
    
    def __str__(self):
        return self.name
 
class Upgrade(ShipAttributes):
    PUB_FIELDS = ("name", "description", "price") + ShipAttributes.PUB_FIELDS

    name = models.CharField("Name", default="", max_length=30, help_text="Name of upgrade")
    description = models.TextField("Description", default="", help_text="Detailed description of upgrade")
    price = models.IntegerField("Price", default=0, help_text="Price of upgrade")
    
    def __str__(self):
        return self.name

class Ship(ShipAttributes):
    PUB_FIELDS = ("user", "model", "name", "experience", "upgrades") + ShipAttributes.PUB_FIELDS
    LIST_FIELDS = ("user", "name", "model")
    RW_FIELDS = ("name")
    user = models.ForeignKey(User, related_name="ships", unique=True)
    model = models.ForeignKey(ShipModel, default="", verbose_name="Ship model", help_text="Model of the ship")
    name = models.CharField("Ship Name", default="", max_length=30, help_text="Users name for the ship")
    experience = models.IntegerField("Experience", default=0, help_text="Numerically expressed ships experience")
    upgrades = models.ManyToManyField(Upgrade, verbose_name="Upgrades", blank=True, help_text="Upgrades mounted on the ship")

    def __str__(self):
        return self.name

## Battles and players in them
class Battle(models.Model):
    PUB_FIELDS = ("date", "ships", "map", "rounds")
    LIST_FIELDS = ("date", "map", "rounds")

    date = models.DateTimeField("Date", auto_now_add=True, help_text="Date and time of battle")
    ships = models.ManyToManyField(Ship, related_name="battles", through="ShipsInBattle", verbose_name="ShipsInBattle", help_text="Ships playing the battle")
    map = models.ForeignKey("Map", verbose_name="Battle Map", help_text="Map used for battle")
    rounds = models.IntegerField("Rounds", default=5, help_text="Number of rounds the battle had")
    
    def __str__(self):
        return "Battle #{0}".format(str(self.id))
    
    def setResults(self, results):
        '''Set result of battle. Check the consistency of input data. Confirm the correct results
        
        @param results: array of {ship_id:x, kills:x, lives:x} dictionaries
        '''
        sum_kills = 0
        sum_lives = 0

        for result in results:
            if "ship_id" not in result or "kills" not in result or "lives" not in result:
                raise Exception("Missing values in ship_results dictionary")
            
            if result["lives"] > self.rounds or result["kills"] > (self.rounds*len(self.ships)):
                raise Exception("Inconsistent results")
            
            sum_lives += result["lives"]
            sum_kills += result["kills"]
            
            ship = self.ships.through.objects.get(ship__id=result["ship_id"])
            
            if ship.confirmed:
                if ship.kills != int(result["kills"]) or ship.lives != int(result["lives"]):
                    ship.confirmed = ship.confirmed - 1
                    if ship.confirmed > 0:
                        continue
                else:
                    ship.confirmed = ship.confirmed + 1
                    continue

            ship.kills = int(result["kills"])
            ship.lives = int(result["lives"])
            ship.confirmed = ship.confirmed + 1
            
        if (sum_kills + sum_lives) != self.rounds*len(self.ships):
            raise Exception("Inconsistent results!")
        
        self.save()
            
        return True

class ShipsInBattle(models.Model):
    PUB_FIELDS = ("ship", "ship.user", "position", "kills", "lives")
    
    ship = models.ForeignKey(Ship)
    battle = models.ForeignKey(Battle)
    position = models.IntegerField("Position", default=0, help_text="Final player position in battle")
    kills = models.IntegerField("Kills", default=0, help_text="How many opponents player killed")
    lives =  models.IntegerField("Lives", default=0, help_text="How many lives has player after battle")
    confirmed = models.IntegerField("Confirmed", default=0, help_text="How many users confirmed results of the match?")
    user_confirmed = models.BooleanField("User Confirmed", default=False, help_text="Does the owner of this ship confirmed the results?")
    
    class Meta:
        unique_together = (("ship", "battle"),)

## Maps
class Map(models.Model, Rating):
    PUB_FIELDS = ("name", "players", "reputation", "image")
    LIST_FIELDS = ("name", "players", "reputation", "image")
    
    name = models.CharField("Map Name", default="", max_length=30, help_text="Name of the map")
    players = models.IntegerField("Players", default=2, help_text="Maximum number of players in map")
    reputation = models.IntegerField("Reputation", default=0, help_text="Number of positive reputation points")
    image = models.FileField("Map Image", help_text="Image of the map", upload_to="server/maps", null=True, blank=True)
    
    def __str__(self):
        return self.name
    
## Messaging
class Message(models.Model):
    PUB_FIELDS = ("user_from", "user_to", "subject", "text", "viewed", "date")
    LIST_FIELDS = ("user_from", "user_to", "subject", "viewed", "date")
    
    user_from = models.ForeignKey(User, related_name="+", verbose_name="User From", help_text="Sender of this message")
    user_to = models.ForeignKey(User, related_name="+", verbose_name="User To", help_text="Receiver of this message")
    subject = models.TextField("Subject", default="", help_text="Subject of the message")
    text = models.TextField("Text", default="", help_text="Body of the message")
    viewed = models.BooleanField("Viewed", default=False, help_text="Whether this message was viewed by receiver")
    date = models.DateTimeField("Date", auto_now_add=True, help_text="Date message was sent")
    
    def __str__(self):
        return "Message #{0}".format(str(self.id))