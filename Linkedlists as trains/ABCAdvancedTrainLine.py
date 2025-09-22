from abc import ABC, abstractmethod
from Station import Station # for type hint consistency


class ABCAdvanvedTrainLine(ABC):
    """
    Abstract interface for a singly linked train line of Station nodes.
    Subclasses must implement all methods below.
    """

    @abstractmethod
    def list_stations(self) -> list[str] | None:
        """
        Return a Python list of station names, in order of appearance
        from head to tail.
        """

    @abstractmethod
    def find_middle(self) -> "Station" | None:
        """
        Return the middle Station using the classic fast/slow cursor method.
        If the line has even length, return the first of the two middle stations.
        Return None if the line is empty.
        """

    @abstractmethod
    def delete(self, index:int) -> "Station" | None:
        """
        Remove and return the Station at position 'index' (head is 0).
        Raise IndexError if index is out of bounds.
        Should update head/tail/count appropriately.
        """

    @abstractmethod
    def index_of(self, name: str) -> int:
        """
        Return the zero-based index of the first station that matches
        the given Station name string.
        Return -1 if not found.
        """

    @abstractmethod
    def exists(self, name: str) -> bool:
        """
        Return True iff a station with the given name exists on the line.
        """

    @abstractmethod
    def has_loop(self) -> bool:
        """
        Return True iff the line contains a cycle (loop) reachable from head.
        (Floyd’s cycle-finding algorithm is a typical implementation.)
        """
