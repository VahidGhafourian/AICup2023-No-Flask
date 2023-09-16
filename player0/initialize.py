from src.components.client_game import ClientGame

def initializer(game: ClientGame, name, initialize, turn):
    output = game.blueprints.login(game.main_game, name, initialize, turn)
    if 'error' in output:
        raise Exception("error: " + output['error'])
    print(game.blueprints.ready(game.main_game, output['player_id']))