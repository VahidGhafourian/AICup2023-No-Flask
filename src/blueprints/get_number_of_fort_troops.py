def get_number_of_fort_troops(main_game):
    # this API used to get the number of fort troops on each node
    output_dict = {}
    for node in main_game.nodes.values():
        output_dict[str(node.id)] = node.number_of_fort_troops
    return output_dict
