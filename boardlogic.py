import random

player = 0
roll = 0

board = { 4 : 8 , 7 : 5 , 10 : 9}


def diceroll():
    global roll                         #Gives the function access to change the value of the original roll variable
    roll = random.randint(1,6)
    print("Dice Rolled on ",roll)

def snl():
    global player                       #Gives the function access to change the value of the original player variable
    if player in board:
        player = board[player]