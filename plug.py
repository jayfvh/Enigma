"""
Enigma Project
Author: Jason Van Humbeck
Date: Jan 11 2023
"""

class Plug:
    """
    The Plug class represents a plug on the Plug Board at the bottom of the Enigma Machine.
    Each plug links two letters together at the front and end of the circuit.
    """
    def __init__(self, plug, plugs):
        """
        Initializes a Plug object with two connected letters and checks its validity.

        Args:
        - plug: A tuple containing two letters representing the connected plugs.
        - plugs: A list of existing Plug objects to check for conflicts.
        """
        self.plugA = plug[0]
        self.plugB = plug[1]
        self.valid = True
        self.check_valid(plugs)

    def get_a(self):
        """Returns the first letter of the plug."""
        return self.plugA

    def get_b(self):
        """Returns the second letter of the plug."""
        return self.plugB

    def check_valid(self, plugs):
        """
        Checks the validity of the plug by comparing it with other plugs.

        Args:
        - plugs: A list of existing Plug objects to check for conflicts.
        """
        if self.plugA == self.plugB:
            self.valid = False
        else:
            for plug in plugs:
                if plug.valid:
                    got_a = plug.get_a()
                    got_b = plug.get_b()
                    if ((got_a == self.plugA) or (got_a == self.plugB) or
                        (got_b == self.plugA) or (got_b == self.plugB)):
                        self.valid = False

    def output(self, input):
        """
        Outputs the letter after a swap on the plug board.

        Args:
        - input: The input letter to be swapped.

        Returns:
        - The swapped letter if applicable, otherwise None.
        """
        if input == self.plugA:
            return self.plugB
        elif input == self.plugB:
            return self.plugA
        else:
            return None

    def export(self):
        """
        Exports the plug data if the plug is valid.

        Returns:
        - A string containing the plug data in the format '|AB' if valid, otherwise an empty string.
        """
        output = ""
        if self.valid:
            output = f'|{self.plugA}{self.plugB}'
        return output


def find_Letter(plugs, letter):
    """
    Finds the letter after potential swaps on the plug board.

    Args:
    - plugs: A list of Plug objects representing the plugs on the plug board.
    - letter: The input letter to be searched for after swaps.

    Returns:
    - The swapped letter if applicable, otherwise the original letter.
    """
    found_letter = letter
    for plug in plugs:
        if plug.valid:
            grab = plug.output(letter)
            if grab is not None:
                found_letter = grab
                break
    return found_letter