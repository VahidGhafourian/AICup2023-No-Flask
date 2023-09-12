def get_adj(main_game):
    # this API used to the list of the adjacent nodes of each node
    output_dict = {}
    for node in main_game.nodes.values():
        output_dict[str(node.id)] = [i.id for i in node.adj_main_map]
    return output_dict
