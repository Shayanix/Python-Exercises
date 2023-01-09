def password_checker(password):
    with open('pass.txt','r') as f:
        common_passwords = f.read().splitlines()
        
        for common_passwords in enumerate(common_passwords):
            if password == common_passwords:
                print(f'{password} is too common ❌')
                return
        print (f'{password} is good to go ✅')
    
def main():
    password = input('Please enter your password: ')
    password_checker(password)
    
if __name__ == '__main__':
    main()