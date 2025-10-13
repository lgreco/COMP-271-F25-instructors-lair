
class MyList:

    # --- Constants for __str__ ---
    _EMPTY = "List is empty"
    _OPEN_STR = "[ "
    _CLOSE_STR = " ]"
    _SEPARATOR = ", "
    # --- Default values ---
    _RESIZE_BY = 2
    _DEFAULT_SIZE = 4

    def __init__(self, maximum_size: int = _DEFAULT_SIZE):
        """Create an empty list with a fixed size block specified by parameter
        maximum_size. The object tracks how many actual elements are in the
        list using the attribute __actual_size.
        """
        # This is how many elements the list can hold
        self._maximum_size: int = maximum_size
        # This is how many actual elements are in the list
        self._actual_size: int = 0
        # This is the actual data storage
        self._data: list = [None] * maximum_size

    def __len__(self) -> int:
        """Return the number of actual elements in the list."""
        return self._actual_size

    def __str__(self) -> str:
        """Return a string representation of the list."""
        # The str representation starts with actual size and max size
        list_str = f"{self._actual_size}/{self._maximum_size}; "
        # Then, if the list is empty, we add the _EMPTY constant
        if self._actual_size == 0:
            list_str += self._EMPTY
        else:
            # The list is not empty, so we add the opening bracket and prepare
            # to add the elements. We start with the first element to avoid adding
            # a separator before it.
            list_str += f"{self._OPEN_STR}{self._data[0]}"
            for i in range(1, self._actual_size):
                # For each element after the first, we add a separator and the
                # element itself.
                list_str += f"{self._SEPARATOR}{self._data[i]}"
            # Finally, we add the closing bracket and return the string
            list_str += self._CLOSE_STR
        return list_str

    def append(self, value):
        """Append value to the end of the list, resizing if necessary."""
        # The method calls insert() to do the actual work of appending.
        # This is a common technique called "code reuse" where we use existing
        # methods to implement new functionality, avoiding code duplication.
        self.insert(self._actual_size, value)

    def _ensure_capacity(self, factor: int = _RESIZE_BY) -> None:
        """Ensure that there is space to add new elements, resizing if necessary by
        the given factor."""
        # If the actual size is equal to the maximum size, we need to resize,
        # otherwise we have enough space and no action is needed.
        if self._actual_size == self._maximum_size:
            # Resize the internal storage by the factor specified
            self._maximum_size *= factor
            # Create a new temporary list to hold the resized data
            temp = [None] * self._maximum_size
            # Copy the existing data to the new list
            for i in range(self._actual_size):
                temp[i] = self._data[i]
            # Update the internal data reference to point to the new list
            self._data = temp

    def insert(self, index: int, value) -> None:
        """Insert value at the given index, shifting elements as necessary.
        If the index is invalid, do nothing."""
        # Validate the index and proceed only if it's valid
        if 0 <= index <= self._actual_size:
            # Ensure there is enough capacity to add a new element
            self._ensure_capacity()
            # shift right (end → index)
            i = self._actual_size - 1
            while i >= index:
                self._data[i + 1] = self._data[i]
                i -= 1
            # insert the new value
            self._data[index] = value
            # Increment the actual size to reflect the addition
            self._actual_size += 1

    def remove(self, index: int):
        """Remove and return the element at the given index, shifting elements
        as necessary. If the index is invalid, return None."""
        # Initialize the variable to hold the removed value
        removed = None
        # Validate the index and proceed only if it's valid
        if index >= 0 and index < self._actual_size:
            # Retrieve the value to be removed
            removed = self._data[index]
            # Shift elements to the left to fill gap left by the removed element
            for i in range(index, self._actual_size - 1):
                self._data[i] = self._data[i + 1]
            # Clear the last position which is now a duplicate after shifting
            self._data[self._actual_size - 1] = None
            # Decrement the actual size to reflect the removal
            self._actual_size -= 1
        return removed

    def pop(self):
        """Remove and return the last element of the list. If the list is empty,
        return None."""
        # Reuse the remove() method to remove the last element
        return self.remove(self._actual_size - 1)




# --- Simple testing ---
if __name__ == "__main__":
    my_list = MyList()
    print("Initial list (should be empty):", my_list)  # 0/4; List is empty
    print("Length (should be 0):", len(my_list))       # 0

    my_list.append(10)
    print("After appending 10:", my_list)              # 1/4; [ 10 ]
    print("Length (should be 1):", len(my_list))       # 1

    my_list.insert(0, 5)
    print("After inserting 5 at index 0:", my_list)    # 2/4; [ 5, 10 ]
    print("Length (should be 2):", len(my_list))       # 2

    my_list.insert(1, 7)
    print("After inserting 7 at index 1:", my_list)    # 3/4; [ 5, 7, 10 ]
    print("Length (should be 3):", len(my_list))       # 3

    removed_value = my_list.remove(1)
    print(f"After removing value at index 1 (removed {removed_value}):", my_list)  # 2/4; [ 5, 10 ]
    print("Length (should be 2):", len(my_list))       # 2

    popped_value = my_list.pop()
    print(f"After popping last value (popped {popped_value}):", my_list)           # 1/4; [ 5 ]
    print("Length (should be 1):", len(my_list))       # 1



    ### test 2
    test = MyList(2)
    print(test)                                 # 0/2; List is empty
    test.append("Alice")
    test.append("Bob")
    test.append("Cathy")
    test.append("Derek"),
    test.append("Eve")
    print(test)                                 # 5/8; [ Alice, Bob, Cathy, Derek, Eve ]

    test.insert(2, "Frank")
    print(test)                                 # 6/8; [ Alice, Bob, Frank, Cathy, Derek, Eve ]
    print(len(test))                            # 6

    for _ in range(len(test)):
        print(test.pop())                       # Eve Derek Cathy Frank Bob Alice  (split by \n)
    print(test)                                 # 0/8; List is empty
    print(test.pop())                           # None

