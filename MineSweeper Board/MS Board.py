# Randomly generates a minesweeper board

from random import randint

board = [] 
for i in range(16):
    board.append([])
    for j in range(30):
        board[i].append(0)


bombs = 0
while bombs != 99:
    Index = randint(0,29)
    ListIndex = randint(0,15)
    if board[ListIndex][Index] != 'B':
        board[ListIndex][Index] = 'B'
        bombs += 1


for i in range(len(board)):
    print(*board[i])

input()
