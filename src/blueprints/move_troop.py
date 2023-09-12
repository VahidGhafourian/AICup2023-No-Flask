from src.tools.find_path import find_path


def move_troop(source: int, destination: int, troop_count: int, main_game, player_id):
    # this API used to move troops from source to destination

    # the body of the request should be like this
    ## source: the source node id
    ## destination: the destination node id
    ## troop_count: the number of troops to move

    # check if the move troop happened in the current turn
    if main_game.move_troop_done:
        return {'error': 'move troop already happened in the current turn'}

    # check if the game is in the turn state
    if main_game.game_state != 2:
        return {'error': 'The game is not in the turn state'}

    # check if the game is in the move troop state
    if main_game.state != 3:
        return {'error': 'The game is not in the move troop state'}

    # check if the source is valid
    if source not in main_game.nodes.keys():
        return {'error': 'source is not valid'}

    # check if the source has a owner
    if main_game.nodes[source].owner == None:
        return {'error': 'source does not have any owner'}

    # check if the source is owned by the player
    if main_game.nodes[source].owner.id != player_id:
        return {'error': 'source is not owned by the player'}

    # check if the destination is valid
    if destination not in main_game.nodes.keys():
        return {'error': 'destination is not valid'}

    # check if the destination has a owner
    if main_game.nodes[destination].owner == None:
        return {'error': 'destination does not have any owner'}

    if main_game.nodes[destination].owner.id != player_id:
        return {'error': 'destination is not owned by the player'}

    # check if the player has at least 2 troops in the source node
    if main_game.nodes[source].number_of_troops <= troop_count:
        return {'error': 'source node does not have enough troops'}

    # check if there is a path between source and destination
    res, path = find_path(source, destination, main_game, player_id)
    if not res:
        return {'error': 'there is no path between source and destination'}

    # check if the number of troops is positive
    if troop_count <= 0:
        return {'error': 'troop_count should be positive'}

    # check if the source and destination isn't same
    if source == destination:
        return {'error': 'source and destination should be different'}

    main_game.nodes[source].number_of_troops -= troop_count
    main_game.nodes[destination].number_of_troops += troop_count

    main_game.move_troop_done = True

    main_game.log_fortify = {"number_of_troops": troop_count,
                             "path": path}

    if main_game.debug:
        main_game.print("player " + str(player_id) + " moved " + str(troop_count) + " troops from node " + str(
            source) + " to node " + str(destination))

    return {'message': 'troops moved successfully'}
