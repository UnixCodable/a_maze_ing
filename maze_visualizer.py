# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 03:32:25 by lbordana        #+#    #+#               #
#  Updated: 2026/03/21 04:23:22 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx


class MazeVisualizer:
    def __init__(self):
        pass

    def maze_chunk(self, byte: str) -> None:
        pass


def visualize() -> None:
    hex_only = str()
    with open('output_maze.txt', 'r') as output:
        for hex in output.read().split('\n'):
            if hex == '':
                break
            hex_only += hex
    print(hex_only)

    window = Mlx()


if __name__ == '__main__':
    visualize()