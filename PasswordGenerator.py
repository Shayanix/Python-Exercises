import string
import secrets


def contain_uppercase(password):
    for char in password:
        if char in string.ascii_uppercase:
            return True
        
        else:
            return False
        
def contain_special_character(password):
    for char in password:
        if char in string.punctuation:
            return True
        
        else:
            return False
        
def generate_password(length,special_char,uppercase):
    combined = string.ascii_lowercase + string.digits
    
    if special_char:
        combined += string.punctuation
        
    if uppercase:
        combined += string.ascii_uppercase
        
    combined_length = len(combined)
    
    new_password = ''
    
    for _ in range(length):
        new_password += combined[secrets.randbelow(combined_length)]
        
    return new_password

if __name__ == '__main__':
    for i in range(10):
        
        new_pass = generate_password(10,True,True)
        print(f'{i+1} ----> {new_pass}')