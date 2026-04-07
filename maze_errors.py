
class MazeError(Exception):
    """
    Base class for all maze application errors.
    Inherit from this for every custom exception.

    Catching MazeError catches ALL maze-related errors.
    Catching a subclass catches only that specific error type.
    """
    pass


class ConfigFileError(MazeError):

    def __init__(self, filename: str, reason: str) -> None:
        self.filename = filename
        self.reason = reason
        super().__init__(
            f"Cannot open config file '{filename}': {reason}"
        )


class ConfigSyntaxError(MazeError):

    def __init__(self, filename: str, line_number: int,
                 line: str, reason: str) -> None:
        self.filename = filename
        self.line_number = line_number
        self.line = line
        self.reason = reason
        super().__init__(
            f"Syntax error in '{filename}' at line {line_number}: "
            f"{reason}\n"
            f"  Got: '{line}'"
        )


class ConfigDuplicateKeyError(MazeError):

    def __init__(self, filename: str,
                 line_number: int, key: str) -> None:
        self.filename = filename
        self.line_number = line_number
        self.key = key
        super().__init__(
            f"Duplicate key '{key}' in '{filename}' at line {line_number}. "
            f"Each key must appear exactly once."
        )


class ConfigMissingKeyError(MazeError):

    def __init__(self, filename: str,
                 missing_keys: list[str]) -> None:
        self.filename = filename
        self.missing_keys = missing_keys
        keys_str = ", ".join(missing_keys)
        super().__init__(
            f"Missing mandatory keys in '{filename}': {keys_str}\n"
            f"  All required keys: "
            f"WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT"
        )


class ConfigTypeError(MazeError):

    def __init__(self, filename: str, line_number: int,
                 key: str, value: str, expected: str) -> None:
        self.filename = filename
        self.line_number = line_number
        self.key = key
        self.value = value
        self.expected = expected
        super().__init__(
            f"Invalid value for '{key}' in '{filename}' "
            f"at line {line_number}: expected {expected}, got '{value}'"
        )


class ConfigUnknownKeyError(MazeError):

    def __init__(self, filename: str,
                 line_number: int, key: str) -> None:
        self.filename = filename
        self.line_number = line_number
        self.key = key
        super().__init__(
            f"Unknown key '{key}' in '{filename}' at line {line_number}. "
            f"This key will be ignored."
        )


class ConfigValueError(MazeError):

    def __init__(self, key: str, value: str,
                 reason: str, hint: str = "") -> None:
        self.key = key
        self.value = value
        self.reason = reason
        self.hint = hint
        message = (
            f"Invalid value for '{key}': '{value}' — {reason}"
        )
        if hint:
            message += f"\n  Hint: {hint}"
        super().__init__(message)


class ConfigCoordinateError(MazeError):

    def __init__(self, key: str, coords: tuple[int, int],
                 width: int, height: int, reason: str) -> None:
        self.key = key
        self.coords = coords
        self.width = width
        self.height = height
        self.reason = reason
        super().__init__(
            f"Invalid {key} coordinates {coords}: {reason}\n"
            f"  Maze is {width}x{height}, "
            f"valid range: x=0..{width-1}, y=0..{height-1}"
        )
