# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to manage the turns of the game
# it will be called after all the players requested for ready


import time
from src.turn_controllers.check_finish import check_finish
import datetime
from player0.main import initializer as initializer_p0
from player0.main import turn as turn_p0
from player1.main import initializer as initializer_p1
from player1.main import turn as turn_p1
from player2.main import initializer as initializer_p2
from player2.main import turn as turn_p2


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
            if player_id == 0:
                turn_p0(client_game)
            elif player_id == 1:
                turn_p1(client_game)
            elif player_id == 2:
                turn_p2(client_game)
            else:
                print('wrong id:' + str(player_id))
            # time.sleep(main_game.config["turn_time"])
        elif main_game.game_state == 1:
            if player_id == 0:
                initializer_p0(client_game)
            elif player_id == 1:
                initializer_p1(client_game)
            elif player_id == 2:
                initializer_p2(client_game)
            else:
                print('wrong id:' + str(player_id))
            # time.sleep(main_game.config["init_time"])
        # end the turn to add the logs for client
        main_game.end_turn()

        if main_game.debug:
            main_game.print("end turn: " + datetime.datetime.now().strftime("%H:%M:%S"))
        # check if the game is finished
        if check_finish(main_game):
            break
