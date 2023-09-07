import random
from tools.find_reachable import find_reachable
# author: Vahid Ghafourian
# Date: 2023/09/06

from tools.find_path import find_path

class Kernel:
    def __init__(self, main_game, kernel_config) -> None:
        # initialize the player_id
        self.player_id = 0
        self.main_game = main_game
        self.kernel_config = kernel_config
        self.main_game.config = self.kernel_config


    def attack(self, attacking_id, target_id, fraction, move_fraction, player_id):
        # this API used to attack a node from another node

        # the body of the request should be like this
        ## attacking_id : the id of the node that will attack
        ## target_id : the id of the node that will be attacked
        ## fraction: the attack continues until the number of troops in the attacking node is fraction of the number of troops in the target node or the attacking node has only one troop or the target node has no troops
        ## move_fraction: the fraction of troops of attacking_id that will move to the target node after a successful attack

        # check if the game is in the turn state
        if self.main_game.game_state != 2:
            return {'error': 'The game is not in the turn state'}

        # check if the game is in the attack state
        if self.main_game.state != 2:
            return {'error': 'The game is not in the attack state'}

            # check if the attacking_id is valid
        if attacking_id not in self.main_game.nodes.keys():
            return {'error': 'attacking_id is not valid'}

        # check if the attacking_id has a owner
        if self.main_game.nodes[attacking_id].owner == None:
            return {'error': 'attacking_id does not have any owner'}

        # check if the attacking_id is owned by the player
        if self.main_game.nodes[attacking_id].owner.id != player_id:
            return {'error': 'attacking_id is not owned by the player'}

        # check if the target_id is valid
        if target_id not in self.main_game.nodes.keys():
            return {'error': 'target_id is not valid'}

        # check if the target_id has a owner
        if self.main_game.nodes[target_id].owner == None:
            return {'error': 'target_id does not have any owner'}

        # check if the target_id is not owned by the player
        if self.main_game.nodes[target_id].owner.id == player_id:
            return {'error': 'target_id is owned by the player'}
        try:
            fraction = float(fraction)
        except:
            return {'error': 'fraction is not valid it should be float'}

        try:
            move_fraction = float(move_fraction)
        except:
            return {'error': 'move_fraction is not valid it should be float'}

        # check if move fraction is between 0 and 1
        if move_fraction < 0 or move_fraction > 1:
            return {'error': 'move_fraction should be between 0 and 1'}

        # check if the player has at least 2 troops in the attacking node
        if self.main_game.nodes[attacking_id].number_of_troops < 2:
            return {'error': 'attacking node does not have enough troops'}

        # check if the fraction is a positive number
        if fraction < 0:
            return {'error': 'fraction should be positive'}

        # check if the attacker_id and target_id are connected
        if self.main_game.nodes[attacking_id] not in self.main_game.nodes[target_id].adj_main_map:
            return {'error': 'attacking_id and target_id are not connected'}

        attacker_troops = self.main_game.nodes[attacking_id].number_of_troops  # number of troops in the attacking node
        target_troops = self.main_game.nodes[target_id].number_of_troops + self.main_game.nodes[
            target_id].number_of_fort_troops  # number of troops in the target node

        # save the number of fort troops in the target node
        fort_troops = self.main_game.nodes[target_id].number_of_fort_troops
        normal_troops = self.main_game.nodes[target_id].number_of_troops

        while attacker_troops > 1 and target_troops > 0 and attacker_troops / target_troops > fraction:
            if attacker_troops > 3:
                attacker_dice = 3
            else:
                attacker_dice = attacker_troops - 1

            if target_troops >= 2:
                target_dice = 2
            else:
                target_dice = target_troops

            attacker_dice_list = []
            target_dice_list = []

            for _ in range(attacker_dice):
                attacker_dice_list.append(random.randint(1, 6))
            for _ in range(target_dice):
                target_dice_list.append(random.randint(1, 6))

            attacker_dice_list.sort(reverse=True)
            target_dice_list.sort(reverse=True)
            if self.main_game.config['debug_dice']:
                self.main_game.print(f'attacker troops: {attacker_troops} target troops: {target_troops}')
                self.main_game.print(f"attacker dice: {attacker_dice_list}" + f" target dice: {target_dice_list}")

            for i in range(min(attacker_dice, target_dice)):
                if attacker_dice_list[i] > target_dice_list[i]:
                    target_troops -= 1
                else:
                    attacker_troops -= 1
            if self.main_game.config['debug_dice']:
                self.main_game.print(f"new attacker troops: {attacker_troops}" + f" new target troops: {target_troops}")
                self.main_game.print(f'_________________________________________________________')

        # check if the attacker won
        if target_troops <= 0:
            move_troops = int(attacker_troops * move_fraction)
            if move_troops == 0:
                move_troops = 1

            if attacker_troops - move_troops < 1:
                move_troops -= 1
                attacker_troops += 1

            self.main_game.nodes[attacking_id].number_of_troops = attacker_troops - move_troops
            self.main_game.nodes[target_id].number_of_troops = move_troops
            self.main_game.nodes[target_id].number_of_fort_troops = 0

            self.main_game.remove_node_from_player(target_id, self.main_game.nodes[target_id].owner.id)
            self.main_game.add_node_to_player(target_id, player_id)
            if self.main_game.has_won_troop == False:
                self.main_game.player_turn.number_of_troops_to_place += self.main_game.config[
                    'number_of_troops_after_successful_attack']
                self.main_game.has_won_troop = True

        else:
            if fort_troops > 0:
                if target_troops <= normal_troops:
                    self.main_game.nodes[target_id].number_of_fort_troops = 0
                    self.main_game.nodes[target_id].number_of_troops = target_troops
                else:
                    self.main_game.nodes[target_id].number_of_fort_troops = target_troops - normal_troops


            else:
                self.main_game.nodes[target_id].number_of_troops = target_troops

            self.main_game.nodes[attacking_id].number_of_troops = attacker_troops

        log = {
            "attacker": attacking_id,
            "target": target_id,
            "new_troop_count_attacker": self.main_game.nodes[attacking_id].number_of_troops,
            "new_troop_count_target": self.main_game.nodes[target_id].number_of_troops,
            "new_target_owner": self.main_game.nodes[target_id].owner.id,
            "new_fort_troop": self.main_game.nodes[target_id].number_of_fort_troops
        }
        self.main_game.log_attack.append(log)
        if self.main_game.debug:
            self.main_game.print(
                f"player {player_id} attacked node {target_id} from node {attacking_id} with fraction {fraction}. successful: {target_troops <= 0}")

        if target_troops <= 0:
            return {'message': 'attack successful', 'won': 1}
        else:
            return {'message': 'attack successful', 'won': 0}

    def fort(self, node_id, troop_count, player_id):
        # this API used to apply the fortification ability of the player

        # the body of the request should be like this
        ## node_id : the id of the node that will be fortified
        ## troop_count : the number of troops that will be fortified

        # check if the Game is in the turn state
        if self.main_game.game_state != 2:
            return {'error': 'The game is not in the turn state'}

        # check if the turn is in the fort state
        if self.main_game.state != 4:
            return {'error': 'The game is not in the fort state'}

        # check if the node_id is valid
        if node_id not in self.main_game.nodes.keys():
            return {'error': 'node_id is not valid'}

        # check the ownership status of the node
        # check if the node has an owner
        if self.main_game.nodes[node_id].owner is None:
            return {'error': 'This node has no owner'}

        # check if the node is owned by the player
        if self.main_game.nodes[node_id].owner.id != player_id:
            return {'error': 'This node is already owned by another player'}

        # check if the troop_count is valid
        if troop_count >= self.main_game.nodes[node_id].number_of_troops:
            return {'error': 'there is not enough troops in the node'}

        # check if the player hasn't used the fortification ability in the game
        if self.main_game.player_turn.use_fort:
            return {'error': 'you have already used the fortification ability in the game'}

        # start the fortification ability
        self.main_game.player_turn.use_fort = True

        # fortify the node
        self.main_game.nodes[node_id].number_of_troops -= troop_count
        self.main_game.nodes[node_id].number_of_fort_troops += self.main_game.config['fort_coef'] * troop_count

        if self.main_game.debug:
            self.main_game.print(f"player {player_id} fortified node {node_id} with {troop_count} troops")

        return {'success': 'the fortification ability is applied successfully'}

    def get_adj(self):
        # this API used to the list of the adjacent nodes of each node
        output_dict = {}
        for node in self.main_game.nodes.values():
            output_dict[node.id] = [i.id for i in node.adj_main_map]

        return output_dict

    def get_number_of_fort_troops(self):
        # this API used to get the number of fort troops on each node
        output_dict = {}
        for node in self.main_game.nodes.values():
            output_dict[node.id] = node.number_of_fort_troops
        return output_dict

    def get_number_of_troops_to_put(self):
        # return the number of troops that the player can put on the map
        output_dict = {"number_of_troops": self.main_game.player_turn.number_of_troops_to_place}
        return output_dict

    def get_owners(self, player_id):
        output_dict = {}
        for node in self.main_game.nodes.values():
            if node.owner != None:
                output_dict[node.id] = node.owner.id
            else:
                output_dict[node.id] = -1
        return output_dict

    def get_player_id(self, player_id):
        output_dict = {'player_id': player_id}
        return output_dict

    def get_reachable(self, node_id):
        # this API used to find all the nodes that the owner can move it's troops from node_id to them
        # body of the request should be like this:
        ## node_id: the id of the node that the player wants to move his troops from it

        # check if the node_id is valid
        if node_id not in self.main_game.nodes.keys():
            return {'error': 'node_id is not valid'}

        output_dict = {"reachable": find_reachable(node_id, self.main_game)}

        return output_dict

    def get_state(self, player_id):
        output_dict = {'state': self.main_game.state}
        return output_dict

    def get_strategic_nodes(self):
        output_dict = {'strategic_nodes': [i.id for i in self.main_game.nodes.values() if i.is_strategic],
                       'score': [i.score_of_strategic for i in self.main_game.nodes.values() if i.is_strategic]}
        return output_dict

    def get_troops_count(self, player_id):
        output_dict = {}
        for node in self.main_game.nodes.values():
            output_dict[node.id] = node.number_of_troops
        return output_dict

    def get_turn_number(self):
        output_dict = {'turn_number': self.main_game.turn_number}
        return output_dict

    def index(self):
        # this API used to check if the server is running
        return {"message": "Welcome, server is running"}

    def login(self):
        # make sure there is no more than number_of_players players
        if self.player_id >= self.kernel_config['number_of_players']:
            output_dict = {'error': 'game players is full'}
            raise output_dict['error']

        # create the output dictionary
        output_dict = {'player_id': self.player_id,
                       'message': 'login successful'}

        # initialize the player
        self.main_game.add_player(self.player_id)
        self.main_game.players[self.player_id].number_of_troops_to_place = self.main_game.config['initial_troop']
        self.player_id += 1
        return output_dict

    def move_troop(self, source, destination, troop_count, player_id):
        # this API used to move troops from source to destination

        # the body of the request should be like this
        ## source: the source node id
        ## destination: the destination node id
        ## troop_count: the number of troops to move

        # check if the move troop happened in the current turn
        if self.main_game.move_troop_done:
            return {'error': 'move troop already happened in the current turn'}

        # check if the game is in the turn state
        if self.main_game.game_state != 2:
            return {'error': 'The game is not in the turn state'}

        # check if the game is in the move troop state
        if self.main_game.state != 3:
            return {'error': 'The game is not in the move troop state'}

        # check if the source is valid
        if source not in self.main_game.nodes.keys():
            return {'error': 'source is not valid'}

        # check if the source has a owner
        if self.main_game.nodes[source].owner == None:
            return {'error': 'source does not have any owner'}

        # check if the source is owned by the player
        if self.main_game.nodes[source].owner.id != player_id:
            return {'error': 'source is not owned by the player'}

        # check if the destination is valid
        if destination not in self.main_game.nodes.keys():
            return {'error': 'destination is not valid'}

        # check if the destination has a owner
        if self.main_game.nodes[destination].owner == None:
            return {'error': 'destination does not have any owner'}

        if self.main_game.nodes[destination].owner.id != player_id:
            return {'error': 'destination is not owned by the player'}

        # check if the player has at least 2 troops in the source node
        if self.main_game.nodes[source].number_of_troops <= troop_count:
            return {'error': 'source node does not have enough troops'}

        # check if there is a path between source and destination
        res, path = find_path(source, destination, self.main_game, player_id)
        if not res:
            return {'error': 'there is no path between source and destination'}

        # check if the number of troops is positive
        if troop_count <= 0:
            return {'error': 'troop_count should be positive'}

        # check if the source and destination isn't same
        if source == destination:
            return {'error': 'source and destination should be different'}

        self.main_game.nodes[source].number_of_troops -= troop_count
        self.main_game.nodes[destination].number_of_troops += troop_count

        self.main_game.move_troop_done = True

        self.main_game.log_fortify = {"number_of_troops": troop_count,
                                      "path": path}

        if self.main_game.debug:
            self.main_game.print("player " + str(player_id) + " moved " + str(troop_count) + " troops from node " + str(
                source) + " to node " + str(destination))

        return {'message': 'troops moved successfully'}

    def next_state(self, player_id):
        '''
        This function is used to change the state of the game to the next state
        1: put troop state
        2: attack state
        3: move troop state
        4: fortification state
        '''
        if self.main_game.game_state != 2:
            output_dict = {'error': 'The game is not in the turn state'}
            return output_dict

        if self.main_game.state >= 4:
            output_dict = {'error': 'you already finished the turn'}
            return output_dict

        self.main_game.state += 1
        if self.main_game.debug:
            self.main_game.print("******* state changed to: " + str(self.main_game.state) + " *******")

        output_dict = {'game_state': self.main_game.state, 'message': 'success'}
        return output_dict

    def put_one_troop(self, player_id, node_id):
        # this API is used to put one troop on the map in the initial troop state of the game

        # body of the request should be like this:
        ## node_id: the id of the node that the player wants to put the troop on it

        # check if the player just put one Troop in a init turn
        if self.main_game.state != 1:
            return {'error': 'You can not put more than one troop in a turn'}
        # check if the game is in the initial troop putting state
        if self.main_game.game_state != 1:
            return {'error': 'The game is not in the initial troop putting state'}

        # check if the player has enough troops to put
        if self.main_game.player_turn.number_of_troops_to_place <= 0:
            return {'error': 'You have no more initial troops to put'}

        # get the node_id from the request body
        node_id = node_id

        # check if the node_id is valid
        if node_id not in self.main_game.nodes.keys():
            return {'error': 'node_id is not valid'}

        # check the ownership status of the node
        if self.main_game.nodes[node_id].owner is None:
            # if the node is not owned by any player, add it to the player
            self.main_game.add_node_to_player(node_id, player_id)

        elif self.main_game.nodes[node_id].owner.id != player_id:
            return {'error': 'This node is already owned by another player'}

        # add one troop to the node and subtract one from the player
        self.main_game.nodes[node_id].number_of_troops += 1
        self.main_game.player_turn.number_of_troops_to_place -= 1

        # add the node id and player id to the log variable of the game
        self.main_game.log_initialize.append([player_id, node_id])

        # change the state to 2 so player just can put one troop in a turn
        self.main_game.state = 4
        if self.main_game.debug:
            self.main_game.print(f"player {player_id} put one troop on node {node_id}")

        return {'message': 'troop added successfully'}

    def put_troop(self, player_id, node_id, number_of_troops):
        # this API used to put troops in the map in the put troop state

        # body of the request should be like this:
        ## node_id: the id of the node that the player wants to put the troop on it
        ## number_of_troops: the number of troops that the player wants to put on the node

        # check if the game is in the turn state
        if self.main_game.game_state != 2:
            return {'error': 'The game is not in the turn state'}

        # check if the turn in the put troop state
        if self.main_game.state != 1:
            return {'error': 'The game is not in the troop putting state'}

        # check if the player has enough troops to place
        if self.main_game.player_turn.number_of_troops_to_place < number_of_troops:
            return {'error': 'You do not have enough troops to place'}

        # check if the node is not owned by anyone
        if self.main_game.nodes[node_id].owner is None:
            self.main_game.add_node_to_player(node_id, player_id)

        # check if the node is not owned by another player
        elif self.main_game.nodes[node_id].owner.id != player_id:
            return {'error': 'This node is already owned by another player'}

        # check if the number_of_troops is positive
        if number_of_troops <= 0:
            return {'error': 'number_of_troops should be positive'}

        # add one troop to the node and subtract one from the player
        self.main_game.nodes[node_id].number_of_troops += number_of_troops
        self.main_game.player_turn.number_of_troops_to_place -= number_of_troops

        # add the node id and player id to the log variable of the game
        self.main_game.log_put_troop.append([node_id, number_of_troops])

        if self.main_game.debug:
            self.main_game.print(
                "player " + str(player_id) + " put " + str(number_of_troops) + " troops on node " + str(node_id))

        return {'message': 'troop added successfully'}

    """
    in this API client shows that it's ready to start the game 
    that means it has a server on the port that it said in the login API
    """

    def ready(self, player_id):
        # try:
        self.main_game.players[player_id].is_ready = True
        output_dict = {"message": "every thing is ok, you should wait for other players to be ready"}
        self.main_game.check_all_players_ready()
        return output_dict

        # except:
        output_dict = {"error": "this player_id doesn't exist"}
        return output_dict