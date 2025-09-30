import random


class SimulateCollisions:

    # Constants for random string generation
    DEFAULT_MIN_LENGTH = 10
    DEFAULT_MAX_LENGTH = 15
    ASCII_OFFSET = ord("A")
    ASCII_SIZE = 26

    # Default hotel size
    DEFAULT_N = 1_024
    DEFAULT_GUESTS = DEFAULT_N

    # Default simulations
    DEFAULT_TRIALS = 10

    def __init__(
        self,
        N: int = DEFAULT_N,
        guests: int = DEFAULT_GUESTS,
        trials: int = DEFAULT_TRIALS,
    ):
        pass

    def reset(self):
        """Reset the hotel for a new simulation."""
        self.hotel = [None] * self.N

    def generate_random_string(self):
        """Generate a random string of length between min_length and max_length."""
        pass

    def hashcode(self, name: str) -> int:
        """A simple hash function for strings."""
        pass

    def hash_function(self, name: str) -> int:
        """Hash function to map a name to a hotel room."""
        return self.hashcode(name) % self.N

    # Additional methods at your discretion

    def main(self):
        """Run multiple simulations and report average success rate."""
        pass


if __name__ == "__main__":
    experiment = SimulateCollisions()
    experiment.main()
