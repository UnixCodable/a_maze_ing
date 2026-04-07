# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/07 00:44:00 by lbordana        #+#    #+#               #
#  Updated: 2026/04/07 18:12:26 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mazegen import MazeGenerator
from maze_visualizer import render

from config_parser import MazeConfig


m = MazeConfig
m.width = 500
m.height = 500
m.entry = (40, 40)
m.exit = (400, 400)
m.output_file = 'other_name.txt'
m.perfect = True
m.seed = None
gen = MazeGenerator(m)
gen.generate()
gen.save()
render()