import random
import sys


class RPS:
    
    def __init__(self):
        print('Welcome To The Rock,Paper and Scissor Game... :)')
        
        self.moves: dict = {'rock':'🗿','paper':'📃','scissors':'✂'}
        self.valid_moves: list[str] =list(self.moves.keys())
        
        
    def play_game(self):
        user_move:str = input('Rock, paper or scissors? >>').lower()
        
        if user_move == 'exit':
            print('goodbye 👋')
            sys.exit()
            
        if user_move not in self.valid_moves:
            print("invalid move")
            self.play_game()
            
        npc_move:str = random.choice(self.valid_moves)
        
        self.display_move(user_move,npc_move)
        self.check_move(user_move,npc_move)
        
    def display_move(self,user_move:str,npc_move:str):
        
        print('-'*25)
        
        print(f'you:{self.moves[user_move]}')
        
        print(f'Computer:{self.moves[npc_move]}')
        
        print('-'*25)
    
    def check_move(self,user_move:str,npc_move:str):
        
        if user_move == npc_move:
            print('it is tie...')
        elif user_move =='rock' and npc_move == 'scissors':
            print('you win!')
        elif user_move =='scissors' and npc_move =='paper':
            print('you win!')
        elif user_move =='paper' and npc_move == 'rock':
            print('you win!')
        else:
            print ('you lost...')

if __name__ == '__main__':
    rps = RPS()
    
    while True:
        rps.play_game()