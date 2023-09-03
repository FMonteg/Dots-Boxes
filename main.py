###########################################################
#               Imports and definitions                   #
###########################################################

import sys
import math


class DotsBoxesBoard(object):
    def __init__(self, size, player):
        self.size = size
        self.limit = self.size**2
        
        self.edges = []
        
        self.scores = [0,0]
        self.current_player = player

        #Up, Left, Right, Down, and so on
        for i in range(self.size):
            for j in range(self.size):
                if i==0:
                    self.edges.append(self.limit)
                else:
                    self.edges.append((i-1)*self.size+(j))

                if j==0:
                    self.edges.append(self.limit)
                else:
                    self.edges.append((i)*self.size+(j-1))
                
                if j==self.size-1:
                    self.edges.append(self.limit)
                else:
                    self.edges.append((i)*self.size+(j+1))

                if i==self.size-1:
                    self.edges.append(self.limit)
                else:
                    self.edges.append((i+1)*self.size+(j))
        #Board's edge
        self.edges.append(-1)
        self.edges.append(-1)
        self.edges.append(-1)
        self.edges.append(-1)

        pass

    def update_move(self, move):
        move = self.convert_move_in(move)
        neighbour = self.edges[move]
        self.edges[move] = -1

        if neighbour>-1:
            self.edges[4*neighbour + 3 - move%4] = -1
        
        self.update_score_and_player(move//4, neighbour)   

        pass

    def update_score_and_player(self, box_1, box_2):
        switch = True
        if box_1 < self.limit:
            if self.counting_edges(box_1) == 0:
                self.scores[self.current_player] += 1
                switch = False
        if box_2 < self.limit:
            if self.counting_edges(box_2) == 0:
                self.scores[self.current_player] += 1
                switch = False 
        if switch:
            self.current_player = 1 - self.current_player
        pass
        
    def is_double_crossing(self, move):
        box_1 = move//4
        box_2 = self.edges[move]
        if box_1 < self.limit and box_2 < self.limit:
            if self.counting_edges(box_1)==1 and self.counting_edges(box_2)==1:
                return True
        return False
    
    def is_boundary_crossing(self, move):
        box_1 = move//4
        box_2 = self.edges[move]
        if box_1 < self.limit and box_2 == self.limit:
            if self.counting_edges(box_1)==1:
                return True
        return False

    def is_in_loop(self, move):
        starting_box = move//4
        if self.counting_edges(starting_box)==2:
            box = starting_box
            direction = move%4
            
            while True:
                #print('checking loop starting from {}, we are in {} {}'.format(starting_box, box, direction))
                box  = self.edges[4*box + direction]
                if self.counting_edges(box)!=2:
                    return False
                elif box == starting_box:
                    return True
                else:
                    direction = self.other_direction(box, 3-direction)
        return False

    def other_direction(self, box, direction):
        for i in range(4):
            if self.edges[4*box+i]>-1 and i != direction:
                return i
        print('Redirection error')
        pass
    
    def is_in_chain(self, move):
        starting_box = move//4
        if self.counting_edges(starting_box)==2:
            box = starting_box
            direction = move%4
            while True:
                #print('checking first part chain starting from {}, we are in {} {}'.format(starting_box, box, direction))
                box  = self.edges[4*box + direction]
                if box == self.limit:
                    break
                elif self.counting_edges(box)!=2:
                    return False
                elif box == starting_box:
                    return False
                else:
                    direction = self.other_direction(box, 3-direction)

            box = starting_box
            direction = self.other_direction(starting_box, move%4)
            while True:
                #print('checking second part chain starting from {}, we are in {} {}'.format(starting_box, box, direction))
                box  = self.edges[4*box + direction]
                if box == self.limit:
                    return True
                elif self.counting_edges(box)!=2:
                    return False
                elif box == starting_box:
                    return False
                else:
                    direction = self.other_direction(box, 3-direction)
        return False


    def counting_edges(self, box):
        square = self.edges[4*box:4*box+4]
        return sum([1 for i in square if i>-1])
    
    def status_print(self, move):
        is_something = False
        print_move = self.convert_move_out(move)
        if self.is_boundary_crossing(move):
            print(print_move+" is a boundary crossing")
            is_something = True
        if self.is_double_crossing(move):
            print(print_move+" is a double crossing")
            is_something = True
        if self.is_in_loop(move):
            print(print_move+" is in a loop")
            is_something = True
        if self.is_in_chain(move):
            print(print_move+" is in a chain")
            is_something = True
        if not is_something:
            print(print_move+" is NOTHING (yet)")
        pass
    
    def convert_move_out(self, move):
        box = move//4
        row = str(box//self.size+1)
        column = chr(box%self.size + ord('A'))
        edges = ['Up', 'Left', 'Right', 'Down']
        edge = edges[move%4]
        #print('move:',move,'  box:',box,'  column:',column,'  row:',row,'  edge:',edge)
        return (column+row+' '+edge)
    
    def convert_move_in(self, move):
        box, direction = move.split(' ')
        column = ord(box[0])-ord('A')
        row = int(box[1:])-1
        edges = ['Up', 'Left', 'Right', 'Down']
        for i in range(4):
            if edges[i] == direction:
                edge = i
        return (row*self.size+column)*4+edge

    
    def print_state(self):
        legal_plays = [i for i in range(len(self.edges)) if self.edges[i] > -1]
        if len(legal_plays) == 0:
            print('FINISHED! Scores are', self.scores)
        else:
            for move in legal_plays:
                self.status_print(move)
        pass





























###########################################################
#               Inputs and main loop                      #
###########################################################


# Own more boxes than your opponent!

board_size = int(input())  # The size of the board.
player_id = int(input())  # The ID of the player. 'A'=first player, 'B'=second player.

board = DotsBoxesBoard(board_size, player_id)
print(board.edges)

while True:
    board.print_state()
    move = input()
    board.update_move(move)











# game loop
while False:
    # player_score: The player's score.
    # opponent_score: The opponent's score.
    player_score, opponent_score = [int(i) for i in input().split()]
    num_boxes = int(input())  # The number of playable boxes.
    for i in range(num_boxes):
        # box: The ID of the playable box.
        # sides: Playable sides of the box.
        box, sides = input().split()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # <box> <side> [MSG Optional message]
    print("A1 B MSG bla bla bla...")



   
   



