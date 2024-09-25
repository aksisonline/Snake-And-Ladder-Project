import random

player = 0
roll = 0

# square number : where to move if landed
board = { 4 : 8 , 7 : 5 , 10 : 9}

#Rolls the dice and prints the number rolled
def diceroll():
    global roll                         #Gives the function access to change the value of the original roll variable
    roll = random.randint(1,6)
    print("Dice Rolled on ",roll)

#If player lands on one of the snakes or ladders, the player will move to the new position
def snl():
    global player                       #Gives the function access to change the value of the original player variable
    if player in board:
        player = board[player]