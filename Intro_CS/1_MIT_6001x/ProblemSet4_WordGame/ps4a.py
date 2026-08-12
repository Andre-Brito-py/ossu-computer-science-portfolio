# Problem Set 4A
# Name: Andre Brito
# Collaborators: None
# Time Spent: 1:30

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

def loadWords():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def getWordScore(word, n):
    score = 0
    for char in word:
        score += SCRABBLE_LETTER_VALUES.get(char, 0)
    score *= len(word)
    if len(word) == n:
        score += 50
    return score

def displayHand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=" ")
    print()

def dealHand(n):
    hand = {}
    numVowels = n // 3
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
    return hand

def updateHand(hand, word):
    new_hand = hand.copy()
    for char in word:
        new_hand[char] -= 1
    return new_hand

def isValidWord(word, hand, wordList):
    if word not in wordList:
        return False
    
    hand_copy = hand.copy()
    for char in word:
        if hand_copy.get(char, 0) == 0:
            return False
        hand_copy[char] -= 1
    return True

def calculateHandlen(hand):
    return sum(hand.values())

def playHand(hand, wordList, n):
    total_score = 0
    while calculateHandlen(hand) > 0:
        print("Current Hand: ", end="")
        displayHand(hand)
        word = input('Enter word, or a "." to indicate that you are finished: ')
        
        if word == '.':
            break
        else:
            if not isValidWord(word, hand, wordList):
                print("Invalid word, please try again.\n")
            else:
                score = getWordScore(word, n)
                total_score += score
                print(f'"{word}" earned {score} points. Total: {total_score} points\n')
                hand = updateHand(hand, word)
                
    if word == '.':
        print(f"Goodbye! Total score: {total_score} points.")
    else:
        print(f"Run out of letters. Total score: {total_score} points.")

if __name__ == '__main__':
    wordList = loadWords()
    playHand(dealHand(HAND_SIZE), wordList, HAND_SIZE)
