import json
from app.dto.PublicPlayer import PublicPlayer


class PublicGameState:
    def __init__(self, ext_dict=None):
        self.agent_id = 0
        self.gameField = [[]]
        self.publicPlayers = []
        if ext_dict is not None:
            self.__dict__ = ext_dict

    def __str__(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)
