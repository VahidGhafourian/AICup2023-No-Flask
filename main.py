# author: Vahid Ghafourian
# Date: 2023/09/06

from src.components.game import Game
from src.tools.read_config import read_config
from src.turn_controllers.change_turn import change_turn
import os
import argparse
from src.components.client_game import ClientGame
from src.blueprints.login import reset_global_player_id


def start_p0(client_game, name="<name of player one>"):
    from player0.initialize import initializer as initializer_p0
    from player0.main import initializer, turn
    initializer_p0(client_game, name, initializer, turn)


def start_p1(client_game, name="<name of player two>"):
    from player1.initialize import initializer as initializer_p1
    from player1.main import initializer, turn
    initializer_p1(client_game, name, initializer, turn)


def start_p2(client_game, name="<name of player three>"):
    from player2.initialize import initializer as initializer_p2
    from player2.main import initializer, turn
    initializer_p2(client_game, name, initializer, turn)


def main(selected_map):
    # define argument parser
    parser = argparse.ArgumentParser(description='choose map to play on')
    parser.add_argument('-m', '--map', type=str, help='choose map to play on')
    args = parser.parse_args()

    # read map file
    main_game = Game()
    # ask player to choose map from the list of maps
    maps = os.listdir('maps')

    ## get the selected map from the player
    selected_map = str(maps.index(args.map)) if args.map != None else str(selected_map)

    while selected_map.isdigit() == False or int(selected_map) >= len(maps) or int(selected_map) < 0:
        ## show the list of maps from the maps folder
        print("Choose a map from the list of maps:")
        for i, map in enumerate(maps):
            print(i, '-', map)
        selected_map = input("Enter the number of the map you want to choose: ")

    ## read the selected map
    main_game.read_map('maps/' + maps[int(selected_map)])

    # read config
    main_game.config = read_config()

    # set the debug variable to True or False to see the debug messages and generate debug logs
    main_game.debug = main_game.config['debug']

    # Build Clients
    client_game = ClientGame(main_game)

    # you can change order of start players for change order on playing
    start_p0(client_game)
    start_p1(client_game)
    start_p2(client_game)

    # Run the server
    if main_game.game_started:
        change_turn(main_game, client_game)

    reset_global_player_id()
    del main_game, client_game


if __name__ == '__main__':
    main(None)
