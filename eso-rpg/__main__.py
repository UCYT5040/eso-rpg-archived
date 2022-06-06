import re
import levels, parse


def get_facing(level, coords, direction):
    if direction == 0:
        return level[coords[0] - 1][coords[1]]
    elif direction == 1:
        return level[coords[0]][coords[1] + 1]
    elif direction == 2:
        return level[coords[0] + 1][coords[1]]
    elif direction == 3:
        return level[coords[0]][coords[1] - 1]


def move_forward(amount, coords, direction):
    if direction == 0:
        return [coords[0] - amount, coords[1]]
    elif direction == 1:
        return [coords[0], coords[1] + amount]
    elif direction == 2:
        return [coords[0] + amount, coords[1]]
    elif direction == 3:
        return [coords[0], coords[1] - amount]


def main():
    try:
        with open('program.esorpg', 'r') as f:
            program = f.read()
    except FileNotFoundError:
        return print("Please create a program.esorpg file, and write your program there.")
    lines = program.split('\n')
    level = levels.levels[lines[0]]
    lines.pop(0)
    # Provided by https://www.codegrepper.com/code-examples/python/frameworks/-file-path-python/python+how+to+find+index+of+an+element+in+a+2d+list
    for y, x in enumerate(level):
        if '@' in x:
            player_coordinates = [y, x.index('@')]
    # End provided code
    level[player_coordinates[0]][player_coordinates[1]] = '0'
    player_facing = 0  # 0N, 1E, 2S, 3W
    dialogue = False
    vars_vals = {
        "e": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0],
        "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 2 else [0],
        "d": [1], "i": [get_facing(level, player_coordinates, player_facing)]}
    for line in lines:
        vars_vals, dialouge, player_facing, level = parse.parse(line, vars_vals, dialouge, player_facing, level)



main()
