# eso rpg

A fun esolang experience.

## Brief Overview

eso rpg is an esolang that you can build an RPG with.

There are levels built into the language, with characters and buildings. It is up to you to collect input and send output.

### Notes

- It is up to you to decide the dialogue. Each NPC has a dialogue ID.
- Blocks have IDs that correspond to the blocks type. You can decide what each type is.

## Language Basics

- Values
  - String
    - Stored as a list of ascii values.
    - Can be used as a digit.
      - When used as a digit, the value is equal to every character added.
    - Can be used a boolean.
      - 0 is false and 1 is true.
- Storage: There are variables 0-9, as well as other variables.
  - To get the value of one you type `/0` with `0` being the variable name. These can be used in strings. If you just want the value, use `'/0'`.
  - To set value, you just type the variable name, then `?`, and then the value on a line.
    - Example: `0?'hello'` sets `0` to `hello`.
- Output
  - You can output a string using `>`.
    - Example: `>'welcome to the rpg'`
- Input
  - You can collect text input using `<`. Specify a variable.
    - Example: `<0` sets `0` to a string.
  - You can collect y/n input using `,`. Specify a variable. Returns `0` (false) or `1` (true).
- Movement
  - Moving the character
    - w for up
    - a for left
    - s for down
    - d for right
    - e for forward (where you are looking)
    - q for backward
  - Looking
    - W for up
    - A for left
    - S for down
    - D for right
- If/If not
  - If uses parentheses (`()`) and if not uses brackets (`[]`).
  - Provide a variable to check. Must be 0 or 1, otherwise error.
  - Example: `(d(q>'This dialogue has two buttons')[q>'This dialogue has one button.'])` This checks if the user is in a dialogue. If there is a secondary interaction available, it outputs that there are two buttons. If the secondary interations is not available, it outputs false. Note that `d` returns boolean of if user is in a dialogue, and `q` returns is a secondary interaction is available.
- Values
  - Values are just like variables, but they can't be set.
  - `e`
    - Boolean for if the facing block is primary interactable.
    - If in dialogue, this is always true because there is no dialogue that doesn't have a single button.
  - `q`
    - Boolean for is the facing block is secondary interactable.
    - If in dialogue, boolean for if there is a second button.
  - `d`
    - Boolean for if in dialogue.
  - `i`
    - Returns ID of the facing block.
  - `o`
    - Returns ID of the open dialogue.
      - ID is used to identify who is saying something, not what is being said.
    - Error if dialogue is not open.
