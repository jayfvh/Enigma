"""
Enigma Project
Author: Jason Van Humbeck
Date: Jan 11 2023
"""
from plug import Plug, find_Letter
from rotor import Rotor

class EnigmaMachine:
    """
    The EnigmaMachine class represents the Enigma Machine, a device used for encryption during World War II.
    It includes rotors, a plugboard, and provides methods for setting up, encoding messages, and reading streams.
    """
    def __init__(self):
        """Initializes an EnigmaMachine object with empty lists for rotors and plugs."""
        self.rotors = []
        self.plugs = []

    def rotor_read(self, letter, rotor, flip):
        """
        Flips through all of the rotors sequentially and recursively returns the mirrored result.
        Example of rotor movement: [A, B, C, D, C, B, A] - At the middle point, it mirrors.

        Args:
        - letter: The input letter to be processed.
        - rotor: The current rotor being processed.
        - flip: The direction to flip through the rotors, either 1 or -1.

        Returns:
        - The final output letter after passing through all rotors.
        """
        if len(self.rotors) > 1:
            output = self.rotors[rotor].output(letter)
            if rotor == (len(self.rotors) - 1) and flip == 1:
                return self.rotor_read(output, rotor - 1, -1)
            elif rotor == 0 and flip == -1:
                return output
            else:
                return self.rotor_read(output, rotor + flip, flip)
        else:
            print("Missing needed information, please fill out")
            self.build_rotor()
            return self.rotor_read(letter,rotor,flip)

    def shift(self):
        """
        Updates the count of all rotors. For each rotor, if the count is 26, resets and carries the one (base 26).
        """
        self.rotors[0].add_count()  # Increases the count of the first rotor
        for i, rotor in enumerate(self.rotors):
            if rotor.count == 26:
                rotor.count = 0
                self.rotors[(i + 1) % len(self.rotors)].add_count()  # Calculates the carrying for all rotors

    def make_settings(self):
        """
        Sets the path for building custom settings, including rotors and plugs.
        """
        self.build_rotor()
        self.build_plug()
        self.output_message()

    def output_message(self):
        """
        Processes a message based on the current settings and prints the result.
        """
        get_input = "1"
        message = ""
        if len(self.rotors) < 2:
            while not get_input.isalpha():
                get_input = input("Enter an alphabetic message (with no spaces): ").upper()

            for inp in get_input:
                self.shift()
                plug_out_1 = find_Letter(self.plugs, inp)
                rotor_out = self.rotor_read(inp, 0, 1)
                plug_out_2 = find_Letter(self.plugs, rotor_out)
                message += plug_out_2
            print(message)
            print(self.get_settings())
        else:
            print("Invalid Settings - Error Thrown. Please add or change settings")
            self.make_settings()

    def basic_interface(self):
        """
        Basic text interface to direct user input for setting up or using the Enigma Machine.
        """
        got = True
        while got:
            grab = input("Enter 1 to input settings, and 2 to create settings: ")
            got = False
            if grab == "1":
                self.import_settings()
            elif grab == "2":
                self.make_settings()
            else:
                print("Invalid Input")
                got = True

    def build_rotor(self):
        """
        Grabs data from the user to build a valid rotor and adds it to the machine.
        There must be at least 2 rotors for the machine to work.
        """
        run = True
        while run:
            get_input = input("Create a rotor (Enter nothing to go to plug board): ")
            if get_input == "":
                if len(self.rotors) < 2:
                    print("You must have 2 Rotors")
                else:
                    run = False
            elif get_input.isalpha():
                my_rotor = Rotor(get_input, 0)
                if my_rotor.get_valid():
                    get_input = input("What is the starting position? ")
                    if get_input.isnumeric():
                        my_rotor.update_start(get_input)
                        self.rotors.append(my_rotor)

    def build_plug(self):
        """
        Grabs data from the user to build proper plugs for the plugboard.
        Plugs must be non-duplicating, non-colliding, and alphabetic.
        """
        run = True
        while run:
            get_input = input("Connect plug ('AE' = A<->E): ")
            if len(get_input) > 1:
                if get_input.isalpha():
                    self.plugs.append(Plug(get_input, self.plugs))
            elif get_input == "":
                run = False

    def get_settings(self):
        """
        Exports the rotor and plug settings so the message can be replicated.

        Returns:
        - A string containing the rotor and plug settings.
        """
        output = "**YOUR SETTINGS**: "
        for plug in self.plugs:
            output += plug.export()
        for rotor in self.rotors:
            output += rotor.export()
        return output

    def import_settings(self):
        """
        Takes a string from the user, previously generated by the program, to determine presets.
        Automatically rejects any invalid data, and there must be 2 valid rotors for the program to start.
        """
        text = input("IMPORT YOUR SETTINGS: ")
        if "|" in text:
            splits = text.split("|")
            for split in splits:
                if len(split) == 2 and split.isalpha():
                    self.plugs.append(Plug(split, self.plugs))
                elif len(split) > 2:
                    halfs = split.split(",")
                    if halfs[0].isalpha() and halfs[1].isnumeric():
                        test = Rotor(halfs[0], halfs[1])
                        if test.valid:
                            self.rotors.append(test)
        if len(self.rotors) < 2:
            print("These are either not valid settings or do not have at least 2 rotors, please manually add them.")
            self.make_settings()
        else:
            self.output_message()

    def read_stream(self, file_in, file_out):
        """
        Uses a text file to read and automatically export it as an Enigma-encoded file.

        Args:
        - file_in: The input file name.
        - file_out: The output file name.
        """
        try:
            with open(file_out, "wt") as wr:
                wr.write(self.get_settings())
                with open(file_in, "rt") as file_read:
                    for line in file_read:
                        new_line = ""
                        for char in line:
                            if char.isalpha():
                                self.shift()
                                new_line += self.rotor_read(char, 0, 1)
                        wr.write(new_line + "\n")
        except FileNotFoundError:
            print(f"The file '{file_in}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")