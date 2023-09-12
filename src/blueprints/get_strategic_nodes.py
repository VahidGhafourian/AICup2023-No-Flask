def get_strategic_nodes(main_game):
    output_dict = {'strategic_nodes': [i.id for i in main_game.nodes.values() if i.is_strategic],
                   'score': [i.score_of_strategic for i in main_game.nodes.values() if i.is_strategic]}
    return output_dict
