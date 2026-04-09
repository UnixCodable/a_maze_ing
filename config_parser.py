from pydantic import BaseModel, Field, model_validator
from maze_errors import (ConfigCoordinateError,
                         ConfigValueError, ConfigFileError,
                         ConfigSyntaxError,
                         ConfigDuplicateKeyError,
                         ConfigMissingKeyError,
                         ConfigTypeError,)


class MazeConfig(BaseModel):
    width: int = Field(ge=2, le=1500)
    height: int = Field(ge=2, le=1500)
    entry:       tuple[int, int]
    exit:        tuple[int, int]
    output_file: str
    perfect:     bool
    seed:        int | None = None
    algorithm:   str | None = None
    animation:   bool = False

    @model_validator(mode="after")
    def validate_all(self) -> "MazeConfig":

        ex, ey = self.entry
        xx, xy = self.exit

        # Entry in bounds
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ConfigCoordinateError(
                "ENTRY", self.entry,
                self.width, self.height,
                f"x={ex} or y={ey} is outside the maze"
            )

        # Exit in bounds
        if not (0 <= xx < self.width and 0 <= xy < self.height):
            raise ConfigCoordinateError(
                "EXIT", self.exit,
                self.width, self.height,
                f"x={xx} or y={xy} is outside the maze"
            )

        # Entry != exit
        if self.entry == self.exit:
            raise ConfigValueError(
                "ENTRY/EXIT",
                str(self.entry),
                "entry and exit cannot be the same cell",
                "choose two different coordinates"
            )
        if self.algorithm == "hunt_and_kill":
            if self.width > 700:
                raise ConfigValueError("Width", str(self.width),
                                       "for the algorithm hunt_and_kill",
                                       " value should be less than 701")

            if self.height > 700:
                raise ConfigValueError("Height", str(self.height),
                                       "for the algorithm hunt_and_kill",
                                       " value should be less than 701")

        return self


def read_config(filename: str) -> dict:
    """
    Read and parse a KEY=VALUE config file.
    Returns a dict of parsed values ready to pass to MazeConfig.
    Raises specific ConfigError subclasses on any problem.
    """
    MANDATORY_KEYS = {
        "width", "height", "entry",
        "exit", "output_file", "perfect"
    }

    # These are ALL keys the parser accepts (mandatory + optional)
    KNOWN_KEYS = MANDATORY_KEYS | {
        "seed", "algorithm", "loop_factor", "animation"
    }

    config: dict = {}

    # ── Open the file ─────────────────────────────────────────────
    try:
        f = open(filename)
    except FileNotFoundError:
        raise ConfigFileError(filename, "file not found")
    except PermissionError:
        raise ConfigFileError(filename, "permission denied")
    except OSError as e:
        raise ConfigFileError(filename, str(e))

    # ── Parse line by line ────────────────────────────────────────
    with f:
        for line_number, line in enumerate(f, start=1):
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                continue

            # Must contain exactly one = sign
            if "=" not in stripped:
                raise ConfigSyntaxError(
                    filename, line_number, stripped,
                    "missing '=' sign — expected KEY=VALUE"
                )

            key_raw, value_raw = stripped.split("=", 1)
            key = key_raw.strip().lower()
            value = value_raw.strip()

            # Key must not be empty
            if not key:
                raise ConfigSyntaxError(
                    filename, line_number, stripped,
                    "empty key — write something before the '=' sign"
                )

            # Value must not be empty
            if not value:
                raise ConfigSyntaxError(
                    filename, line_number, stripped,
                    f"empty value for key '{key.upper()}' "
                    f"— write something after the '=' sign"
                )

            # Warn about unknown keys but do not crash
            if key not in KNOWN_KEYS:
                print(
                    f"Warning: unknown key '{key.upper()}' "
                    f"at line {line_number} — ignored"
                )
                continue

            # Duplicate key check
            if key in config:
                raise ConfigDuplicateKeyError(
                    filename, line_number, key.upper()
                )

            # ── Type conversion per key ───────────────────────────
            if key in ("width", "height"):
                try:
                    config[key] = int(value)
                except ValueError:
                    raise ConfigTypeError(
                        filename, line_number,
                        key.upper(), value, "a whole number"
                    )

            elif key in ("entry", "exit"):
                parts = value.split(",")
                if len(parts) != 2:
                    raise ConfigTypeError(
                        filename, line_number,
                        key.upper(), value,
                        "a coordinate pair like '0,0'"
                    )
                try:
                    x = int(parts[0].strip())
                    y = int(parts[1].strip())
                    config[key] = (x, y)
                except ValueError:
                    raise ConfigTypeError(
                        filename, line_number,
                        key.upper(), value,
                        "two integers separated by a comma, like '5,10'"
                    )

            elif key == "perfect":
                if value.lower() not in ("true", "false"):
                    raise ConfigTypeError(
                        filename, line_number,
                        "PERFECT", value,
                        "'True' or 'False'"
                    )
                config[key] = value.lower() == "true"

            elif key == "animation":
                if value.lower() not in ("true", "false"):
                    raise ConfigTypeError(
                        filename, line_number,
                        "Animation", value,
                        "'True' or 'False'"
                    )
                config[key] = value.lower() == "true"

            elif key == "seed":
                try:
                    config[key] = int(value)
                except ValueError:
                    raise ConfigTypeError(
                        filename, line_number,
                        "SEED", value, "a whole number"
                    )

            else:
                # string keys like output_file, algorithm
                config[key] = value

    # ── Check all mandatory keys are present ──────────────────────
    missing = [k.upper() for k in MANDATORY_KEYS if k not in config]
    if missing:
        raise ConfigMissingKeyError(filename, missing)

    return config


if __name__ == "__main__":
    di = read_config("config.txt")
    try:
        config = MazeConfig(**di)
        print(config.perfect)
    except Exception as e:
        print(f"{e}")
