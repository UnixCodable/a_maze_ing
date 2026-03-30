from pydantic import BaseModel, Field, model_validator
from typing import Tuple, Optional


class MazeConfig(BaseModel):
    width: int = Field(ge=2, le=500)
    height: int = Field(ge=2, le=500)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    algorithm: Optional[str] = "dfs"

    @model_validator(mode="after")
    def validate_coordinates(self):
        ex, ey = self.entry
        xx, xy = self.exit

        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT cannot be the same")

        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError("ENTRY coordinates out of bounds")

        if not (0 <= xx < self.width and 0 <= xy < self.height):
            raise ValueError("EXIT coordinates out of bounds")

        return self


def read_config(filename: str) -> dict:
    config = {}

    try:
        with open(filename) as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Line {line_number}: invalid syntax")

                key, value = line.split("=", 1)

                key = key.strip().lower()
                value = value.strip()

                if key in config:
                    raise ValueError(f"Line {line_number}: "
                                     f"duplicate key '{key}'")

                # Parse special values
                if key in ['entry', 'exit']:
                    try:
                        x, y = value.split(',')
                        config[key] = (int(x.strip()), int(y.strip()))
                    except ValueError:
                        raise ValueError("Invalid {} tuple at "
                              "line {}".format(key, line_number))
                elif key == 'perfect':
                    config[key] = value.lower() == 'true'
                elif key in ['width', 'height', 'seed']:
                    config[key] = int(value)
                else:
                    config[key] = value

        return config

    except FileNotFoundError:
        raise ValueError("Configuration file not found")

    except OSError:
        raise ValueError("Unable to read configuration file")
    except PermissionError:
        raise (" add permission to the file")


if __name__ == "__main__":
    di = read_config("default_config.txt")
    try:
        config = MazeConfig(**di)
        print(config)
    except Exception as e:
        print(f"{e}")
