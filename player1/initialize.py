from src.components.client_game import ClientGame

def initializer(game: ClientGame):
    output = game.blueprints.login(game.main_game)
    print(game.blueprints.ready(game.main_game, output['player_id']))