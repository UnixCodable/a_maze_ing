import sys
from config_parser import read_config, MazeConfig
from maze_visualizer import render
from src.mazegen import MazeGenerator
from maze_errors import (
    MazeError,
    ConfigFileError,
    ConfigSyntaxError,
    ConfigDuplicateKeyError,
    ConfigMissingKeyError,
    ConfigTypeError,
    ConfigValueError,
    ConfigCoordinateError,
)
from pydantic import ValidationError


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
        if raw.get('animation') is True:
            render(gen, gen.animate_save_file())
        else:
            render(gen)
        # display will be: MazeDisplay(gen).show()  ← later

    except ConfigFileError as e:
        # File could not be opened at all
        print(f"[File Error] {e}")
        sys.exit(1)

    except ConfigSyntaxError as e:
        # A line in the file was malformed
        print(f"[Syntax Error] {e}")
        sys.exit(1)

    except ConfigDuplicateKeyError as e:
        # Same key appeared twice
        print(f"[Duplicate Key] {e}")
        sys.exit(1)

    except ConfigMissingKeyError as e:
        # One or more mandatory keys were absent
        print(f"[Missing Key] {e}")
        sys.exit(1)

    except ConfigTypeError as e:
        # A value could not be converted to its expected type
        print(f"[Type Error] {e}")
        sys.exit(1)

    except ConfigCoordinateError as e:
        # Entry or exit coordinates were out of bounds
        print(f"[Coordinate Error] {e}")
        sys.exit(1)

    except ConfigValueError as e:
        # A value was syntactically correct but logically wrong
        print(f"[Value Error] {e}")
        sys.exit(1)

    except ValidationError as e:
        # Pydantic field-level validation failed (ge, le, etc.)
        print(f"[Validation Error] {e}")
        sys.exit(1)

    except MazeError as e:
        # Catch-all for any other custom maze error
        print(f"[Error] {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"[Error] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
