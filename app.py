import threading
import readchar
import time
from random import randint
from enum import Enum

BOARD_GAME_SIZE = 8

class SquareValue(Enum):
    SNAKE = "🟢"
    APPLE = "🍎"
    EMPTY = "⬜"

class MoveDirection(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"

def create_board_game():
    board_game = []

    for linha in range(0, BOARD_GAME_SIZE):
        board_game.append([])
        for _ in range(0, BOARD_GAME_SIZE):
            board_game[linha].append(SquareValue.EMPTY)
    
    return board_game

def define_snake_initial_position(board_game):
    snake_line = randint(0, len(board_game) - 1)
    snake_column = randint(0, len(board_game[snake_line]) - 1)
    board_game[snake_line][snake_column] = SquareValue.SNAKE

    return snake_line, snake_column

def define_new_apple_position(board_game):
    while True:
        apple_line = randint(0, len(board_game) - 1)
        apple_column = randint(0, len(board_game[apple_line]) - 1)
        if not is_a_snake(board_game, apple_line, apple_column):
            board_game[apple_line][apple_column] = SquareValue.APPLE
            break

def listen_to_user_keyboard(game_state):
    while True:
        key = readchar.readkey()
        if key == readchar.key.UP:
            game_state["move_direction"] = MoveDirection.UP
        elif key == readchar.key.DOWN:
            game_state["move_direction"] = MoveDirection.DOWN
        elif key == readchar.key.LEFT:
            game_state["move_direction"] = MoveDirection.LEFT
        elif key == readchar.key.RIGHT:
            game_state["move_direction"] = MoveDirection.RIGHT
    
def display_game(board_game):
    for linha in range (len(board_game)):
        for coluna in range (len(board_game[linha])):
            print(board_game[linha][coluna].value, end=" ")
        print()

def compute_next_snake_movement(snake_line, snake_column, move_direction):
    if move_direction == MoveDirection.RIGHT:
        snake_column += 1

    elif move_direction == MoveDirection.LEFT:
        snake_column -= 1

    elif move_direction == MoveDirection.UP:
        snake_line -= 1
        
    elif move_direction == MoveDirection.DOWN:
        snake_line += 1

    return snake_line, snake_column

def hit_the_wall(board_game, snake_line, snake_column):
    return snake_line < 0 or snake_line > len(board_game) - 1 or snake_column < 0 or snake_column > len(board_game[snake_line]) - 1

def won_the_game(board_game, snake_positions):
    return len(snake_positions) == len(board_game) * len(board_game[0])

def is_a_snake(board_game, snake_line, snake_column):
    return board_game[snake_line][snake_column] == SquareValue.SNAKE

def is_an_apple(board_game, snake_line, snake_column):
    return board_game[snake_line][snake_column] == SquareValue.APPLE

def run():
    board_game = create_board_game()
    game_state = {"move_direction": None}

    threading.Thread(target=listen_to_user_keyboard, args=(game_state,), daemon=True).start()

    snake_line, snake_column = define_snake_initial_position(board_game)
    snake_positions = [[snake_line, snake_column]]

    define_new_apple_position(board_game)

    print("Welcome to PySnake!") 
    display_game(board_game)

    while game_state["move_direction"] == None:
        time.sleep(1)

    while True:
        print()
        display_game(board_game)

        time.sleep(0.4)
        
        next_snake_line, next_snake_column = compute_next_snake_movement(snake_line, snake_column, game_state["move_direction"])

        if hit_the_wall(board_game, next_snake_line, next_snake_column):
            print("You lost! You hit the wall :(")
            return

        if is_a_snake(board_game, next_snake_line, next_snake_column):
            print("You lost! You hit itself :(")
            return
    
        did_snake_ate_an_apple = is_an_apple(board_game, next_snake_line, next_snake_column)

        board_game[next_snake_line][next_snake_column] = SquareValue.SNAKE
        snake_positions.append([next_snake_line, next_snake_column])

        if won_the_game(board_game, snake_positions):
            print("You won the game!")
            break

        if did_snake_ate_an_apple:
            define_new_apple_position(board_game)
        else:
            snake_tail_line, snake_tail_column = snake_positions.pop(0)
            board_game[snake_tail_line][snake_tail_column] = SquareValue.EMPTY

        snake_line = next_snake_line
        snake_column = next_snake_column

if __name__ == "__main__": 
    run()