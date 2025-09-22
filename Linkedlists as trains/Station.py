class Station:

    def __init__(self, name: str) -> None:
        """ Partial constructor. New stations are created with their next
        pointer set to None. The pointer is updated by the user."""
        self._name = name
        self._next: "Station" | None = None

    def set_next(self, next_station: "Station") -> None:
        """Mutator for next pointer."""
        self._next = next_station

    def get_next(self) -> "Station" | None:
        """Accessor for next station."""
        return self._next

    def get_name(self) -> str:
        """Accessor for the name of the station."""
        return self._name

    def has_next(self) -> bool:
        """Predicate accessor for next station"""
        return self._next is not None
