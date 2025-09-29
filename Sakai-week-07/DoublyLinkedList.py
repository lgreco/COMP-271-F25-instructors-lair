from Node import Node

class DoublyLinkedList:

    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__size = 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        nodes = []
        current = self.__head
        while current is not None:
            nodes.append(str(current))
            current = current.get_next()
        return " <-> ".join(nodes)

    def is_empty(self):
        return self.__size == 0

    def get_size(self):
        return self.__size

    def add_to_back(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.__head = new_node
        else:
            new_node.set_prev(self.__tail)
            self.__tail.set_next(new_node)
        self.__tail = new_node
        self.__size += 1
    
    def add_to_front(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.__tail = new_node
        else:
            new_node.set_next(self.__head)
            self.__head.set_prev(new_node)
        self.__head = new_node
        self.__size += 1
