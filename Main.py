"""
Enigma Project
Author: Jason Van Humbeck
Date: Jan 11 2023
"""

from enigma import EnigmaMachine
from rotor import Rotor
from plug import Plug
import random

class Main:
    """
    Enigma when hooked up to modern computers can do anything regardless of its real life time intensity.
    As a testimte to this I am plugging in Hamlet into the Engima machine, with the real settings and randomized plugs.
    """
    my_enigma = EnigmaMachine()
    my_rotors = ["LPGSZMHAEOQKVXRFYBUTNICJDW", "SLVGBTFXJQOHEWIRZYAMKPCNDU", "CJGDPSHKTURAWZXFMYNQOBVLIE", "IMETCGFRAYSQBZXWLHKDVUPOJN"]
    my_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for my_rotor in my_rotors:
        # Set all 4 rotors and give them random start positions
        my_enigma.rotors.append(Rotor(my_rotor, random.randint(0, 25)))

    for _ in range(20):
        """
        When setting the plugs, since the data structure for Enigma and plugs are so robust they can
        automatically sort through valid plugs. As such, I can randomize two letters 20 times and ensure it will
        filter to likely give 5-10 plug options, which is accurate to the real settings.
        """
        pos_x = my_alphabet[random.randint(0, 25)]
        pos_y = my_alphabet[random.randint(0, 25)]
        my_enigma.plugs.append(Plug(pos_x + pos_y, my_enigma.plugs))

    my_enigma.read_stream("hamlet.txt", "secretHamlet.txt")


