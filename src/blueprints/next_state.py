def next_state(main_game):
    ''' 
    This function is used to change the state of the game to the next state 
    1: put troop state
    2: attack state
    3: move troop state
    4: fortification state
    '''
    if main_game.game_state != 2:
        output_dict = {'error': 'The game is not in the turn state'}
        return output_dict

    if main_game.state >= 4:
        output_dict = {'error': 'you already finished the turn'}
        return output_dict

    main_game.state += 1
    if main_game.debug:
        main_game.print("******* state changed to: " + str(main_game.state) + " *******")

    output_dict = {'game_state': main_game.state, 'message': 'success'}
    return output_dict
