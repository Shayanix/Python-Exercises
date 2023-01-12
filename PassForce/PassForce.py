import itertools
import string
import time


def usual_guess(word):
    with open('pass.txt','r') as file:
        
        word_list = file.read().splitlines()
        
        for i, match in enumerate(word_list,start=1):
            if match == word:
                return f'Common match :{match} (#{i})'
            
def brute_force(word,length,digits,symbol):
    char = string.ascii_lowercase
    
    if symbol:
        char += string.punctuation
        
    if digits:
        char += string.digits
        
    attempts = 0
    
    for guess in itertools.product(char,repeat=length):
        attempts +=1
        guess = ''.join(guess)
        
        
        if guess == word:
            return f'password is {guess} and attempts are {attempts}'
        
def main():
    
    print('searching ....')
    
    password = 'pass1'
    
    start_time = time.perf_counter()
    
    if common_match := usual_guess(password):
        print(common_match)
    else:
        if cracked := brute_force(password,length=5,digits=True,symbol=True):
            print(cracked)
        else:
            print('There is NO matched')
    end_time = time.perf_counter()
    
    print(round(end_time-start_time,2),'s')
    
if __name__ == '__main__':
    main()
    
    