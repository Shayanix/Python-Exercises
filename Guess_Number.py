from random import randint


lower_bound, upper_bound = 1, 100
random_number:int = randint(lower_bound, upper_bound)
print(f' Then answer is in range of {lower_bound} to {upper_bound}')

while True:
    
    try:
        user_guess = int(input('Guess the number: '))
    except ValueError as e:
        print('Please enter a valid number')
        continue
    
    if user_guess > random_number:
        print('Too high! Try again.')
    elif user_guess < upper_bound:
        print('Too low! Try again.')
    else:
        print('You guessed it right!')
        break

