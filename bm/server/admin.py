from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from bm.server.models import UserProfile, ShipModel, Upgrade,\
    Ship, Battle, ShipsInBattle, Map, Message

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class MyUserAdmin(UserAdmin):
    inlines = [UserProfileInline,]

class ShipsInBattleInline(admin.StackedInline):
    model = ShipsInBattle
    
class BattleAdmin(admin.ModelAdmin):
    inlines = [ShipsInBattleInline,]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(ShipModel)
admin.site.register(Upgrade)
admin.site.register(Ship)
admin.site.register(Battle, BattleAdmin)
admin.site.register(Map)
admin.site.register(Message)


