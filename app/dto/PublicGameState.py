import json

from app.dto.HelperDTOs import PublicFields
from app.dto.PublicPlayer import PublicPlayer


class PublicGameState:
    def __init__(self, gameState=None, jsonString=None):
        self.gameField = [[]]
        self.publicPlayers = []
        if jsonString != None:
            self._create_self_from_json(jsonString)
        else:
            layout = gameState.data.layout
            height, width = layout.height, layout.width
            self.gameField = [[PublicFields.WALL if layout.walls[x][y] else PublicFields.EMPTY for x in range(width)]
                              for y in range(height)]
            for agent in gameState.data.agentStates[:]:
                self.publicPlayers.append(PublicPlayer(isPacman=agent.isPacman,
                                                       direction=agent.getDirection(),
                                                       position=agent.getPosition(),
                                                       activeCapsule=(agent._scaredTimer > 0)))

    def _create_self_from_json(self, jsonString):
        loadedJsonString = json.loads(jsonString)
        for key, value in loadedJsonString.items():
            if key == "publicPlayers":
                self.publicPlayers = self._instance_players_out_of_json_string(value)
            if key == "gameField":
                self.gameField = self._instance_game_field_out_of_json_string(value)

    @staticmethod
    def _instance_game_field_out_of_json_string(jsonString):
        myGameField = [[]]
        for fieldRowElements in jsonString:
            myGameField.append(fieldRowElements)
        return myGameField

    @staticmethod
    def _instance_players_out_of_json_string(jsonString):
        myPublicPlayers = []
        for publicPlayersJsonString in jsonString:
            myPublicPlayers.append(PublicPlayer(jsonString=publicPlayersJsonString))
        return myPublicPlayers

    def __str__(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)
