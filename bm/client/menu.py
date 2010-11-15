from django.core.urlresolvers import reverse

class Menu(list):
    '''
    Deadly simple Menu class
    '''


    def __init__(self, menu_structure):
        '''
        Create menu structure
        
        @param menu_structure: tuple of pairs (name, view)
        '''
        for item in menu_structure:
            self.append({'name':item[0], 'url':reverse(item[1])})
        