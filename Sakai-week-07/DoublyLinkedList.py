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

    def has_gap_backward(self):
        """Returns True if there is a gap between the forward and backward pointers."""
        has_gap = False
        if not self.is_empty():
            cursor = self.__head
            while cursor is not None and cursor.has_next() and not has_gap:
                next = cursor.get_next
                has_gap = ( next.get_prev() != cursor)
                cursor = next
        return has_gap
    
    def has_gap_forward(self):
        has_gap = False
        if not self.is_empty():
            cursor = self.__tail
            while cursor is not None and cursor.has_prev() and not has_gap:
                prev = cursor.get_prev()
                has_gap = (prev.get_next() != cursor)
                cursor = prev
        return has_gap