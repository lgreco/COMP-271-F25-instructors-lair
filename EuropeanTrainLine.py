from Station import Station

# 1234567890123456789012345678901234567890123456789012345678901234567890123456789


class EuropeanTrainLine:

    """A more versatile trainline class with faster operations that reduce the times
    we need to traverse the object to find the last station, either because we 
    need to add a new station to the end or to count the number of stations."""

    _SINGULAR = "station"
    _PLURAL = _SINGULAR + "s"
    _EMPTY = _PLURAL

    def __init__(self, name: str) -> None:
        """Constructor to set the name of the trainline object. Its head
        station is determined later, when we are adding stations to it."""
        self._name = name
        self._head: "Station" | None = None
        self._tail: "Station" | None = None
        self._count: int = 0

    def add(self, new_station: "Station"|str) -> None:
        """Adds a new station to the train line. The method accepts string or
        station objects as inputs and acts accordingly."""
        if isinstance(new_station, str):
            # Input is a string. Using the string to create a new Station object
            # with the string as the station's name. 
            # DISCUSS IN CLASS: In Python, we can’t truly overload methods by signature
            # like in Java or C++. Instead, we make the method flexible enough to accept 
            # multiple types and handle them appropriately.
            new_station = Station(new_station)
        # At this point, new_station is a Station object. Let's add it to the line.
        if self._head is None:
            # The line is empty. The new station becomes its first (head).
            self._head = new_station
        else:
            # Since we know where the last station is we don't need to traverse
            # down the line seeking it. Just update the last station's next pointer.
            self._tail.set_next(new_station)
        # The new station just added becomes the new tail for the line
        self._tail = new_station
        # Just out of abundance of caution, ensure _tail's next is None
        self._tail.set_next(None)
        # Update the count of stations in the line.
        self._count += 1

    def count_stations(self) -> int:
        """Returns the number of train stations in the line. Because the count is a
        class field that is updated every time we add a train station, there is no
        need to traverse down the line counting stations."""
        return self._count

    def __len__(self) -> int:
        """Overloading len to use local metric."""
        return self.count_stations()
    
    def __str__(self) -> str:
        """Textual representation."""
        if self._count == 0:
            textual = self._EMPTY
        elif self._count == 1:
            textual = self._SINGULAR
        else: 
            textual = self._PLURAL
        return f"{self._name} has {self._count} {textual}"
    
    def __bool__(self) -> bool:
        return self._count > 0