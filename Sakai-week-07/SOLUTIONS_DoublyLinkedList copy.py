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

    def find_middle(self):
        """Returns the middle node of the list. If the list has an even number of nodes,
        the second middle node is returned.
        """
        # Prepare an empty variable to hold the middle node
        middle_node = None
        # Check if the list is empty, and if so return the None object
        if not self.is_empty():
            # Set two pointers, one starting at the head and the other at the tail
            forward = self.__head
            backward = self.__tail
            # Move the pointers toward each other until they meet or cross
            while forward != backward and forward.get_next() != backward:
                forward = forward.get_next()
                backward = backward.get_prev()
            middle_node = forward
        return middle_node

    def has_loop(self) -> bool:
        """Returns True if the list has a loop, False otherwise."""
        return (
            self.__head is not None
            and self.__tail is not None
            and self.__head.get_prev() == self.__head
            and self.__tail.get_next() == self.__tail
        )
