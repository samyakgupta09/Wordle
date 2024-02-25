#----------------------------------------------------
# Assignment2: Wordle
# Purpose of program: create the necessary classes for the wordle game
#
# Author: Samyak Gupta
# Collaborators/references: CMPUT 175 team
#----------------------------------------------------

from random import choice
from collections.abc import MutableSet

class TooShortError(ValueError):
    '''Error class for when word is shorter than needed length'''
    
    def __init__(self, arg):
        """
        Intializes an instance of this error
        arg(str) - arguments
        """
        
        self.args = arg    

class TooLongError(ValueError):
    '''Error class for when word is longer than needed length'''
    
    def __init__(self, arg):
        """
        Intializes an instance of this error
        arg(str) - arguments
        """
        
        self.args = arg
        
class NotLettersError(ValueError):
    '''Error class for when word has special characters/numbers'''
    
    def __init__(self, arg):
        """
        Intializes an instance of this error
        arg(str) - arguments
        """
        
        self.args = arg

class WordleWords(MutableSet):
    '''An instance of this class is the words for wordle'''
    
    def __init__(self, letters):
        """
        Initializes an instance of WordleWords
        letter(int) - number of letters
        """
        
        self._words = set()
        self._letters = letters
           
    def __contains__(self, word):
        """
        Checks if word is in self._words
        word(str) - word to be checked
        returns(bool) - returns true or false
        """
        
        return word in self._words
        
    def __iter__(self):
        """
        Creates and iterable object of self._words
        returns - iterator object
        """
        
        return iter(self._words)
        
    def __len__(self):
        """
        returns the number of words
        returns(int) - number of words
        """
        
        return len(self._words)
        
    def add(self, word):
        """
        Adds given word to self._words after checking if word is valid
        word(str) - word to be added
        """
        
        self.check_word(word)
        self._words.add(word)
        
    def discard(self, word):
        """
        removes given word from self._words after checking if word is in the set
        word(str) - word to be removed
        """
        
        self.__contains__(word)
        self._words.discard(word)
        
    def load_file(self, filename):
        """
        adds valid words from given filename to self._words
        filename(str) - name of the file
        """
        
        # opens file, reads name and adds to the set
        with open(filename,'r') as file:
            words = file.readlines()
            for word in words:
                word = word.strip('\n')
                try:
                    self.add(word.upper())
                except:
                    pass
        
    def check_word(self, word):
        """
        checks if word is valid
        word(str) - word to be checked
        """
        
        alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        #checks if word is too short
        if len(word) < self._letters:
            raise TooShortError('word is too short')
        
        # checks if word is too long
        if len(word) > self._letters:
            raise TooLongError('word is too long')
        
        # checks if word has capital letters only
        for letter in word:
            if letter not in alphabets:
                raise NotLettersError('Word should have capital letters only')
            
    def letters(self):
        """
        Returns the number of letters in every word. 
        returns(int) - number of letters in every word
        """
        
        return self._letters
    
    def copy(self):
        """
        Returns a second WorldeWords instance which contains the same words
        returns(WordleWords) - copy of the same instance
        """
        
        copy = WordleWords(self._letters)
        copy._words = self._words.copy()
        return copy
        
class Guess:
    '''An instance of this class is a guess for wordle'''
    
    def __init__(self, guess, answer):
        """
        intialized an instance of Guess
        guess(str) - guess word
        answer(str) - answer word
        """
        
        self._guess = guess
        self._answer = answer
        
    def guess(self):
        """
        returns guess word
        return(str) - guess word
        """
        
        return self._guess
    
    def correct(self):
        """
        returns letters of the string in the correct positions with dashes
        returns(str) - letters of the string in correct positions along with dashes
        """
        
        # checks if letter in the same indexes for both words
        correct = ''
        for index in range(len(self._guess)):
            if self._guess[index] == self._answer[index]:
                correct += self._guess[index]
            else:
                correct += '_'
        return correct
                
    def misplaced(self):
        """
        returns letters in the answer but in incorrect positions
        returns(str) - string of lettes in answer but in incorrect positions
        """
        
        # create empty lists
        misplaced = []
        non_correct_guess = []
        non_correct_answer = []
        
        # keeps track of non correct letter
        for index in range(len(self._guess)):
            if self._guess[index] != self._answer[index]:
                non_correct_guess.append(self._guess[index])
                non_correct_answer.append(self._answer[index])
        
        # checks if non correct letter is in both words
        for letter in non_correct_guess:
            if letter in non_correct_answer:
                misplaced.append(letter)
                non_correct_answer.remove(letter)
        misplaced = sorted(misplaced)
        misplaced = ''.join(misplaced)
        return misplaced
    
    def wrong(self):
        """
        returns letters not in the answer
        returns(str) - string of letters not in answers
        """
        
        # creates empty lists
        wrong = []
        non_correct_guess = []
        non_correct_answer = []
        
        # makes non correct letters lists
        for index in range(len(self._guess)):
            if self._guess[index] != self._answer[index]:
                non_correct_guess.append(self._guess[index])
                non_correct_answer.append(self._answer[index])
                
        # checks if letter in guess is not in answer
        for letter in non_correct_guess:
            if letter not in non_correct_answer:
                wrong.append(letter)
        wrong = sorted(wrong)
        wrong = ''.join(wrong)
        return wrong
    
    def is_win(self):
        """
        tells if guess is correct or not
        returns(bool) - true if guess is correct false otherwise
        """
        
        if self._guess == self._answer:
            return True
        else:
            return False
        
class Wordle:
    '''An instance of this class is a game of wordle'''
    
    def __init__(self, words):
        """
        initializes an instance of Wordle
        words(WordleWords) - wordle words instance object for the game
        """
        
        self._words = words
        self._answer = choice(list(self._words._words))
        self._guesses = 0 
        
    def guesses(self):
        """
        returns number of guesses
        returns(int) - number of guesses
        """
        
        return self._guesses
        
    def guess(self, guessed):
        """
        takes a string guessed and return a Guess instance object that represents the results of the guess
        guessed(str) - word to be guessed
        returns(Guess) - Guess instance object for the guessed word
        """
        
        self._guesses += 1
        return Guess(guessed, self._answer)