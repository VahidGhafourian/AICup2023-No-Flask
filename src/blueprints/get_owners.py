def get_owners(main_game):
    output_dict = {}
    for node in main_game.nodes.values():
        if node.owner != None:
            output_dict[str(node.id)] = node.owner.id
        else:
            output_dict[str(node.id)] = -1
    return output_dict
