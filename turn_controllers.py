# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Edit: Vahid Ghafourian
# Date: 2023/09/06

import json
import datetime
import os


def calculate_score(main_game):
    # (number of nodes * 1000) + (number of troops)+ (3000/score of strategic nodes)
    scores = []
    for i in main_game.players.values():
        number_of_nodes = len(i.nodes)
        number_of_troops = 0
        strategic_score = 0
        for j in i.nodes:
            number_of_troops += j.number_of_troops
            if j.is_strategic:
                strategic_score += 3000 // j.score_of_strategic

        scores.append((number_of_nodes * 1000) + number_of_troops + strategic_score)
    return scores


def check_finish(main_game):
    # find the number of strategic nodes for each player
    players_strategic_nodes_count = []
    for player in main_game.players.values():
        number_of_strategic_nodes = 0
        for node in player.nodes:
            if node.is_strategic:
                number_of_strategic_nodes += 1
        players_strategic_nodes_count.append(number_of_strategic_nodes)

    # check if there is a player with enough strategic nodes to win
    for i in range(len(players_strategic_nodes_count)):
        if players_strategic_nodes_count[i] >= int(main_game.config["number_of_strategic_nodes_to_win"]):
            if main_game.debug:
                main_game.print("player won because of having enough strategic nodes")
            print("Player ", str(i), " won because of having enough strategic nodes.")
            scores = calculate_score(main_game)
            scores[i] += sum(scores)
            game_finished(main_game, scores)
            return True
    # check if the game is finished
    if main_game.turn_number >= int(main_game.config["number_of_turns"]):
        if main_game.debug:
            main_game.print("game finished because of number of turns")
        scores = calculate_score(main_game)
        print("The game ended due to the completion of the number of turns and player", scores.index(max(scores)),
              "won with a score of:", max(scores))
        game_finished(main_game, scores)
        return True
    return False


def game_finished(main_game, score):
    # finish the game
    # make log folder if it does not exist
    if not os.path.exists("log"):
        os.makedirs("log")

    # add score the the log file
    main_game.log["score"] = score

    # generate and save the main_game.log file into a json file in the log folder
    with open("log/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json", "w") as log_file:
        json.dump(main_game.log, log_file)

    # generate and save an export from main_game object and save in the result log folder
    # generate export
    export = dict()
    export['node_owners'] = [i.owner.id if i.owner != None else -1 for i in main_game.nodes.values()]
    export['troop_count'] = [i.number_of_troops for i in main_game.nodes.values()]
    export['turn_number'] = main_game.turn_number
    export['score'] = score
    # add the number of strategic nodes for each player
    for player in main_game.players.values():
        export['player' + str(player.id) + " strategic nodes"] = len([i for i in player.nodes if i.is_strategic])

        # make result_log folder if it does not exist
    if not os.path.exists("result_log"):
        os.makedirs("result_log")

    # save the export in the result log folder
    with open("result_log/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json", "w") as result_log_file:
        json.dump(export, result_log_file)

    print(export)
    # write debug_logs in the text file in the debug_log folder
    if main_game.debug:
        # make debug_log folder if it does not exist
        if not os.path.exists("debug_log"):
            os.makedirs("debug_log")
        with open("debug_log/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt", "w") as debug_log_file:
            debug_log_file.write(main_game.debug_logs)


def change_turn(main_game, c_ai, c_two, c_three):
    while True:
        # increase the turn number and initialize the turn
        player_id = main_game.start_turn()

        # add the turn number to the logs
        if main_game.debug:
            # print("start turn:", main_game.turn_number)
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
                c_ai.turn()
            elif player_id == 1:
                c_two.turn()
            elif player_id == 2:
                c_three.turn()
            else:
                print('wrong id:' + str(player_id))
                input()
        elif main_game.game_state == 1:
            if player_id == 0:
                c_ai.initializer_turn()
            elif player_id == 1:
                c_two.initializer_turn()
            elif player_id == 2:
                c_three.initializer_turn()
            else:
                print('wrong id:' + str(player_id))
                input()
        # end the turn to add the logs for client
        main_game.end_turn()

        if main_game.debug:
            main_game.print("end turn: " + datetime.datetime.now().strftime("%H:%M:%S"))
        # check if the game is finished
        if check_finish(main_game):
            break
