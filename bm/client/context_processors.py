from bm.client.menu import Menu
from bm.client.views import MENU

def menu(request):
    if request.is_ajax():
        return {}
    
    return {'menu' : Menu(MENU)}
