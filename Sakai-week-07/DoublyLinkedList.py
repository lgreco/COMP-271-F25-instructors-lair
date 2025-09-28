from Node import Node

class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        nodes = []
        current = self.head
        while current is not None:
            nodes.append(str(current))
            current = current.get_next()
        return " <-> ".join(nodes)

    def is_empty(self):
        return self.size == 0

    def get_size(self):
        return self.size

    def add_to_back(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            new_node.set_prev(self.tail)
            self.tail.set_next(new_node)
        self.tail = new_node
        self.size += 1
    
    def add_to_front(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.tail = new_node
        else:
            new_node.set_next(self.head)
            self.head.set_prev(new_node)
        self.head = new_node
        self.size += 1