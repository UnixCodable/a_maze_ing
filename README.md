# A_maze_ing : An old gaming story

***This project has been created as part of the 42 curriculum by rshikder and lbordana.***

## Description

A_maze_ing shuffle algorithm and first visualization tools together into our brains.

It is the very first big project after python piscine and his goals are mostly to enforce our new-learned understandings, through a maze generation and visualization concept.

## Instructions

First, you need to ensure that all packages are installed. For that, we strongly recommend that you use a virtual environment. So we can do :

```bash
python3 -m venv venv
source ./venv/bin/activate
make install
```

After that, you can set your config file (see below) or use the default one (config.txt).\
For the default one :

```bash
make run
```

Otherwise :

```bash
python3 a_maze_ing.py <your_file>
```
\
Once it is launched, here are some commands you can use:\
\
**[R]**             to regenerate a maze\
**[E]**             to relaunch the animation (or the basic)\
**[T]**             to change the theme\
**[+]**             to speed up the maze\
**[-]**             to speed down the maze\
**[w]** or **[↑]**  to move see the top of the maze\
**[a]** or **[←]**  to move see the left side of the maze\
**[s]** or **[↓]**  to move see the bottom of the maze\
**[d]** or **[→]**  to move see the right side of the maze\
**[space bar]**     to pause / unpause the maze generation\
**[mouse wheel]**   to scroll in a fluid way\

## Resources
\
[RSHIKDER resources] :\
For this project I have watched tutorilas online on Depth-First Search algorithm for maze generation and breadth first search algorithm to solve the shortest path. Read online resoures, https://www.geeksforgeeks.org/python/python-program-for-depth-first-search-or-dfs-for-a-graph/
https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/.
https://en.wikipedia.org/wiki/Maze_generation_algorithm
I have used AI to understand the concept, expectaion and improvement of functionalities. 
\
- lbordana resources :\
\
Firstly concerning AI, I try to use it at least as possible during my learning path. However, for this project it was used on my side for gathering ideas on how to not write on disk through **pillow** and from there I got the idea of using **numpy** then **cv2**.\
\
It was also used to detect and understand 2 to 3 errors in the code, that were actually made because on how **mlx** is wrapped. No code was copy / paste or given by AI.\
\
Then, on the 'pure' resources part, I often use stackoverflow forums to gather ideas but on the algorithm part (Hunt and Kill for me), here is a website shared by [lbonnet](https://github.com/Kletsol) and [gtourdia](https://github.com/sousampere) that I used : [Hunt and Kill maze algorithm](https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm)\
\
Otherwise, only official documentation or the 42 Slack network.\

## Config File

The config file structure can handle :

```python
    width: int = Field(ge=2, le=3000)
    height: int = Field(ge=2, le=3000)
    entry:       tuple[int, int]
    exit:        tuple[int, int]
    output_file: str
    perfect:     bool
    seed:        int | None = None
    algorithm:   str | None = None
    animation:   bool = False
```

As you see, only **seed**, **algorithm** and **animation** are optional.\
\
All those option can be set like this in a config file:

```
WIDTH=3000
HEIGHT=3000
ENTRY=39,48
EXIT=4,4
OUTPUT_FILE=maze.txt
PERFECT=True
ALGORITHM=dfs
ANIMATION=True

#  Algorithms:
#
#  - hunt_and_kill
#  - dfs
```

## Maze algorithms

We chosen to use 2 algorithms:\
\
    - DFS (Depth-first search) : Using backtracking when encountering a locked way.\
        [RSHIKDER PART]\
        DFS(Depth-First Search algorithm) is used to create maze generator. as it is easy and beginner friendly and its default output is a perfect maze which is the requirements of the subject.
    - Hunt and Kill : Using a scan from top when encountering a locked way.\
        This one was easily reusable with DFS algorithm, and understandable, as it was almost working the same way. I needed to implement a new scan function but otherwise used the DFS structure as patron.\

## Reusability

[RSHIKDER PART]
    For the reusabitlity of the project we have put the mazegeneration as a stand alone class in a module "maze_generator.py" in directory "src" as per required for .toml file. And have put "__init__.py" file for python to consider as a packge. we have created a .toml file for the build system and generation of .tar.gz and .whl file so that can be installed by pip and used. and put "readme.md" in the directory to guide how it can be used

## Project management

Decisions were taking by the two of us. We had a very nice collaboration and our fixed roles were :\
    - rshikder for DFS algorithm\
    - rshikder for parsing / error handling\
    - lbordana for the visualiser\
    - lbordana for hunt and kill algorithm\
\
This planning didn't move, we worked quite on our side on isolated git branches, and meet up 1 to 3 times a week to discuss our implementations and get reviews for ideas.\
