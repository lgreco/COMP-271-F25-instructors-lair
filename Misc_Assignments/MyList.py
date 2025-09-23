# Starter code for MyList


class MyList:

    _EMPTY = "List is empty"
    _RESIZE_BY = 2

    def __init__(self, maximum_size: int = 4):
        """Create an empty list with a fixed size block specified by parameter
        maximum_size. The object tracks how many actual elements are in the list
        using the attribute __actual_size.
        """
        self._maximum_size: int = maximum_size
        self.__actual_size: int = 0
        self._data: list = [None] * maximum_size

    def __len__(self) -> int:
        pass

    def __str__(self) -> str:
        pass

    def append(self, value) -> None:
        pass

    def insert(self, index: int, value) -> None:
        pass

    def remove(self, index: int):
        pass

    def pop(self):
        pass


# --- Simple testing ---
if __name__ == "__main__":
    my_list = MyList()
    # Write tests using this object to verify your methods work correctly.
