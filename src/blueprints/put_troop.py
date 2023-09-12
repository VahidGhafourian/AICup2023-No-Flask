def put_troop(node_id: int, number_of_troops: int, main_game, player_id):
    # this API used to put troops in the map in the put troop state

    # body of the request should be like this:
    ## node_id: the id of the node that the player wants to put the troop on it
    ## number_of_troops: the number of troops that the player wants to put on the node

    # check if the game is in the turn state
    if main_game.game_state != 2:
        return {'error': 'The game is not in the turn state'}

    # check if the turn in the put troop state
    if main_game.state != 1:
        return {'error': 'The game is not in the troop putting state'}

    # check if the node_id is valid
    if node_id not in main_game.nodes.keys():
        return {'error': 'node_id is not valid'}

    # check if the player has enough troops to place
    if main_game.player_turn.number_of_troops_to_place < number_of_troops:
        return {'error': 'You do not have enough troops to place'}

    # check if the node is not owned by anyone
    if main_game.nodes[node_id].owner is None:
        main_game.add_node_to_player(node_id, player_id)

    # check if the node is not owned by another player
    elif main_game.nodes[node_id].owner.id != player_id:
        return {'error': 'This node is already owned by another player'}

    # check if the number_of_troops is positive
    if number_of_troops <= 0:
        return {'error': 'number_of_troops should be positive'}

    # add one troop to the node and subtract one from the player
    main_game.nodes[node_id].number_of_troops += number_of_troops
    main_game.player_turn.number_of_troops_to_place -= number_of_troops

    # add the node id and player id to the log variable of the game
    main_game.log_put_troop.append([node_id, number_of_troops])

    if main_game.debug:
        main_game.print(
            "player " + str(player_id) + " put " + str(number_of_troops) + " troops on node " + str(node_id))

    return {'message': 'troop added successfully'}
