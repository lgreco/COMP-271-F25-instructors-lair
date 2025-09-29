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

    def find_middle(self):
        """Returns the middle node of the list. If the list has an even number of nodes,
        the second middle node is returned.
        """
        # Prepare an empty variable to hold the middle node
        middle_node = None
        # Check if the list is empty, and if so return the None object
        if not self.is_empty():
            # Set two pointers, one starting at the head and the other at the tail
            forward = self.head
            backward = self.tail
            # Move the pointers toward each other until they meet or cross
            while forward != backward and forward.get_next() != backward:
                forward = forward.get_next()
                backward = backward.get_prev()
            middle_node = forward
        return middle_node

    def has_loop(self) -> bool:
        """Returns True if the list has a loop, False otherwise."""
        loop = False
        if not self.is_empty():
            slow = self.head
            fast = self.head
            while fast.has_next() and fast.get_next().has_next() and not loop:
                slow = slow.get_next()
                fast = fast.get_next().get_next()
                loop = slow == fast
        return loop
    
