# a_maze_ing.py
import sys
from config_parser import read_config, MazeConfig
from src.mazegen import MazeGenerator


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        raw = read_config(sys.argv[1])   # → dict
        config = MazeConfig(**raw)          # → validated config

        gen = MazeGenerator(config)         # set up
        gen.generate()                      # build maze
        gen.save()
        gen.animate_save_file()                       # write file

        # display will be: MazeDisplay(gen).show()  ← later

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
