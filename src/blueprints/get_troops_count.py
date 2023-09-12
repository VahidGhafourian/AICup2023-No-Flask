def get_troops_count(main_game):
    output_dict = {}
    for node in main_game.nodes.values():
        output_dict[str(node.id)] = node.number_of_troops
    return output_dict
