class NaiveTwoDimensionalQ:
    """
    A naive implementation of a two-dimensional queue. The queue is implemented
    using a 2-D array (list of lists) and shifts elements on dequeue.
    This implementation is not efficient, as dequeue operation takes O(n^2) time
    in the worst case.
    """

    def __init__(self, n: int = 4):
        """
        Initialize the two-dimensional queue using an n x n underlying array.
        """
        self._underlying: list[list[str]] = [[None for _ in range(n)] for _ in range(n)]
        self._n: int = n
        self._capacity: int = n * n
        self._usage: int = 0

    def get_usage(self) -> int:
        """
        Get the current usage of the queue (number of elements).
        """
        return self._usage

    def get_capacity(self) -> int:
        """
        Get the capacity of the queue (maximum number of elements).
        """
        return self._capacity

    def enqueue(self, value: str) -> bool:
        """
        Enqueue an element into the two-dimensional queue.
        """
        # Check if there is space in the queue and add the element if so.
        success: bool = self._usage < self._capacity
        if success:
            # Calculate the row and column to insert the new element based
            # on current usage.
            row = self._usage // self._n
            col = self._usage % self._n
            self._underlying[row][col] = value
            self._usage += 1
        return success

    def dequeue(self) -> str:
        """
        Dequeue an element from the two-dimensional queue. The first element 
        is always expected to be at the front pointer, which has two components
        for the corresponding row and column in the 2D underlying array.
        """
        result = None
        if self._usage > 0:
            # If the queue is not empty, remove and return the front element.
            result = self._underlying[0][0]
            # Shift all other elements forward to fill the gap.
            for i in range(self._usage - 1):
                # Calculate the row and column of the current element.
                row = i // self._n
                col = i % self._n
                # Calculate the row and column of the next element.
                next_row = (i + 1) // self._n
                next_col = (i + 1) % self._n
                # Move the next element to the current position.
                self._underlying[row][col] = self._underlying[next_row][next_col]
            # Clear the last element which is now a duplicate after shifting.
            last_row = (self._usage - 1) // self._n
            last_col = (self._usage - 1) % self._n
            self._underlying[last_row][last_col] = None
            # Decrease the usage count.
            self._usage -= 1
        return result

    def list_queue(self) -> list[str]:
        """
        List all elements in the two-dimensional queue.
        """
        # Return a flat list of all elements in the queue.
        result = []
        # Iterate only up to current usage.
        for i in range(self._usage):
            # Calculate the row and column of the current element.
            row = i // self._n
            col = i % self._n
            # Append the element to the result list.
            result.append(self._underlying[row][col])
        return result


if __name__ == "__main__":
    test = NaiveTwoDimensionalQ(2)
    items_to_add = ["Alice", "Bob", "Cathy", "Derek", "Eva"]
    for item in items_to_add:
        success = test.enqueue(item)
        print(f"Enqueuing {item:<6}: {'Successful' if success else 'Failed'}")
    print(test.list_queue())