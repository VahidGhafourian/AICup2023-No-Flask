# import blueprints
from src.blueprints.index import index
from src.blueprints.login import login
from src.blueprints.ready import ready
from src.blueprints.get_owners import get_owners
from src.blueprints.get_troops_count import get_troops_count
from src.blueprints.get_state import get_state
from src.blueprints.get_turn_number import get_turn_number
from src.blueprints.get_adj import get_adj
from src.blueprints.next_state import next_state
from src.blueprints.put_one_troop import put_one_troop
from src.blueprints.put_troop import put_troop
from src.blueprints.get_player_id import get_player_id
from src.blueprints.attack import attack
from src.blueprints.move_troop import move_troop
from src.blueprints.get_strategic_nodes import get_strategic_nodes
from src.blueprints.get_number_of_troops_to_put import get_number_of_troops_to_put
from src.blueprints.get_reachable import get_reachable
from src.blueprints.get_number_of_fort_troops import get_number_of_fort_troops
from src.blueprints.fort import fort


class BluePrints:
    def __init__(self):
        self.index = index
        self.login = login
        self.ready = ready
        self.get_owners = get_owners
        self.get_troops_count = get_troops_count
        self.get_state = get_state
        self.get_turn_number = get_turn_number
        self.get_adj = get_adj
        self.next_state = next_state
        self.put_one_troop = put_one_troop
        self.put_troop = put_troop
        self.get_player_id = get_player_id
        self.attack = attack
        self.move_troop = move_troop
        self.get_strategic_nodes = get_strategic_nodes
        self.get_number_of_troops_to_put = get_number_of_troops_to_put
        self.get_reachable = get_reachable
        self.get_number_of_fort_troops = get_number_of_fort_troops
        self.fort = fort
