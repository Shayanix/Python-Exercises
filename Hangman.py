from random import choice


def run_game():
    
    word : str = choice(['apple', 'banana', 'cherry', 'date',
                         'elderberry', 'fig', 'grape', 'honeydew',
                         'kiwi', 'lemon', 'mango', 'nectarine', 'orange',
                         'pear', 'quince', 'raspberry', 'strawberry',
                         'tangerine', 'ugli', 'watermelon'])
    
    username : str = input("Enter your username: ")
    print(f"Hello, {username}! Welcome to Hangman!")
    
    guessed : str = ''
    tries : int = 5
    
    while tries > 0:
        
        blanks : int = 0
        
        for char in word:
            if char in guessed:
                print(char, end=' ')
            else:
                print('_', end=' ')
                blanks += 1
                
        print()
        if blanks == 0:
            print("\nCongratulations! You won!")
            break
        
       
        
        guess : str = input("\nGuess a letter: ")
        
        
        
        if guess in guessed:
            print("You already guessed that letter.")
            continue
        
        guessed += guess
        
        if guess not in word:
            tries -= 1
            print(f"Wrong! You have {tries} tries left.")
            
            if tries == 0:
                print("You lost! The word was", word)
                break
            
if __name__ == '__main__':
    
    run_game()
    
    while True:
        play_again : str = input("Do you want to play again? (yes/no): ")
        
        if play_again.lower() == 'yes':
            run_game()
        else:
            print("Goodbye!")
            break
    
    