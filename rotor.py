"""
Enigma Project
Author: Jason Van Humbeck
Date: Jan 11 2023
"""

class Rotor:
    """
    The Rotor class represents one of the rotors in the Enigma Machine.
    Rotors shift after every key stroke, contributing to the constantly changing cipher.
    """
    def __init__(self, string, start):
        """
        Initializes a Rotor object with a given string and starting position.

        Args:
        - string: A string of 26 unique characters representing the rotor's wiring.
        - start: The starting position of the rotor, an integer between 0 and 25.
        """
        self.string = string
        self.count = int(start) % 26
        self.start = int(start) % 26
        self.valid = True
        self.find_valid()

    def find_valid(self):
        """
        Determines if the rotor has unique pairings and sets validity accordingly.
        """
        terminate = False
        if not len(self.string) == 26:
            terminate = True
        else:
            for l in self.string:
                if self.string.count(l) > 1:
                    terminate = True
        if terminate:
            print("Invalid Rotor - Deleted")
            self.valid = False

    def output(self, input):
        """
        Converts the given input to the shifted text based on rotor wiring.

        Args:
        - input: The input letter to be converted.

        Returns:
        - The output letter after shifting.
        """
        to_number = (ord(input.upper()) - 65)
        found_pos = (to_number + self.count) % 26
        return self.string[found_pos]

    def update_start(self, count):
        """
        Updates the starting position of the rotor.

        Args:
        - count: The new starting position.
        """
        self.start = int(count) % 26
        self.count = int(count) % 26

    def add_count(self):
        """Increases the rotation by one move."""
        self.count += 1

    def get_valid(self):
        """
        Returns if the rotor is valid and can be used.
        """
        return self.valid

    def export(self):
        """
        Exports the rotor data if the rotor is valid.

        Returns:
        - A string containing the rotor data in the format '|ABCDEF...,start' if valid, otherwise an empty string.
        """
        output = ""
        if self.valid:
            output = f'|{self.string},{self.start}'
        return output