# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 7/31/2022
# Description: Class and methods for a Wordle clone called 6-Game.

import random


class Game:
    """
    An object representing a Wordle clone called 6-Game.
    """
    _word = ''
    guesses = 6
    num_guesses = 0
    finished = False

    def start(self):
        """
        Start the game and pick the word.
        """
        words = []
        with open('words') as file:
            for line in file:
                words.append(line.strip())
        self._word = random.choice(words).lower()
        #print(self._word)

    def parse_response(self, message):
        """
        Checks the response from the player to see if they matched the word or how close they were.
        :param message: The message from the player.
        :return: The response text to give the player a hint or tell them if they won/lost.
        """
        message = message.strip()
        if len(message) < 6:
            return 'Word is too short. Try again.'
        if len(message) > 25:
            return 'Word is waaaaaaaaay too long. Try again.'
        if len(message) > 6:
            return 'Word is too long. Try again.'

        self.num_guesses += 1
        message = message.lower()
        # check for a match
        if message == self._word:
            self.finished = True
            return f'You got the word in {self.num_guesses} guess{"es" if self.num_guesses > 1 else ""}! {self._word}'

        response = f'You guessed:\r\n\t\t  {message}\r\n\t\t  '
        guess_score = 0
        # check each letter for a match
        for i in range(len(message)):
            if message[i] == self._word[i]:
                response += '$'
                guess_score += 2
            elif message[i] in self._word:
                response += '!'
                guess_score += 1
            else:
                response += '_'

        # check how close the player is to the word and give some encouraging words.
        if guess_score >= 10:
            response += f' Wow! You\'re getting close!'
        elif guess_score >= 7:
            response += f' That was a pretty good guess.'
        elif guess_score >= 3:
            response += f' Keep going, you\'ll get there.'

        # calculate remaining guesses and build the response
        remaining = self.guesses - self.num_guesses
        if remaining == 0:
            self.finished = True
            return f'Oh no! You\'re out of guesses! The word was "{self._word}".'
        else:
            guesses = f' {remaining} guess{"es" if remaining > 1 else ""} left.'
            response += guesses

        return response
