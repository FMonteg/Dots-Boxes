###########################################################
#               Imports and definitions                   #
###########################################################

import sys
import math


class DotsBoxesBoard(object):
    def __init__(self, size):
        self.size = size
        self.limit = self.size**2
        
        self.edges = []
        
        self.scores = [0,0]
        self.current_player = 0

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
                
                if i==self.size-1:
                    self.edges.append(self.limit)
                else:
                    self.edges.append((i+1)*self.size+(j))
                
                if j==self.size-1:
                    self.edges.append(self.limit)
                else:
                    self.edges.append((i)*self.size+(j+1))
        #Board's edge
        self.edges.append(-1)
        self.edges.append(-1)
        self.edges.append(-1)
        self.edges.append(-1)

        pass

    def update_move(self, box, direction):
        edge = 4*box + direction
        neighbour = self.edges[edge]
        self.edges[edge] = -1

        if neighbour>-1:
            self.edges[4*neighbour + 3 - direction] = -1
        
        self.update_score_and_player(box, neighbour)   

        pass

    def update_score_and_player(self, box_1, box_2):
        switch = True
        if box_1 < self.limit:
            square = self.edges[4*box_1:4*box_1+4]
            if sum(square) == -4:
                self.score[self.current_player] += 1
                switch = False
        if box_2 < self.limit:
            square = self.edges[4*box_2:4*box_2+4]
            if sum(square) == -4:
                self.score[self.current_player] += 1
                switch = False 
        if switch:
            self.current_player = 1 - self.current_player
        pass











###########################################################
#               Inputs and main loop                      #
###########################################################


# Own more boxes than your opponent!

board_size = int(input())  # The size of the board.
player_id = input()  # The ID of the player. 'A'=first player, 'B'=second player.

# game loop
while True:
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
