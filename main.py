

import colorama
from colorama import Fore, Style

import random
import os

import pygame

# Initialize pygame mixer for sound effects
pygame.mixer.init()


# Load sound effects
try:
    correct_sound = pygame.mixer.Sound('correct.wav')
    incorrect_sound = pygame.mixer.Sound('incorrect.wav')
    win_sound = pygame.mixer.Sound('win.wav')
    lose_sound = pygame.mixer.Sound('lose.wav')
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    print("Ensure that 'correct.wav', 'incorrect.wav', 'win.wav', and 'lose.wav' are in the same directory.")
    exit(1)


WORDS_FILE = 'wordcategory.txt'

hangman_art = { 
    0: (' ',),
    1: (' O ',
        '  ',
        '   '),
    2: (' O ',
        ' | ',
        ' |  '),
    3: (' O ',
        '/| ',
        ' |  '),
    4: (' O ',
        '/|\\ ',
        ' |  '),
    5: (' O ',
        '/|\\',
        '/| '),
    6: (' O ',
        '/|\\',
        '/|\\ '),
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_man(wrong_guesses):
    print('****************')
    for line in hangman_art[wrong_guesses]:
        print(line)
    print('****************')

def display_hint(hint):
    if isinstance(hint, list):
        # If hint is a list of characters
        print('Word: ' + ' '.join(hint))
    elif isinstance(hint, str):
        # If hint is a string (the actual hint)
        print(f"Hint: {hint}")
    else:
        print("No hint available.")

def display_answer(answer):
    print('The word was: ' + ' '.join(answer))

def load_words(file_path):
    
#Load words from the wordcategory text file. Each line in the file contains a category, word, and hint separated by commas.
    words = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace and split by comma
                parts = line.strip().split(',', 2)  # Split each line into 3 parts: category, word, hint
                if len(parts) == 3:
                    category, word, hint = parts
                    category = category.strip()
                    word = word.strip().lower()
                    hint = hint.strip()
                    
                    if category not in words:
                        words[category] = []
                    words[category].append({'word': word, 'hint': hint})
                else:
                    # Handle lines that don't have exactly 3 parts
                    print(f"Skipping invalid line in wordcategory.txt: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        exit(1)
    return words

def select_category(categories):

#Prompts the user to select a category from the available categories.  Returns the chosen category.
    
    print('****************************')
    print('WELCOME TO THE SPELLING GAME')
    print('****************************')
    print("Available Categories:")
    for idx, category in enumerate(categories, 1):
        print(f"{idx}. {category}")
    
    while True:
        choice = input("Select a category by number (or type 'exit' to quit): ").strip()
        
        if choice.lower() == "exit":
            print(Fore.BLUE + "Exiting the game..." + Style.RESET_ALL)
            exit(0)
        
        if not choice.isdigit():
            print(Fore.CYAN + "Invalid input! Please enter a number corresponding to the category."+ Style.RESET_ALL)
            continue
        
        choice = int(choice)
        if 1 <= choice <= len(categories):
            selected_category = categories[choice - 1]
            print(f"\nYou selected: {selected_category}")
            return selected_category
        else:
            print(f"Please enter a number between 1 and {len(categories)}.")

def play_letter_guess(answer):
  
    #Handles the letter guessing mode. Returns 'win' if the player wins, 'lose' if the player loses.
  
    hint = ['_'] * len(answer)
    wrong_guesses = 0
    guessed_letters = set()
    is_running = True
    max_attempts = len(hangman_art) - 1  # ( 7-1 = 6 )

    while is_running:
        display_man(wrong_guesses)
        display_hint(hint)
        guess = input('Enter a letter (or type "exit" to quit): ').lower()
        
        # Allow the player to exit the game during a playthrough
        if guess == "exit":
            print(Fore.BLUE + "Exiting the game..." + Style.RESET_ALL)
            exit(0)
        
        if len(guess) != 1:
            print('Invalid input! Please type a single character.')
            continue
        if not guess.isalpha():
            print('Invalid input! Please type an alphabet.')
            continue
        if guess in guessed_letters:
            print(f"'{guess}' is already guessed.")
            continue
        guessed_letters.add(guess)

        if guess in answer:
            for i in range(len(answer)):
                if answer[i] == guess:
                    hint[i] = guess
                    print(Fore.GREEN + f"Good job! '{guess}' is in the word." + Style.RESET_ALL)
                    correct_sound.play()
        else:
            wrong_guesses += 1
            print(Fore.RED + f"Sorry, '{guess}' is not in the word." + Style.RESET_ALL)
            incorrect_sound.play()


        # Calculate attempts left
        attempts_left = max_attempts - wrong_guesses
        print(f"Attempts left: {attempts_left}\n")

        if "_" not in hint:
            display_man(wrong_guesses)
            display_answer(answer)
            print(Fore.GREEN + 'YOU WIN!' + Style.RESET_ALL)
            win_sound.play()
            return 'win'
        elif wrong_guesses >= max_attempts:
            display_man(wrong_guesses)
            display_answer(answer)
            print('YOU LOSE!')
            lose_sound.play()
            return 'lose'

def play_word_guess(answer):
    #Handles the word guessing mode. Returns 'win' if the player guesses correctly, 'lose' otherwise.
    wrong_guesses = 0
    max_attempts = 6  # number of attempts allowed for guessing the whole word.

    while wrong_guesses < max_attempts:
        guess_word = input('Enter your word guess (or type "exit" to quit): ').lower()
        
        if guess_word == "exit":
            print(Fore.BLUE + f"Exiting the game..." + Style.RESET_ALL)
            exit(0)
        
        if not guess_word.isalpha():
            print('Invalid input! Please type a valid word.')
            continue

        if guess_word == answer:
            display_man(wrong_guesses)
            print(Fore.GREEN + 'YOU WIN!' + Style.RESET_ALL)
            win_sound.play()
            return 'win'
        else:
            wrong_guesses += 1
            attempts_left = max_attempts - wrong_guesses
            display_man(wrong_guesses)
            print(Fore.RED + f"Sorry, '{guess_word}' is not the correct word." + Style.RESET_ALL)
            incorrect_sound.play()
            print(f'Attempts left: {attempts_left}\n')

    # If the player fails to guess the word within the allowed attempts
    display_man(wrong_guesses)
    display_answer(answer)
    print(Fore.RED + 'YOU LOSE!'+ Style.RESET_ALL)
    lose_sound.play()
    return 'lose'

def play_game(words_data):
    
    # function to plays a single round of the spelling based on the user's choice. Returns 'win' or 'lose' based on the outcome.
    
    clear_screen() #to clear the previous code in the terminal and preent a clean dashboard

    # Select a category
    categories = list(words_data.keys())
    selected_category = select_category(categories)
    
    # Select a random word from the chosen category
    selected_entry = random.choice(words_data[selected_category])
    answer = selected_entry['word']
    hint_text = selected_entry['hint']
    
    print(f"\nThe word has {len(answer)} letters.")
    print(f"Hint: {hint_text}")  # Display the hint at the start

    # Display instruction menu
    print("\nChoose an option:")
    print("1. Guess a letter")
    print("2. Guess the whole word")
    print("3. Reveal answer and give up")
    choice = input("Enter your choice (1/2/3): ").strip()
    
    # Allow the player to exit the game by typing 'exit' at the choice prompt
    if choice.lower() == "exit":
        print(Fore.BLUE + "Exiting the game..." + Style.RESET_ALL)
        exit(0)

    if choice == '1':
        return play_letter_guess(answer)
    elif choice == '2':
        return play_word_guess(answer)
    elif choice == '3':
        display_man(0)  # Display the hangman art at index [0] (no wrong guesses)
        display_answer(answer)
        print(Fore.RED +'YOU LOSE!' + Style.RESET_ALL)
        lose_sound.play()
    else:
        print ('wow')
        print("Invalid choice! Please enter 1, 2, or 3.")
        # Recursively call play_game to prompt again for a valid choice
        return play_game(words_data)

def main():
#Main function to run the spelling game with scoring and multiple playthroughs.

    words_data = load_words(WORDS_FILE)   # Load words from the text file
    
    if not words_data:
        print("The words list is empty. Please add words to 'words.txt'.")
        exit(1)
    
    score = 0  # Initialize score
    play_again = True

    while play_again:
        result = play_game(words_data)
        
        # Update score based on game result
        if result == 'win':
            score += 1
        elif result == 'lose':
            score -= 1

        print(f"\nCurrent Score: {score}\n")

        # Ask the user if they want to play again
        while True:
            user_input = input("Do you want to play again? (y/n): ").strip().lower()
            if user_input == 'y':
                break  
            elif user_input == 'n':
                play_again = False
                print(Fore.MAGENTA + f"\nThank you for playing! Your final score is {score}."+ Style.RESET_ALL)
                break
            else:
                print("Invalid input! Please enter 'y' for yes or 'n' for no.")

if __name__ == '__main__':
    main()

