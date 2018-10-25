import random
import bottle
import os
from app.dto.HelperDTOs import Directions
from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer

@bottle.post('/start')
def start():
    return "SomeFancyTeamName"


@bottle.post('/chooseAction')
def move():
    print(bottle.request.json)
    # TODO: Do things with data
    return random.choice(list(Directions))

application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))