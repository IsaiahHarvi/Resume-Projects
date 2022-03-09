import os
maze = ['########## #########', '#        #    # #  #', '#### ### #### # ## #', '#      # #       # #', '## ### #   #####   #', '#    # #####     ###', '#### # #     ###   #', '#    ### ## ##   # #', '#    # #  #  # ### #', '###### ## # #    # #', '# #     # #  ##### #', '# # ##### ##  # #  #', '#          ## # # ##', '# #############   ##', '#  #    # #   ######', '## ###    # #   #  #', '#       # ###   #  #', '####### #     #   ##', '#       ### # #    #', '####################']
player = [18,11]
while player != [0,10]:
    mazes = ''
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if i == player[0] and j == player[1]:
                mazes += '0'
            else:
                mazes += maze[i][j]
        mazes += '\n'
    print(mazes)
    directions = {'w':[-1,0], 's':[1,0], 'a':[0,-1], 'd':[0,1]}
    direction = input('Enter direction (wasd)\n').lower()
    if direction in directions:
        if maze[player[0] + directions[direction][0]][player[1] + directions[direction][1]] != '#':
            player[0] += directions[direction][0]
            player[1] += directions[direction][1]
    os.system('cls')
print('YOU ESCAPED!')
