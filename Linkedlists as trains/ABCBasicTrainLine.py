from abc import ABC, abstractmethod
from Station import Station  # for type hint consistency


class ABCBasicTrainLine(ABC):
    """
    Abstract interface for a singly linked train line of Station nodes.
    Subclasses must implement all methods below.

    Conventions:
      - "head" is position 0
      - Methods that mention "Station" accept either a Station instance
        or a station name string when noted in the docstring.
    """

    @abstractmethod
    def __init__(self, name: str):
        """Initialize an empty line with the given name."""

    # ----- core mutators / accessors -----

    @abstractmethod
    def add(self, new_station: "Station" | str):
        """
        Append a station to the end.
        Accepts either a Station instance or a station-name string.
        Should run in O(1) when a tail pointer is maintained.
        """

    @abstractmethod
    def count_stations(self) -> int:
        """
        Return the number of stations on the line.
        May return a cached count (O(1)).
        """

    # ----- python dunders -----

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of stations (enables len(line))."""

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-friendly summary string."""

    @abstractmethod
    def __bool__(self) -> bool:
        """Return True iff the line is non-empty."""
