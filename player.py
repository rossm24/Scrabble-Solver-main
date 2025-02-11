
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0  # Initial score is 0
        self.letters_in_rack = []  # Initially, the rack is empty

    def add_letters_to_rack(self, letters):
        """
        Adds letters to the player's rack.
        :param letters: List of letters to add to the rack
        """
        self.letters_in_rack.extend(letters)

    def remove_letters_from_rack(self, letters):
        for letter in letters:
            if letter in self.letters_in_rack:
                self.letters_in_rack.remove(letter)

    def update_score(self, points):
        """
        Updates the player's score.
        :param points: The points to add to the player's score
        """
        self.score += points

    def set_tile_rack(self, letters):
        self.letters_in_rack = letters

'''
We found an exisiting Scrabble algorithm that would run through a full game of Scrabble as a single player,
playing the best possible word from a complete Scrabble dictionary, at each turn.

We have taken this and made necessary adaptations so that it better fits out goals. This includes mainly implementing a player
system to accomodate two players turns and also changing the dictionary so that it is more kid friendly, 
playing words that they would know and understand. 

[show algorithm] [show player 1 button 1 player 2 button 2]
'''