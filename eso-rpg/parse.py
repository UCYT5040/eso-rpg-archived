def parse_code(code, vars_vals, dialouge, player_facing, level):
    if_stack = 0  # +1 for every (, -1 for every ). Should be 0 by the end of the line.
    if_not_stack = 0
    while_stack = 0
    skip_stack = 0  # While >0, skip the character.
    string_builder = []  # When in string mode, each new character is added here.
    string_mode = False
    skip_until_end_if = False
    skip_until_end_not = False
    skip_until_end_while = False
    action_on_string_finish = None  # Something like "print" or "set"
    variable_to_set = None  # Used for when setting a variable for action_on_string_finish
    for iteration in range(len(line)):
        if skip_stack > 0:
            skip_stack -= 1
            continue
        char = line[iteration]
        if skip_until_end_if:
            if char == ')':
                skip_until_end_if = False
        elif skip_until_end_not:
            if char == ']':
                skip_until_end_not = False
        elif skip_until_end_while:
            if char == '}':
                skip_until_end_while = False
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
                if vars_vals[line[iteration + 1]].sum() == 1:
                    if_stack += 1
            except KeyError:
                print(
                    "!!! eso rpg error !!!\nif statement requesting a variable or value that doesn't exist yet")
        elif char == '[':
            skip_stack += 1
            try:
                if vars_vals[line[iteration + 1]].sum() != 1:
                    if_not_stack += 1
            except KeyError:
                print(
                    "!!! eso rpg error !!!\nif not statement requesting a variable or value that doesn't exist yet")
        elif char == '{':
            skip_stack += 1
            try:
                if vars_vals[line[iteration + 1]].sum() == 1:
                    code = ""
                    code_finder_position = iteration + 1
                    while line[code_finder_position + 1] != '}':
                        code += line[code_finder_position + 1]
                    while_stack.append([vars_vals[line[iteration + 1]], code])
                else:
                    skip_until_end_while = True
            except KeyError:
                return print(
                    "!!! eso rpg error !!!\nwhile statement requesting a variable or value that doesn't exist yet")
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
        elif char == '}':
            for while_loop in while_stack:
                # try: isn't needed here because this only happens when we already checked it earlier
                if while_loop[0].sum() == 1:
                    vars_vals, dialouge, player_facing, level = parse_code(while_loop[1], vars_vals, dialouge, player_facing, level)
        elif char == 'w':
            player_coordinates[0] += 1
            vars_vals = {"e": [1] if len(
                levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0],
                            "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)][
                                                'actions']) >= 2 else [0],
                            "i": [get_facing(level, player_coordinates, player_facing)]}
        elif char == 'a':
            player_coordinates[1] -= 1
            vars_vals = {"e": [1] if len(
                levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0],
                            "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)][
                                                'actions']) >= 2 else [0],
                            "i": [get_facing(level, player_coordinates, player_facing)]}
        elif char == 's':
            player_coordinates[0] -= 1
            vars_vals = {"e": [1] if len(
                levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0],
                            "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)][
                                                'actions']) >= 2 else [0],
                            "i": [get_facing(level, player_coordinates, player_facing)]}
        elif char == 'd':
            player_coordinates[1] += 1
            vars_vals = {"e": [1] if len(
                levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0],
                            "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)][
                                                'actions']) >= 2 else [0],
                            "i": [get_facing(level, player_coordinates, player_facing)]}
        elif char == 'e':
            player_coordinates = move_forward(1, player_coordinates, player_facing)
            vars_vals = {"e": [1] if len(
                levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0],
                            "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)][
                                                'actions']) >= 2 else [0],
                            "i": [get_facing(level, player_coordinates, player_facing)]}
        elif char == 'q':
            player_coordinates = move_forward(-1, player_coordinates, player_facing)
            vars_vals = {"e": [1] if len(
                levels.blocks[get_facing(level, player_coordinates, player_facing)]['actions']) >= 1 else [0],
                            "q": [1] if len(levels.blocks[get_facing(level, player_coordinates, player_facing)][
                                                'actions']) >= 2 else [0],
                            "i": [get_facing(level, player_coordinates, player_facing)]}
        elif char == 'W':
            player_facing = 0
        elif char == 'D':
            player_facing = 1
        elif char == 'S':
            player_facing = 2
        elif char == 'A':
            player_facing = 3
        else:
            if not re.search("(\\(.|\\[.)*.\\?'.*'(\\)|\\])*", line) is None:
                statement = re.sub('(\\(.)|(\\[.)|(\\])|(\\))', '', line).split('?')
                vars_vals[statement[0]] = statement[1]
    return (vars_vals, dialouge, player_facing, level)