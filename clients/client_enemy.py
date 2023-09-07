# author: Vahid Ghafourian
# Date: 2023/09/06

from clients.game_client import Game_Client
import random


class Client_Enemy():
    def __init__(self, kernel) -> None:
        self.flag = False
        self.kernel = kernel
        self.game = self.join_kernel()
        print(self.kernel.ready(self.game.get_player_id()))

    def join_kernel(self):
        login_response = self.kernel.login()
        id = login_response['player_id']
        # generate game object
        game = Game_Client(self.kernel, id)
        return game

    def initializer_turn(self):
        strategic_nodes = self.game.get_strategic_nodes()['strategic_nodes']
        score = self.game.get_strategic_nodes()['score']
        strategic_nodes = list(zip(strategic_nodes, score))
        strategic_nodes.sort(key=lambda x: x[1], reverse=True)
        strategic_nodes, score = list(zip(*strategic_nodes))

        owner = self.game.get_owners()
        for i in strategic_nodes:
            if owner[i] == -1:
                print(self.game.put_one_troop(i), "-- putting one troop on", i)
                return
        adj = self.game.get_adj()
        for i in strategic_nodes:
            for j in adj[i]:
                if owner[j] == -1:
                    print(self.game.put_one_troop(j), "-- putting one troop on neighbor of strategic node", j)
                    return
        my_id = self.game.get_player_id()
        nodes = []
        nodes.extend([i for i in strategic_nodes if owner[i] == my_id])
        for i in strategic_nodes:
            for j in adj[i]:
                if owner[j] == my_id:
                    nodes.append(j)
        nodes = list(set(nodes))
        node = random.choice(nodes)
        self.game.put_one_troop(node)
        print("3-  putting one troop on", node)

    def turn(self):
        print(self.game.get_number_of_troops_to_put())
        owner = self.game.get_owners()
        for i in owner.keys():
            if owner[i] == -1 and self.game.get_number_of_troops_to_put()['number_of_troops'] > 1:
                print(self.game.put_troop(i, 1))

        list_of_my_nodes = []
        for i in owner.keys():
            if owner[i] == self.game.get_player_id():
                list_of_my_nodes.append(i)

        with open('log.txt', 'at') as logfile:
            logfile.write(str(random.choice(list_of_my_nodes)))

        print(self.game.put_troop(random.choice(list_of_my_nodes),
                                  self.game.get_number_of_troops_to_put()['number_of_troops']))
        print(self.game.get_number_of_troops_to_put())

        print(self.game.next_state())

        # find the node with the most troops that I own
        max_troops = 0
        max_node = -1
        owner = self.game.get_owners()
        for i in owner.keys():
            if owner[i] == self.game.get_player_id():
                if self.game.get_number_of_troops()[i] > max_troops:
                    max_troops = self.game.get_number_of_troops()[i]
                    max_node = i
        # find a neighbor of that node that I don't own
        adj = self.game.get_adj()
        for i in adj[max_node]:
            if owner[i] != self.game.get_player_id() and owner[i] != -1:
                print(self.game.attack(max_node, i, 1, 0.5))
                break
        print(self.game.next_state())
        print(self.game.get_state())
        # get the node with the most troops that I own
        max_troops = 0
        max_node = -1
        owner = self.game.get_owners()
        for i in owner.keys():
            if owner[i] == self.game.get_player_id():
                if self.game.get_number_of_troops()[i] > max_troops:
                    max_troops = self.game.get_number_of_troops()[i]
                    max_node = i
        print(self.game.get_reachable(max_node))
        destination = random.choice(self.game.get_reachable(max_node)['reachable'])
        print(self.game.move_troop(max_node, destination, 1))
        print(self.game.next_state())

        if self.flag == False:
            max_troops = 0
            max_node = -1
            owner = self.game.get_owners()
            for i in owner.keys():
                if owner[i] == self.game.get_player_id():
                    if self.game.get_number_of_troops()[i] > max_troops:
                        max_troops = self.game.get_number_of_troops()[i]
                        max_node = i

            print('Max Number of node in best planet', self.game.get_number_of_troops()[max_node])
            print(self.game.fort(max_node, 3))
            print(self.game.get_number_of_fort_troops())
            self.flag = True