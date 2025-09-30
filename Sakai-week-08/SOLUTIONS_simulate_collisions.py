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
        self.hotel = [None] * self.N

    def generate_random_string(self):
        length = random.randint(self.min_length, self.max_length)
        return "".join(
            chr(self.ASCII_OFFSET + random.randint(0, self.ASCII_SIZE - 1))
            for _ in range(length)
        )

    def hashcode(self, name: str) -> int:
        h = 0
        for char in name:
            h = h * 31 + ord(char)
        return h

    def hash_function(self, name: str) -> int:
        return self.hashcode(name) % self.N

    def check_in(self, name: str) -> bool:
        h = self.hash_function(name)
        checked_in = self.hotel[h] is None
        if checked_in:
            self.hotel[h] = name
        return checked_in

    def simulate_check_in(self) -> int:
        success = 0
        for _ in range(self.guests):
            name = self.generate_random_string()
            if self.check_in(name):
                success += 1
        return success

    def main(self):
        num_simulations = self.trials
        total_success = 0
        for _ in range(num_simulations):
            self.reset()
            current_success = self.simulate_check_in()
            total_success += current_success

        print(
            f"Average success over {num_simulations} simulations: {total_success / num_simulations}"
        )


if __name__ == "__main__":
    experiment = SimulateCollisions()
    experiment.main()
