import random
from src.components.client_game import ClientGame

flag = False


def initializer(game: ClientGame):
    print(game.get_player_id())
    strategic_nodes = game.get_strategic_nodes()['strategic_nodes']
    score = game.get_strategic_nodes()['score']
    strategic_nodes = list(zip(strategic_nodes, score))
    strategic_nodes.sort(key=lambda x: x[1], reverse=True)
    strategic_nodes, score = list(zip(*strategic_nodes))
    print(game.get_turn_number())

    owner = game.get_owners()
    for i in strategic_nodes:
        if owner[str(i)] == -1:
            print(game.put_one_troop(i), "-- putting one troop on", i)
            return
    adj = game.get_adj()
    for i in strategic_nodes:
        for j in adj[str(i)]:
            if owner[str(j)] == -1:
                print(game.put_one_troop(j), "-- putting one troop on neighbor of strategic node", j)
                return
    my_id = game.get_player_id()['player_id']
    nodes = []
    nodes.extend([i for i in strategic_nodes if owner[str(i)] == my_id])
    for i in strategic_nodes:
        for j in adj[str(i)]:
            if owner[str(j)] == my_id:
                nodes.append(j)
    nodes = list(set(nodes))
    node = random.choice(nodes)
    game.put_one_troop(node)
    print("3-  putting one troop on", node)
    


def turn(game: ClientGame):
    global flag
    print(game.get_number_of_troops_to_put())
    owner = game.get_owners()
    for i in owner.keys():
        if owner[str(i)] == -1 and game.get_number_of_troops_to_put()['number_of_troops'] > 1:
            print(game.put_troop(int(i), 1))

    list_of_my_nodes = []
    for i in owner.keys():
        if owner[str(i)] == game.get_player_id()['player_id']:
            list_of_my_nodes.append(i)

    print(game.put_troop(random.choice(list_of_my_nodes), game.get_number_of_troops_to_put()['number_of_troops']))
    print(game.get_number_of_troops_to_put())

    print(game.next_state())

    # find the node with the most troops that I own
    max_troops = 0
    max_node = -1
    owner = game.get_owners()
    for i in owner.keys():
        if owner[str(i)] == game.get_player_id()['player_id']:
            if game.get_number_of_troops()[i] > max_troops:
                max_troops = game.get_number_of_troops()[i]
                max_node = i
    # find a neighbor of that node that I don't own
    adj = game.get_adj()
    for i in adj[max_node]:
        if owner[str(i)] != game.get_player_id()['player_id'] and owner[str(i)] != -1:
            print(game.attack(int(max_node), int(i), 1, 0.5))
            break
    
    print(game.next_state())
    print(game.get_state())
    # get the node with the most troops that I own
    max_troops = 0
    max_node = -1
    owner = game.get_owners()
    for i in owner.keys():
        if owner[str(i)] == game.get_player_id()['player_id']:
            if game.get_number_of_troops()[i] > max_troops:
                max_troops = game.get_number_of_troops()[i]
                max_node = i
    print(game.get_reachable(int(max_node)))
    x = game.get_reachable(int(max_node))['reachable']
    x.remove(int(max_node))
    if len(x) > 0:
        destination = random.choice(x)
        print(game.move_troop(int(max_node), int(destination), 1))
    
    print(game.next_state())

    if flag == False:
        max_troops = 0
        max_node = -1
        owner = game.get_owners()
        for i in owner.keys():
            if owner[str(i)] == game.get_player_id()['player_id']:
                if game.get_number_of_troops()[i] > max_troops:
                    max_troops = game.get_number_of_troops()[i]
                    max_node = i

        print(game.get_number_of_troops()[max_node])
        print(game.fort(int(max_node), 3))
        print(game.get_number_of_fort_troops())
        flag = True
    
