# author: Mohamad Mahdi Reisi 
# Date: 2023/8/16

# Description: This file defines a blueprint for the login API 
# each player should send a request to this API to get a token and player_id 
# it also gets a port number to run a server
# player also should send a token/password to this API so server is going to use it to authenticate that the request comes from server 

# initialize the player_id
player_id = 0


def login(main_game):
    global player_id
    # make sure there is no more than number_of_players players
    if player_id >= main_game.config['number_of_players']:
        output_dict = {'error': 'game players is full'}
        return output_dict

    # create the output dictionary
    output_dict = {'player_id': player_id,
                   'message': 'login successful'}

    # initialize the player
    main_game.add_player(player_id)
    main_game.players[player_id].number_of_troops_to_place = main_game.config['initial_troop']
    player_id += 1
    return output_dict
