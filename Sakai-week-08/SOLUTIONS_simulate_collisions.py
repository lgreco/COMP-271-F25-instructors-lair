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
        self.N = N
        self.guests = guests
        self.hotel = [None] * N
        self.trials = trials
        self.min_length = self.DEFAULT_MIN_LENGTH
        self.max_length = self.DEFAULT_MAX_LENGTH

    def reset(self):
        """Reset the hotel for a new simulation. """
        self.hotel = [None] * self.N

    def generate_random_string(self):
        """Generate a random string of length between min_length and max_length."""
        length = random.randint(self.min_length, self.max_length)
        return "".join(
            chr(self.ASCII_OFFSET + random.randint(0, self.ASCII_SIZE - 1))
            for _ in range(length)
        )

    def hashcode(self, name: str) -> int:
        """A simple hash function for strings."""
        h = 0
        for char in name:
            h = h * 31 + ord(char)
        return h

    def hash_function(self, name: str) -> int:
        """Hash function to map a name to a hotel room."""
        return self.hashcode(name) % self.N

    def check_in(self, name: str) -> bool:
        """Attempt to check in a guest. Return True if successful, False if there's a collision."""
        # Find where to place the guest
        h = self.hash_function(name)
        # Check if the room is available
        checked_in = self.hotel[h] is None
        if checked_in:
            # No collision, check in the guest
            self.hotel[h] = name
        return checked_in

    def simulate_check_in(self) -> int:
        """Simulate the check-in process for all guests."""
        success = 0
        for _ in range(self.guests):
            # Generate a random name
            name = self.generate_random_string()
            # Attempt to check in the guest
            if self.check_in(name):
                # No collision, increment success count
                success += 1
        return success

    def main(self):
        """Run multiple simulations and report average success rate."""
        num_simulations = self.trials
        total_success = 0
        # Run the simulations
        for _ in range(num_simulations):
            # Reset the hotel for a new simulation
            self.reset()
            # Simulate check-ins and accumulate success count
            current_success = self.simulate_check_in()
            # Accumulate total success
            total_success += current_success
            # Print the success for this simulation
        print(
            f"\nN={self.N:,d}; simulations={num_simulations}; average admissions: {total_success / num_simulations}"
        )


if __name__ == "__main__":
    experiment = SimulateCollisions()
    experiment.main()
