class Arya:
    def a(self):
        print('Arya-a')

    def b(self):
        self.a()
        print('Arya-b')

    def __str__(self):
        return 'Arya'

        
