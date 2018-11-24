import random
import bottle
import os
import time

from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections


@bottle.post('/start')
def start():
    return "packe hacke"

@bottle.post('/chooseAction')
def move():
    start = time.time()
    data = PublicGameState(ext_dict=bottle.request.json)
    agent_id = data.agent_id
    our_player = data.publicPlayers[agent_id]
    our_x, our_y = our_player['position']
    our_y = (len(data.gameField) - our_y) - 1
    game_grid = data.gameField
    game_grid.reverse()
    
    weighted_game_grid = get_weighted_game_grid(data.gameField)

    from .bstar import PathFinder

    print_state_nice(game_grid, our_x, our_y)
    print("OUR X: {}, OUR Y: {}".format(our_x, our_y))

    desired_point = find_point(data.gameField)
    print("DESIRED POINT", desired_point)

    print()
    finder = PathFinder(None, None, weighted_game_grid)
    path = list(finder.astar((int(our_x), int(our_y)), desired_point))

    print("PATH", path)
    next_x, next_y = path[1]
    print("NEXT X: {}, NEXT Y: {}".format(next_x, next_y))

    move_x = next_x - our_x
    move_y = next_y - our_y
    
    direction = get_direction(move_x, move_y)

    print(time.time()-start)
    return direction

def find_point(game_grid):
    half_of_length = int(len(game_grid[0]) / 2)
    for y, rows in enumerate(game_grid):
        if "o" in rows[half_of_length:]:
            x = rows[half_of_length:].index("o")
            return (half_of_length + x, y)


def get_weighted_game_grid(game_grid):
    weighted_game_grid = []
    for rows in game_grid:
        weighted_row = []
        for col in rows:
            w = 10
            if col == "%":
                w = 0
            elif col == "O":
                w = 5
            elif col == "o":
                w = 2
            weighted_row.append(w)
        weighted_game_grid.append(weighted_row)
    return weighted_game_grid


def get_direction(x, y):
    print("X: {}, Y: {}".format(x, y))
    next_move = None
    if x == 0:
        if y == -1:
            next_move = ReturnDirections.NORTH
        if y == 1:
            next_move = ReturnDirections.SOUTH
    elif y == 0:
        if x == -1:
            next_move = ReturnDirections.WEST
        if x == 1:
            next_move = ReturnDirections.EAST

    if not next_move:
        print("WTF doing random shit!!!")
        next_move = ReturnDirections.random()
    print("DON'T STOP MOVING: " + next_move)
    return next_move

def print_state_nice(gameField, our_x, our_y):
    print("Game State:")
    for y,row in enumerate(gameField):
        for x,col in enumerate(row):
            if y == our_y and x == our_x:
                print(":D",end =" ")
            else:
                print(col, end =" ")
        print()

application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080')
    )