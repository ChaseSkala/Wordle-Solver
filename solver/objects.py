from enum import Enum

class Colors(Enum):
    red = 0
    yellow = 1
    green = 2

class LetterStatus:
    letter: str
    status: Colors

    def __init__(self, letter, status):
        self.letter = letter
        self.status = status

    @classmethod
    def from_dict(cls, data):
        letter = data['letter']
        status = Colors[data['status']]
        return cls(letter, status)

class Guess:
    word: str
    result: list[LetterStatus]

    def __init__(self, word, result):
        self.word = word
        self.result = result

    @classmethod
    def from_dict(cls, data):
        word = data['word']
        result = data['result']
        clean_result = []
        for status in result:
            clean_result.append(LetterStatus.from_dict(status))
        return cls(word,clean_result)

class WordleData:
    attempts: int
    solution: str
    guesses: list[Guess]
    clean_guesses: list

    def __init__(self, attempts: int, solution: str, guesses: list[Guess]):
        self.attempts = attempts
        self.solution = solution
        self.guesses = guesses
        self.clean_guesses = []

    @classmethod
    def from_dict(cls, data):
        attempts = data["attempts"]
        solution = data["solution"]
        guesses = data["history"]["guesses"]
        clean_guesses = []
        for guess in guesses:
            clean_guesses.append(Guess.from_dict(guess))
        return cls(attempts, solution, clean_guesses)