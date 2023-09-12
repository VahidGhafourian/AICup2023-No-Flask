from src.tools.find_reachable import find_reachable


def get_reachable(node_id: int, main_game):
    # this API used to find all the nodes that the owner can move it's troops from node_id to them    
    # body of the request should be like this:
    ## node_id: the id of the node that the player wants to move his troops from it

    # check if the node_id is valid
    if node_id not in main_game.nodes.keys():
        return {'error': 'node_id is not valid'}

    output_dict = {"reachable": find_reachable(node_id, main_game)}

    return output_dict
