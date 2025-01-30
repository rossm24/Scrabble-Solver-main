
class Player:
    def __init__(self):
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

