# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to manage the turns of the game
# it will be called after all the players requested for ready


import time
from src.turn_controllers.check_finish import check_finish
import datetime


def change_turn(main_game, client_game):
    while True:
        # increase the turn number and initialize the turn
        player_id = main_game.start_turn()

        # add the turn number to the logs 
        if main_game.debug:
            main_game.print("----------------------------- start turn: " + str(
                main_game.turn_number) + "----------------------------")
            main_game.print(
                "player: " + str(player_id) + ' -- start time ' + datetime.datetime.now().strftime("%H:%M:%S"))
            # print the owner and number of troops of each node at the beginning of the turn
            for i in main_game.nodes.values():
                main_game.print(
                    f"node {i.id}: owner: {i.owner.id if i.owner is not None else -1}, number of troops: {i.number_of_troops} , number of fort troops: {i.number_of_fort_troops}")

        # show number of troops that the player did not put on the map
        if main_game.debug:
            main_game.print(
                f"player {player_id} has {main_game.player_turn.number_of_troops_to_place} troops to put on the map")

        print("Turn Number:", main_game.turn_number, ' =' * 20)
        # wait for the player to play
        if main_game.game_state == 2:
            try:
                main_game.players[player_id].turn(client_game)
            except Exception as e:
                raise Exception('Wrong player id:' + str(player_id))
        elif main_game.game_state == 1:
            try:
                main_game.players[player_id].initializer(client_game)
            except Exception as e:
                raise Exception('Wrong player id:' + str(player_id))

        # end the turn to add the logs for client
        main_game.end_turn()

        if main_game.debug:
            main_game.print("end turn: " + datetime.datetime.now().strftime("%H:%M:%S"))
        # check if the game is finished
        if check_finish(main_game):
            break
