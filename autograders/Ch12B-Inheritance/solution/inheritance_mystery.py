from Arya import *
from Oberyn import *
from Brienne import *
from Tyrion import *

def main():
    thrones = [Oberyn(), Arya(), Brienne(), Tyrion()]
    #for each of the object above show the results of their behaviors
    for i in range(len(thrones)):
        print('Element', i)
        thrones[i].a()          #call the a method
        print()
        print(thrones[i])       #uses __str__
        print()
        thrones[i].b()          #call the b method
        print('Done')
        print()

main()
