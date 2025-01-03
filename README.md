# spellingGame
A terminal-based spelling application that help children improve their spelling abilities. Adapted from the classic hangman game

At the start of the game, the player is provided with an interactive user interface where the player is prompted to choose a word category of their choice. 

The game is divided into nine categories with each category consisting of a list of random two to five letter words. 
After choosing a word category, a hidden word is selected through an algorithm which randomly selects a word from a database of words.  
The player is then presented with corresponding number of underscores and hint that describes the hidden word. 

The player is then presented with three game options: 
1. To guess the word each letter at a time
2. To guess the entire word at once
3. To give up and reveal the answer. 

Throughout the game, the theme of drawing the “hanged man” in steps is implemented 
1-head, 2- torso , 3-right arm , 4-left arm , 5-right leg , 6-left leg

The players motive would be to win the game by guessing the word correctly before the drawing of the hangman is completed. 

The player is given few attempts to guess the correct hidden word selected by the algorithm.  For every alphabet the player guessed, the chosen alphabet is then checked if it exists in the actual word that the application algorithm has randomly selected. 

If it exists, the letter is replaced in its corresponding position of the underscores and the player score will be increased by one. However, if it is not in the actual word, the number of available wrong attempts and score would each be decreased by one.  

If the player uses all number of attempts without guessing the word, the player loses the game. If the player guesses the word correctly either at the first attempt or without using all the attempts set, the player wins the game. Regardless of if the player losses or wins a round, they would be asked if they wish to play again or exit the game. 

To enhance the user experience while playing the game, a colouful written feedback is displayed each time a correct or incorrect guess is made. Additionally, game sound effect was incorporated with a sound being played after a correct or incorrect guess is made. The user also hears a voice that congratulated and encourage them when they choose to exit the game.

