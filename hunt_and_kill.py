# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  hunt_and_kill.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/02 02:46:39 by lbordana        #+#    #+#               #
#  Updated: 2026/04/02 03:40:12 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from random import randint
from config_parser import read_config


class MazeHunt():
    def __init__(self):
        self.visited_cells = []
        self.height = read_config('config.txt').get('height', 0)
        self.width = read_config('config.txt').get('width', 0)

    def scan(self):
        pass

    def check_and_walk(self, starting_point):
        height = starting_point[0]
        width = starting_point[1]
        for _ in range(4):
            exclude = []
            path_direction = randint(1, 4)
            if path_direction == 1:
                if self.validate(height - 1, width) is True:
                    self.visited_cells[height - 1][width] = 1
                    
        

    def first_point(self) -> tuple:
        position = (randint(0, self.height - 1), randint(0, self.width - 1))
        self.visited_cells[position[0]][position[1]] = 1
        return position

    def fullfill_zeros(self):
        for _ in range(self.height):
            self.visited_cells.append([0 for _ in range(self.width)])


if __name__ == '__main__':
    maze = MazeHunt()
    maze.fullfill_zeros()
    maze.starting_point()
