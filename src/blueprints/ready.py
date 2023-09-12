"""
in this API client shows that it's ready to start the game 
that means it has a server on the port that it said in the login API
"""


def ready(main_game, player_id):
    main_game.players[player_id].is_ready = True
    output_dict = {"message": "every thing is ok, you should wait for other players to be ready"}
    main_game.check_all_players_ready()
    return output_dict
