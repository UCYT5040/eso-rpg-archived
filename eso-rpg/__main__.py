import levels, parse

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
        "e": [1] if len(levels.blocks[int(parse.get_facing(level, player_coordinates, player_facing))]['actions']) >= 1 else [0],
        "q": [1] if len(levels.blocks[int(parse.get_facing(level, player_coordinates, player_facing))]['actions']) >= 2 else [0],
        "d": [1], "i": [int(parse.get_facing(level, player_coordinates, player_facing))]}
    for line in lines:
        vars_vals, dialogue, player_facing, level = parse.parse(line, vars_vals, dialogue, player_facing, level)



main()
