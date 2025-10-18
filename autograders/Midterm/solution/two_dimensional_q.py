class TwoDimensionalQ:

    def __init__(self, n: int = 4):
        """A circular queue implements on an n x n grid modeling the seating
        in a waiting room.
        """
        self._underlying: list[list[str]] = [[None for _ in range(n)] for _ in range(n)]
        self._n: int = n
        self._capacity: int = n * n
        self._usage: int = 0
        # (row, column) grid reference for front and back of queue
        self._front: tuple[int, int] = (0, 0)
        self._back: tuple[int, int] = (0, 0)

    # --- Accessors ----

    def get_usage(self) -> int:
        return self._usage

    def get_capacity(self) -> int:
        return self._capacity

    def is_full(self) -> bool:
        return self._usage == self._capacity

    def is_empty(self) -> bool:
        return self._usage == 0

    def peek(self) -> str:
        front_row, front_col = self._front
        return self._underlying[front_row][front_col] if self._usage > 0 else None

    # --- Overloading some special methods ---

    def __len__(self) -> int:
        return self.get_usage()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"Queue size {self._n}x{self._n}; capacity: {self._capacity}; usage:{self._usage}; front is at {self._front}; back is at {self._back}"

    def __str__(self) -> str:
        return self.__repr__()

    def __iter__(self):
        """Yield occupants from front to back in FIFO order (handles wrap-around)."""
        count = 0
        row, col = self._front
        while count < self._usage:
            value = self._underlying[row][col]
            # Occupied cells are non-None by invariant; guard defensively anyway.
            if value is not None:
                yield value
            col = (col + 1) % self._n
            row = (row + 1) % self._n if col == 0 else row
            count += 1


    # --- Core functionality ---

    def enqueue(self, value: str) -> bool:
        """Add value to the back of the queue. Return True if successful, False if not."""
        success: bool = self._usage < self._capacity
        if success:
            # There is room to add the value, obtain the back position.
            back_row, back_col = self._back
            # Place the value at the back position and increment usage.
            self._underlying[back_row][back_col] = value
            self._usage += 1
            # Update the back position to the next available slot.
            back_col = (back_col + 1) % self._n
            back_row = (back_row + 1) % self._n if back_col == 0 else back_row
            self._back = (back_row, back_col)
        return success

    def dequeue(self) -> str:
        """Remove and return the value at the front of the queue. If the queue is empty, return None."""
        result = None
        if self._usage > 0:
            # There is something to remove, obtain the front position.
            front_row, front_col = self._front
            result = self._underlying[front_row][front_col]
            # Remove the value at the front position and decrement usage.
            self._underlying[front_row][front_col] = None
            self._usage -= 1
            # Update the front position to the next occupied slot.
            front_col = (front_col + 1) % self._n
            front_row = front_row + 1 if front_col == 0 else front_row
            self._front = (front_row, front_col)
        return result

    def list_queue(self) -> list[str]:
        """Return a list of the items in the queue from front to back."""
        queue: list[str] = list()
        # Traverse the queue from front to back, wrapping as necessary.
        front_row, front_col = self._front
        for i in range(self._usage):
            # Append the current front item to the result list.
            queue.append(self._underlying[front_row][front_col])
            # Move to the next item in the queue.
            front_col = (front_col + 1) % self._n
            front_row = (front_row + 1) % self._n if front_col == 0 else front_row
        return queue


if __name__ == "__main__":
    test = TwoDimensionalQ(4)
    items_to_add = ["Alice", "Bob", "Cathy", "Derek", "Eva"]
    for item in items_to_add:
        print(test.enqueue(item))

    print(test.list_queue())
    print(test.dequeue())
    print(f"Peeking: {test.peek()}")
    print(test.list_queue())