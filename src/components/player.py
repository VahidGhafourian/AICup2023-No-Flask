# author: Mohamad Mahdi Reisi

# this is one of the most basic components of the Risk game.

class Player:
    def __init__(self, id, name, initializer, turn) -> None:
        self.nodes = []  # list of Node objects that owned by this player
        self.id = id  # each player has an id that is unique in the game
        self.name = name  # each player has a name
        self.number_of_troops_to_place = 0  # number of troops that the player have but not placed on the map
        self.is_ready = False  # a boolean that shows if the player is ready to get requests and play the game or not
        self.use_fort = False  # a boolean that shows if the player used fortify or not
        self.turn = turn  # turn function
        self.initializer = initializer  # initializer function
