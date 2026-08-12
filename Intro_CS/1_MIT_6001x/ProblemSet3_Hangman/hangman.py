import random
import string

WORDLIST_FILENAME = "words.txt"

def loadWords():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def chooseWord(wordlist):
    return random.choice(wordlist)

wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    for char in secretWord:
        if char not in lettersGuessed:
            return False
    return True

def getGuessedWord(secretWord, lettersGuessed):
    result = ""
    for char in secretWord:
        if char in lettersGuessed:
            result += char
        else:
            result += "_ "
    return result

def getAvailableLetters(lettersGuessed):
    result = ""
    for char in string.ascii_lowercase:
        if char not in lettersGuessed:
            result += char
    return result

def hangman(secretWord):
    print("Welcome to the game, Hangman!")
    print(f"I am thinking of a word that is {len(secretWord)} letters long.")
    print("-------------")
    
    guesses_left = 8
    lettersGuessed = []
    
    while guesses_left > 0 and not isWordGuessed(secretWord, lettersGuessed):
        print(f"You have {guesses_left} guesses left.")
        print(f"Available letters: {getAvailableLetters(lettersGuessed)}")
        guess = input("Please guess a letter: ").lower()
        
        if guess in lettersGuessed:
            print(f"Oops! You've already guessed that letter: {getGuessedWord(secretWord, lettersGuessed)}")
        else:
            lettersGuessed.append(guess)
            if guess in secretWord:
                print(f"Good guess: {getGuessedWord(secretWord, lettersGuessed)}")
            else:
                print(f"Oops! That letter is not in my word: {getGuessedWord(secretWord, lettersGuessed)}")
                guesses_left -= 1
        print("-------------")
        
    if isWordGuessed(secretWord, lettersGuessed):
        print("Congratulations, you won!")
    else:
        print(f"Sorry, you ran out of guesses. The word was {secretWord}.")

if __name__ == "__main__":
    secretWord = chooseWord(wordlist).lower()
    hangman(secretWord)
