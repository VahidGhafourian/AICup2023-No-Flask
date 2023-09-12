import requests
from src.blueprints import BluePrints


class ClientGame:
    def __init__(self, main_game) -> None:
        self.main_game = main_game
        self.blueprints = BluePrints

    def output_handler(self, output):
        """
            handles the output of the server
        """
        if 'error' in output:
            raise Exception("player_id: " + str(self.get_player_id()['player_id']) + " error: " + output['error'])
        return output
    
    def __check_int(self, n):
        return n if type(n) == int else int(n)

    def __check_float(self, n):
        return n if type(n) == float else float(n)

    def get_owners(self):
        """
            returns a dictionary of node_id: owner_id
            node_id: str
            owner_id: int
        """

        return self.output_handler(self.blueprints.get_owners(self.main_game))

    def get_number_of_troops(self):
        """
            returns a dictionary of node_id: number_of_troops
            node_id: str
            number_of_troops: int
        """
        return self.output_handler(self.blueprints.get_troops_count(self.main_game))

    def get_state(self):
        """
            returns a dictionary containing the state of the game
            1: put_troop
            2: attack
            3: move_troop
            4: fort
            {'state': number_of_state}
        """
        return self.output_handler(self.blueprints.get_state(self.main_game))

    def get_turn_number(self):
        """
            returns a dictionary containing the turn number
            {'turn_number': number_of_turn}
        """
        return self.output_handler(self.blueprints.get_turn_number(self.main_game))

    def get_adj(self):
        """
            return the adjacent nodes of each node
            returns a dictionary of node_id: [adjacent_nodes]
            node_id: str
            adjacent_nodes: list of int
        """
        return self.blueprints.get_adj(self.main_game)

    def next_state(self):
        """
            changes the state of the turn to the next state
        """
        return self.output_handler(self.blueprints.next_state(self.main_game))

    def put_one_troop(self, node_id):
        """
            puts one troop in the node with the given id
            this function can only be used in the put_troop state in the initialize function
        """
        node_id = self.__check_int(node_id)
        return self.output_handler(self.blueprints.put_one_troop(node_id, self.main_game, self.get_player_id()['player_id']))

    def put_troop(self, node_id, num):
        """
            puts num troops in the node with the given id
            this function can only be used in the put_troop state in the turn function
        """
        node_id = self.__check_int(node_id)
        num = self.__check_int(num)
        return self.output_handler(self.blueprints.put_troop(node_id, num, self.main_game, self.get_player_id()['player_id']))

    def get_player_id(self):
        """
            returns the id of the player
        """
        return self.output_handler(self.blueprints.get_player_id(self.main_game))

    def attack(self, attacking_id, target_id, fraction, move_fraction):
        """
            attacks the target node with the given fraction of troops
        """
        attacking_id = self.__check_int(attacking_id)
        target_id = self.__check_int(target_id)
        fraction = self.__check_float(fraction)
        move_fraction = self.__check_float(move_fraction)
        return self.output_handler(self.blueprints.attack(attacking_id, target_id, fraction, move_fraction, self.main_game,
                                      self.get_player_id()['player_id']))

    def move_troop(self, source, destination, troop_count):
        """
            moves the given number of troops from the source node to the destination node
        """
        source = self.__check_int(source)
        destination = self.__check_int(destination)
        troop_count = self.__check_int(troop_count)
        return self.output_handler(self.blueprints.move_troop(source, destination, troop_count, self.main_game,
                                          self.get_player_id()['player_id']))

    def get_strategic_nodes(self):
        """
            returns a list of strategic nodes and their score
            {"strategic_nodes": [node_id, ...], "score": [score, ...]}
        """
        return self.output_handler(self.blueprints.get_strategic_nodes(self.main_game))

    def get_number_of_troops_to_put(self):
        """
            returns the number of troops that the player can put in the put_troop state
            {"number_of_troops": number_of_troops}
        """
        return self.output_handler(self.blueprints.get_number_of_troops_to_put(self.main_game))

    def get_reachable(self, node_id):
        """
            returns a dictionary of "reachable" key and a list of reachable nodes
            {"reachable": [node_id, ...]}
        """
        node_id = self.__check_int(node_id)
        return self.output_handler(self.blueprints.get_reachable(node_id, self.main_game))

    def get_number_of_fort_troops(self):
        """
            returns the number of troops that used to defend the node
            {node_id: number_of_troops, ...}
            node_id: str
            number_of_troops: int
        """
        return self.output_handler(self.blueprints.get_number_of_fort_troops(self.main_game))

    def fort(self, node_id, troop_count):
        """
            fortifies the node with the given number of troops
        """
        node_id = self.__check_int(node_id)
        troop_count = self.__check_int(troop_count)
        self.output_handler(self.blueprints.fort(node_id, troop_count, self.main_game, self.get_player_id()['player_id']))
