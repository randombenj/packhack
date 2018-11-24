import random
import bottle
import os
import time

from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections

last_desired_point = None
last_desired_point_reached = False
last_home_point = None

eaten_big_points = 0

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
    our_y = int((len(data.gameField) - our_y) - 1)
    our_x = int(our_x)
    game_grid = data.gameField
    game_grid.reverse()
    
    weighted_game_grid = get_weighted_game_grid(data.gameField, agent_id)

    from .bstar import PathFinder

    print_state_nice(game_grid, our_x, our_y)
    print("OUR X: {}, OUR Y: {}".format(our_x, our_y))

    
    desired_point = get_next_point(data, game_grid, agent_id, our_x, our_y)
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


def get_next_point(data, game_grid, agent_id, our_x, our_y):
    global last_desired_point
    global last_desired_point_reached
    global last_home_point
    global eaten_big_points
 
    if last_desired_point is not None:
        if (our_x) == last_desired_point[0] and (our_y) == last_desired_point[1]:
            print("Reached and go home")
            eaten_big_points += 1
            last_desired_point_reached = True
            last_desired_point = None

            desired_point = find_point_home(game_grid, agent_id)
            last_home_point = desired_point
            return desired_point

        else:
            return last_desired_point
    else:
        if last_desired_point_reached and last_home_point is None:
            desired_point = find_point_home(game_grid, agent_id)
            last_home_point = desired_point
            return desired_point
        else:
            if last_desired_point is None and last_home_point is None:
                desired_point = find_point(data.gameField, "o")
                last_desired_point = desired_point
                return desired_point

            if (our_x) == last_home_point[0] and (our_y) == last_home_point[1]:
                last_home_point = None
                last_desired_point_reached = False

                if eaten_big_points < 2:
                    desired_point = find_point(data.gameField, "o")
                else:
                    desired_point = find_point(data.gameField, "°")

                last_desired_point = desired_point
                return desired_point
            else:
                return last_home_point



def find_point_home(game_grid, agent_id):
    half_of_length = int(len(game_grid[0]) / 2)

    if agent_id == 0:
        x = half_of_length - 1
    elif agent_id == 1:
        x = half_of_length + 2

    for y, rows in enumerate(game_grid):
        if rows[x] == " ":
            return (x, y)


def find_point(game_grid, search_for):
    half_of_length = int(len(game_grid[0]) / 2)
    for y, rows in enumerate(game_grid):
        if search_for in rows[half_of_length:]:
            x = rows[half_of_length:].index(search_for)
            return (half_of_length + x, y)


def get_weighted_game_grid(game_grid, agent_id):
    field_lenght = int(len(game_grid[0]) / 2)
    weighted_game_grid = []
    for rows in game_grid:
        weighted_row = []
        for idx,col in enumerate(rows):
            w = 1
            if col == "%":
                w = 0
            elif col == "o" and compare_based_on_agent(idx, field_lenght, agent_id):
                w = 5
            elif col == "°" and compare_based_on_agent(idx, field_lenght, agent_id):
                w = 2
            weighted_row.append(w)
        weighted_game_grid.append(weighted_row)
    return weighted_game_grid

def compare_based_on_agent(idx, field_lenght, agent_id):
    if agent_id == 0:
        return idx >= field_lenght
    if agent_id == 1:
        return idx <= field_lenght


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