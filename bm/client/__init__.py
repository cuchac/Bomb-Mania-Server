from xmlrpc import client
from django.utils.datastructures import SortedDict

class MyUnmarshaller(client.Unmarshaller):
    def end_struct(self, data):
        mark = self._marks.pop()
        # map structs to Python dictionaries
        dict = SortedDict()
        items = self._stack[mark:]
        for i in range(0, len(items), 2):
            dict[client._stringify(items[i])] = items[i+1]
        self._stack[mark:] = [dict]
        self._value = 0
        
client.Unmarshaller.dispatch["struct"] = MyUnmarshaller.end_struct
