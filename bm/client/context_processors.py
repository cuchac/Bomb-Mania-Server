from bm.client.menu import Menu
from bm.client.views import MENU

def menu(request):
    if request.path[:6] == "/ajax/":
        return {}
    
    return {'menu' : Menu(MENU)}
