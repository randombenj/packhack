import random
import bottle
import os

from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections


@bottle.post('/start')
def start():
    return "packe hacke"

@bottle.post('/chooseAction')
def move():
    data = PublicGameState(ext_dict=bottle.request.json)
    agent_id = data.agent_id
    our_player = data.publicPlayers[agent_id]
    our_x, our_y = our_player['position']
    game_grid = data.gameField
    weighted_game_grid = get_weighted_game_grid(game_grid)

    from .bstar import PathFinder

    printStateNice(data)
    print("OUR X: {}, OUR Y: {}".format(our_x, our_y))

    desired_point = find_point(game_grid)
    print("DESIRED POINT", desired_point)

    print()
    finder = PathFinder(None, None, weighted_game_grid)
    path = list(finder.astar((int(our_x), int(our_y)), desired_point))

    print("PATH", path)
    next_x, next_y = path[1]
    print("NEXT X: {}, NEXT Y: {}".format(next_x, next_y))

    move_x = next_x - our_x
    move_y = next_y - our_y

    #return get_direction(move_x, move_y)
    return ReturnDirections.NORTH

def find_point(game_grid):
    half_of_length = int(len(game_grid[0]) / 2)
    for y, rows in enumerate(game_grid):
        if "o" in rows[half_of_length:]:
            x = rows[half_of_length:].index("o")
            return (x, y)


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
            next_move = ReturnDirections.SOUTH
        if y == 1:
            next_move = ReturnDirections.NORTH
    elif y == 0:
        if x == -1:
            next_move = ReturnDirections.EAST
        if x == 1:
            next_move = ReturnDirections.WEST

    if not next_move:
        print("WTF doing random shit!!!")
        next_move = ReturnDirections.random()
    print("DON'T STOP MOVING: " + next_move)

def printStateNice(gState):
    print("Game State:")
    print("Field:")
    for y in reversed(range(len(gState.gameField))):
        for x in range(len(gState.gameField[y])):
            print(gState.gameField[y][x], end =" ")
        print()

def get_fucked(maze, our_x, our_y, move):
    direction = move
    if last_move is not None:
        print("get fucked")
        direction = ReturnDirections.random()

    next_move_char = ""
    if direction == ReturnDirections.SOUTH:
        next_move_char = maze[our_y + 1][our_x]
    elif direction == ReturnDirections.NORTH:
        next_move_char = maze[our_y - 1][our_x]
    elif direction == ReturnDirections.EAST:
        next_move_char = maze[our_y][our_x + 1]
    elif direction == ReturnDirections.WEST:
        next_move_char = maze[our_y][our_x - 1]
    return (next_move_char, direction)


application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080')
    )