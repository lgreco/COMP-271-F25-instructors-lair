from Station import Station

# 1234567890123456789012345678901234567890123456789012345678901234567890123456789


class AmericanTrainLine:

    def __init__(self, name: str) -> None:
        """Constructor to set the name of the trainline object. Its head
        station is determined later, when we are adding stations to it."""
        self._name = name
        self._head: "Station" | None = None

    def add(self, new_station: "Station") -> None:
        """Adds a new station to the train line."""
        if self._head is None:
            # The line is empty. The new station becomes its first (head).
            self._head = new_station
        else:
            # Need to find the end of the line. Create a "traveling" station,
            # and traverse the line, following the next pointers until we
            # find a station whose next is None -- that's the last station.
            cursor: "Station" = self._head
            while cursor.has_next():
                cursor = cursor.get_next()
            # The ultimate (last) station becomes the penultimate station
            # by setting its next pointer to the new station. The new station's
            # next pointer remains null, making it the new last station
            # of the trainline
            cursor.set_next(new_station)

    def count_stations(self) -> int:
        """Returns the number of train stations in the line."""
        count: int = 0
        current: "Station" | None = self._head
        while current is not None:
            count += 1
            current = current.get_next()
        # Done
        return count

    def __len__(self) -> int:
        """Overloading len to use local metric."""
        return self.count_stations()
    
    def __str__(self) -> str:
        """Textual representation."""
        return f"{self._name}"
