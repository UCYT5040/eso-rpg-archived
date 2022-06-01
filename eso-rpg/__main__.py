import re
import levels

def get_facing(level, coords, direction):
    if direction == 0:
        return level[coords[0]-1][coords[1]]
    elif direction == 1:
        return level[coords[0]][coords[1]+1]
    elif direction == 2:
        return level[coords[0]+1][coords[1]]
    elif direction == 3:
        return level[coords[0]][coords[1]-1]
def move_forward(amount, coords, direction):
    if direction == 0:
        return [coords[0]-amount, coords[1]]
    elif direction == 1:
        return [coords[0], coords[1]+amount]
    elif direction == 2:
        return [coords[0]+amount, coords[1]]
    elif direction == 3:
        return [coords[0], coords[1]-amount]
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
    player_facing = 0 # 0N, 1E, 2S, 3W
    dialogue = False
    vars_vals = {"e": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0], "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 2 else [0], "d": [1] if dialouge else [0], "i": [get_facing(level, player_coordinates, player_facing)]}
    for line in lines:
        if_stack = 0 # +1 for every (, -1 for every ). Should be 0 by the end of the line.
        if_not_stack = 0
        skip_stack = 0 # While >0, skip the character.
        string_builder = [] # When in string mode, each new character is added here.
        string_mode = False
        skip_until_end_if = False
        skip_until_end_not = False
        action_on_string_finish = None # Something like "print" or "set"
        variable_to_set = None # Used for when setting a variable for action_on_string_finish
        for iteration in range(len(line)):
            if skip_stack > 0:
                skip_stack -= 1
                continue
            char = line[iteration]
            if skip_until_end_if:
                if char == ')':
                    skip_until_end_if = False
            if skip_until_end_not:
                if char == ']':
                    skip_until_end_not = False
            elif string_mode:
                if char == "'":
                    string_mode = False
                    if action_on_string_finish == "print":
                        print(''.join([chr(x) for x in string_builder]), end='')
                elif char == '\\':
                    skip_stack += 1
                    string_builder.append(ord(line[iteration + 1]))
                elif char == '/':
                    skip_stack += 1
                    for x in vars_vals[line[iteration + 1]]:
                        string_builder.append(x)
                else:
                    string_builder.append(ord(char))
            elif char == '(':
                skip_stack += 1
                try:
                    if vars_vals[line[iteration+1]][0] == 1:
                        if_stack += 1
                except KeyError:
                    return print("!!! eso rpg error !!!\nif statement requesting a variable or value that doesn't exist yet")
            elif char == '[':
                skip_stack += 1
                try:
                    if vars_vals[line[iteration+1]][0] != 1:
                        if_not_stack += 1
                except KeyError:
                    return print("!!! eso rpg error !!!\nif not statement requesting a variable or value that doesn't exist yet")
            elif char == '>':
                action_on_string_finish = "print"
            elif char == "'":
                string_mode = True
            elif char == '<':
                vars_vals[line[iteration + 1]] = [ord(x) for x in input()]
            elif char == ')':
                if_stack -= 1
            elif char == ']':
                if_not_stack -= 1
            elif char == 'w':
                player_coordinates[0] += 1
                vars_vals = {"e": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0], "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 2 else [0], "i": [get_facing(level, player_coordinates, player_facing)]}
            elif char == 'a':
                player_coordinates[1] -= 1
                vars_vals = {"e": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0], "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 2 else [0], "i": [get_facing(level, player_coordinates, player_facing)]}
            elif char == 's':
                player_coordinates[0] -= 1
                vars_vals = {"e": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0], "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 2 else [0], "i": [get_facing(level, player_coordinates, player_facing)]}
            elif char == 'd':
                player_coordinates[1] += 1
                vars_vals = {"e": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0], "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 2 else [0], "i": [get_facing(level, player_coordinates, player_facing)]}
            elif char == 'e':
                player_coordinates = move_forward()
            elif char == 'q':
                ...
            else:
                if not re.search("(\\(.|\\[.)*.\?'.*'(\\)|\\])*", line) is None:
                    statement = re.sub('(\\(.)|(\\[.)|(\\])|(\\))', '', line).split('?')
                    vars_vals[statement[0]] = statement[1]

main()
