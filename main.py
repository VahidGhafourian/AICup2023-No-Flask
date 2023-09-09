# author: Vahid Ghafourian
# Date: 2023/09/06

from Kernel import Kernel
from components.game import Game
from clients.client_ai import Client_AI
from clients.client_enemy_one import Client_Enemy_One
from clients.client_enemy_two import Client_Enemy_Two
from turn_controllers import change_turn
import os

import json

def read_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def main():
    # read map file
    kernel_main_game = Game()
    # ask player to choose map from the list of maps
    maps = os.listdir('maps')

    ## get the selected map from the player
    selected_map = '3'

    while selected_map.isdigit() == False or int(selected_map) >= len(maps) or int(selected_map) < 0:
        ## show the list of maps from the maps folder
        print("Choose a map from the list of maps:")
        for i, map in enumerate(maps):
            print(i,'-', map)
        selected_map = input("Enter the number of the map you want to choose: ")

    ## read the selected map
    kernel_main_game.read_map('maps/'+maps[int(selected_map)])

    # read config
    kernel_config = read_config()

    # Build Kernel
    kernel = Kernel(kernel_main_game, kernel_config)

    # Build AI Client
    c_ai = Client_AI(kernel)

    # Build Enemy clients
    c_two = Client_Enemy_One(kernel)
    c_three = Client_Enemy_Two(kernel)

    change_turn(kernel.main_game, c_ai, c_two, c_three)

if __name__ == '__main__':
    main()


