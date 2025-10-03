import random
import string
# 1. madlib string concatenation (aka how to put strings together)

# adj = input("Adjective: ")
# verb1 = input("Verb: ")
# verb2 = input("Verb: ")
# famous_person = input("Famous person: ")
# madlib = f"Computer programming is so {adj}! It makes me excited all the time becuase \
# I love to {verb1}. Stay hydrated and {verb2} like you are {famous_person}!"
# print(madlib)

# ======================================================================================================



# def guess(x):
#     random_number = random.randint(1 ,x)
#     guess = 0
#     while guess != random_number:
#         guess = int(input(f'Guess a number between 1 and {x}'))
#         if guess < random_number:
#             print('Sorry, guess again. Too low.')
#         elif guess > random_number:
#             print('Sorry, guess again. Too high.')
#     print(f'Yay, congrats! You have guessed the number {random_number} correctly!')
# guess(10)

# def computer_guess(x):
#     low = 1
#     high = x
#     feedback = ''
#     while feedback != 'c':
#         if low != high:
#             guess = random.randint(low, high)
#         else
#             guess = low # or high b/c low == high
#         feedback = input(f'Is this number {guess}, too high (H), too low (L) or correct (C)?').lower()
#         if feedback == 'h':
#             high = guess - 1
#         elif feedback == 'l':
#             low = guess + 1
#     print(f'Yay! Computer guessed the number {guess} correctly!')
# computer_guess(10)

# rock, paper, scissor
# def play():
#     user = input("What is your choice? 'r' for rock, 'p' for paper, 's' for scissor.\n")
#     computer = random.choice(['r','p','s'])
#     if user == computer:
#         return 'It was a tie. The computer chose ' + computer + '.'
#     if is_win(user, computer):
#         return 'You won. The computer chose ' + computer + '.'
#     return 'You lost. The computer chose ' + computer + '.'
#
# def is_win(player, opponent):
#     # r > s, s > p, p > r
#     if (player == 'r' and opponent == 's') or (player == 's' and opponent == 'p') or (player == 'p' and opponent == 'r'):
#         return True
# print(play())
# ====================================================== ================================================

 #hangman
# from words import words
# def get_valid_word(words):
#     word = random.choice(words)
#     while '-' in word or ' ' in word:
#         word = random.choice(words)
#     return word.upper()
#
# def hangman():
#     word = get_valid_word(words)
#     word_letters = set(word)
#     alphabet = set(string.ascii_uppercase)
#     used_letters = set()
#     lives = 6
#     while len(word_letters) > 0 and lives > 0:
#         # ' '.join(['a','b','cd']) -> 'a b cd'
#         print('You have', lives, ' lives yet and used these letters: ' + ' '.join(used_letters))
#         word_list = [letter if letter in used_letters else '-' for letter in word]
#         print('Current word: ' + ' '.join(word_list))
#         user_letter = input('Guess a letter: ').upper()
#         if user_letter in alphabet - used_letters:
#             used_letters.add(user_letter)
#             if user_letter in word_letters:
#                 word_letters.remove(user_letter)
#             else:
#                 lives = lives - 1
#                 print('Letter is not in the word.')
#         elif user_letter in used_letters:
#             print('You have already used this character. Please try again.')
#         else:
#             print('Invalid character. Please try again.')
#     if lives == 0:
#         print('No more lives. The word is ' + word + '. Game over.')
#     else:
#         print('Good job! You guessed the word ' + word + ' correctly.')
#
# hangman()
# from functions.yh_fnce.yh_fnce import yh_fnce as yf
from etfpy import ETF, load_etf, get_available_etfs_list

spy = ETF('SPY')
print(spy.info)