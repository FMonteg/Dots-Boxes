import sys
import math

import datetime
from random import choice, shuffle

possible_lines = [[0,1,2], [3,4,5], [6,7,8],
                  [0,3,6], [1,4,7], [2,5,8],
                  [0,4,8], [2,4,6]]

class Board(object):
    def start(self, size):
        board = {}
        score = 0
        for i in range(size):
            for j in range(size):
                box = chr(ord('A')+i)+str(j+1)
                board[box] = 'LTRB'
        return flatten(board, score, True)

    def current_player(self, state):
        board, score, player = unflatten(state)
        return player

    def find_winning_move(self, state):
        choice = 'NONE'
        board, score, player = unflatten(state)
        for box, sides in board.items():
            if len(sides)==1:
                choice = " ".join([box, sides])
                break
        return choice

    def legal_plays(self, states):
        board, score, player = unflatten(states[-1])
        legal = []
        for box, sides in board.items():
            for s in sides:
                legal.append(' '.join([box, s]))
        return legal
        
    def next_state(self, state, play):
        board, score, player = unflatten(state)
        board = board.copy()
        box, direction = play.split(' ')
        neighbor, symetrical = self.neighbor(box, direction)
        switch = True

        if len(board[box]) == 1:
            score += 1
            switch = False
            del(board[box])
        else:
            board[box] = board[box].replace(direction, '')

        if board.get(neighbor):
            if len(board[neighbor]) == 1:
                score += 1
                switch = False
                del(board[neighbor])
            else:
                board[neighbor] = board[neighbor].replace(symetrical, '')

        if switch:
            score *= (-1)
            player = not player

        return flatten(board, score, player)

    def winner(self, state_history):
        board, score, player = unflatten(state_history[-1])
        if len(board) > 0:
            return 0
        else:
            winner = 1
            if not player:
                score *= (-1)
            if score < 0:
                winner += 1
            return winner


    def neighbor(self, box, direction):
        if direction == 'L':
            return [chr(ord(box[0])-1)+box[1], 'R']
        if direction == 'T':
            return [box[0]+str(int(box[1])+1), 'B']
        if direction == 'R':
            return [chr(ord(box[0])+1)+box[1], 'L']
        if direction == 'B':
            return [box[0]+str(int(box[1])-1), 'T']








class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        self.board = board
        self.states = kwargs.get('states',[])

        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)

        self.max_moves = kwargs.get('max_moves', 10)

        self.wins = {}
        self.plays = {}

        self.C = kwargs.get('C', 1.4)
        pass

    def set_calculation_time(self, seconds):
        self.calculation_time = datetime.timedelta(seconds=seconds)
        pass

    def update (self, play):
        self.states.append(self.board.next_state(self.states[-1], play))
        pass
    
    def get_play(self):
        self.max_depth = 0
        state = self.states[-1]
        player = True
        legal = self.board.legal_plays(self.states[:])
        winning = self.board.find_winning_move(state)

        if not legal:
            return
        if len(legal) == 1:
            return legal[0]
        if winning != 'NONE':
            return winning

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow()-begin < self.calculation_time:
            self.run_simulation()
            games += 1
        
            
        moves_states = [(p, self.board.next_state(state, p)) for p in legal]

        max_percent = max((self.wins.get((player, S), 0)/self.plays.get((player, S), 1)) for p, S in moves_states)
        move = choice([p for p, S in moves_states if (self.wins.get((player, S), 0)/self.plays.get((player, S), 1)) == max_percent])


        return move 

    def run_simulation(self):
        plays, wins = self.plays, self.wins
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = True

        expand = True
        for t in range(1, self.max_moves+1):
            legal = self.board.legal_plays(states_copy)
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]

            if all(plays.get((player, S)) for p, S in moves_states):
                log_total = math.log(sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(((wins[(player, S)]/plays[(player, S)])+self.C*math.sqrt(log_total/plays[(player, S)]),p,S) for p,S in moves_states)
            else:
                move, state = choice(moves_states)
            states_copy.append(state)

            if expand and (player, state) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins[(player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t
            visited_states.add((player, state))
            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)
            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in plays:
                continue
            plays[(player, state)] += 1
            if player == winner:
                wins[(player, state)] +=1
        pass

    def force_update(self, board, score):
        state = flatten(board, score, True)
        self.states.append(state)
        pass




    



def flatten(board, score, player):
    flat = []
    for box, sides in board.items():
        flat += [box, sides]
    flat += [score, player]
    return tuple(flat)

def unflatten(flat):
    N = len(flat)//2
    board = {}
    for i in range(N-1):
        board[flat[2*i]] = flat[2*i+1]
    score = flat[-2]
    player = flat[-1]
    return board, score, player






###########################################################
#                        Old code                       #
###########################################################




#Play for 0 or 1 sided boxes, without creating 3-side
def find_value_play(board):
    choice = 'NONE'
    counter = 0
    profondeur_calcul = 3
    found_edge = False
    found_four_side = False

    for key,item in board.items():
        if len(item)>2:
            for i in range(len(item)):
                play = " ".join([key, item[i]])
            #Check if such play won't create a 3 sided box
                valid, temp_bord = is_okay(play, board)
                if valid:
                    if temp_bord:
                        choice = play
                        found_edge = True
                    elif not found_edge and len(item) == 4:
                        choice = play
                        found_four_side = True
                    else:
                        counter += 1
                        if counter > profondeur_calcul:
                            if not found_edge and not found_four_side:
                                choice = play

    return choice


#Find loops and connections
def identify_loops(board):
    graph = {}
    loops = {}
    counter = 0
    done = []
    for key,item in board.items():
        if key not in done and len(item)>2:
            done.append(key)
            for i in range(len(item)):
                temp, trash = neighboring_box(key, item[i])
                while_loop = True
                if temp not in board.keys():
                                while_loop = False
                if temp not in done:
                    counter += 1
                    length = 1 
                    while while_loop:
                        length +=1
                        if temp in done:
                            while_loop = False
                        elif len(board[temp]) > 2:
                            while_loop = False
                        else:
                            done.append(temp)
                            temp, trash = neighboring_box(temp, anti(board[temp],trash))
                            if temp not in board.keys():
                                while_loop = False

                    graph[counter] = [length, (key, item[i]), (temp, trash)]

    counter = 0
    for key,item in board.items():
        if key not in done:
            done.append(key)
            for i in range(len(item)):
                temp, trash = neighboring_box(key, item[i])
                if temp not in done:
                    counter += 1
                    length = 1
                    while len(board[temp])==2 and temp not in done:
                        done.append(temp)
                        temp, trash = neighboring_box(temp, anti(board[temp],trash)) 
                        length +=1
                    loops[counter] = [length, (key, item[i]), (temp, trash)]

    return simplify(graph, loops)

    

#Find play in endgame
def simplify(graph, loops):
    plays = {}

    for key,item in graph.items():
        if item[1][0] in plays.keys():
            plays[item[1][0]].append((item[1][1], item[2][0], item[0]))
        else:
            plays[item[1][0]] = [(item[1][1], item[2][0], item[0])]

    for key,item in loops.items():
        plays[item[1][0]] = [(item[1][1], item[2][0], item[0])]

    return plays




def minimax(plays):

    if plays == {}:
        return 'NONE', 'NONE'
    else:
        best = -1000000
        choice = 'NONE'
        for key,item in plays.items():
            for i in range(len(item)):

                temp_plays = plays.copy()
                if len(item) == 1:
                    del temp_plays[key]
                    score = -1*item[0][2]
                elif len(item) == 2:
                    if item[i][1] == key:
                        del temp_plays[key]
                        score = -1*(item[0][2]+item[1][2])
                        cible = item[1-i][1]
                    else:
                        del temp_plays[key][i]
                        score = -1*item[i][2]
                        cible = item[i][1]
                elif len(item) == 3:
                    del temp_plays[key][i]
                    score = -1*item[i][2]
                    cible = item[i][1]
                
                if len(item) > 1:
                    N = len(plays[cible])
                    for j in range(N):
                        if plays[cible][j][1] == key:
                            del temp_plays[cible][j]
                        if N == 3:
                            new_length = temp_plays[cible][0][2] + temp_plays[cible][1][2]
                            index = [0,0]
                            targets = [0,0]
                            for k in range(2):
                                targets[k] = temp_plays[cible][k][1]
                                for l in range(len(temp_plays[targets[k]])):
                                    if temp_plays[targets[k]][l][1] == cible:
                                        index[k] = l
                            for k in range(2):
                                temp_plays[targets[k]].append((plays[targets[k]][index[k]][0], targets[1-k], new_length))
                                del temp_plays[targets[k]][index[k]]
                
                temp_score, temp_action = minimax(temp_plays)
                if choice == 'NONE':
                    choice = " ".join([key, item[i][0]])
                if temp_score != 'NONE':
                    if score - temp_score > best:
                        best = score - temp_score
                        choice = " ".join([key, item[i][0]])
        return score, choice



def anti(directions, unwanted):
    if directions[0]==unwanted:
        return directions[1]
    else:
        return directions[0]

def is_okay(play, board):
    result = True
    bord = True
    box, direction = play.split()
    neighbor = neighboring_box(box, direction)[0]
    if neighbor in board.keys():
        bord = False
        if len(board[neighbor]) <= 2:
            result = False
    return result, bord




###########################################################
#               Inputs and main loop                      #
###########################################################


board_size = int(input())  # The size of the board.
player_id = input()  # The ID of the player. 'A'=first player, 'B'=second player.

board = Board()
MC = MonteCarlo(board, states=[board.start(board_size)], time = 0.8)
first_turn = True

# game loop
while True:
    # player_score: The player's score.
    # opponent_score: The opponent's score.
    player_score, opponent_score = [int(i) for i in input().split()]
    num_boxes = int(input())  # The number of playable boxes.
    playable = {}
    for i in range(num_boxes):
        # box: The ID of the playable box.
        # sides: Playable sides of the box.
        box, sides = input().split()
        playable[box] = sides

    if not first_turn:
        MC.set_calculation_time(0.07)
        MC.force_update(playable, player_score - opponent_score)

    play = MC.get_play()
    print(play)
    MC.update(play)
    first_turn = False





