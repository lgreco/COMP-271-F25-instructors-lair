from Arya import *

class Oberyn(Arya):
    def b(self):
        print('Oberyn-b')
        super().b()

    def __str__(self):
        return 'Oberyn'
