from abc import ABC, abstractmethod


class ABCSuperiorTrainLine(ABC):
    """
    Abstract interface for a singly linked train line of Station nodes.
    Subclasses must implement all methods below.
    """

    @abstractmethod
    def __iter__(self):
        """
        Return an iterator over the stations in order of appearance.
        Typically yields Station objects one by one as sketched below:

        def __iter__(self):
            current = self._head
            while current is not None:
                yield current
                current = current.get_next()
        """
        pass

    @abstractmethod
    def reverse_list_stations(self) -> list[str] | None:
        """
        Return a Python list of station names, in order of appearance
        from tail to head.
        """
        pass
