import random


def roll_dice(amount: int) -> list[int]:
    if amount < 1:
        raise ValueError("Amount must be greater than 0")
       
    rolls: list[int] = []
    
    for i in range(amount):
        rolls.append(random.randint(1, 6))
    
    return rolls

def main():
    while True:
        try:
            user_input = input("Enter the amount of dice to roll: ")
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            print(*roll_dice(int(user_input)), sep=", ")
           
        except ValueError:
            print("Please enter a valid number.")
        
if __name__ == "__main__":
    main()