def fort(node_id: int, troop_count: int, main_game, player_id):
    # this API used to apply the fortification ability of the player

    # the body of the request should be like this
    ## node_id : the id of the node that will be fortified
    ## troop_count : the number of troops that will be fortified

    # check if the ClientGame is in the turn state
    if main_game.game_state != 2:
        return {'error': 'The game is not in the turn state'}

    # check if the turn is in the fort state
    if main_game.state != 4:
        return {'error': 'The game is not in the fort state'}

    # check if the node_id is valid
    if node_id not in main_game.nodes.keys():
        return {'error': 'node_id is not valid'}

    # check the ownership status of the node
    # check if the node has an owner
    if main_game.nodes[node_id].owner is None:
        return {'error': 'This node has no owner'}

    # check if the node is owned by the player
    if main_game.nodes[node_id].owner.id != player_id:
        return {'error': 'This node is already owned by another player'}

    # check if the troop_count is valid
    if troop_count >= main_game.nodes[node_id].number_of_troops:
        return {'error': 'there is not enough troops in the node'}

    # check if the player hasn't used the fortification ability in the game
    if main_game.player_turn.use_fort:
        return {'error': 'you have already used the fortification ability in the game'}

    # start the fortification ability
    main_game.player_turn.use_fort = True

    # fortify the node
    main_game.nodes[node_id].number_of_troops -= troop_count
    main_game.nodes[node_id].number_of_fort_troops += main_game.config['fort_coef'] * troop_count

    if main_game.debug:
        main_game.print(f"player {player_id} fortified node {node_id} with {troop_count} troops")

    return {'success': 'the fortification ability is applied successfully'}
