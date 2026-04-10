import random
from tqdm import tqdm
from typing import Optional, Any


class MazeGenerator():

    def __init__(self, config: dict[Any, Any]) -> None:
        """Initialize MazeGenerator with config parameters."""
        self.config = config
        self.width = config.get('width', 4)
        self.height = config.get('height', 4)

        self.rng = random.Random(config.get('seed', None))

        self.grid: list[list[int]] = []
        self.pattern_cells: set[tuple[int, int]] = set()

        self.path: str = ""
        self.frames: list[list[int | int | str]] = []

    def _init_grid(self) -> None:
        """Initialize grid with all walls closed (all bits set to 0xF)."""
        self.grid = [[0xF for _ in range(self.width)]
                     for _ in range(self.height)]

    def _carve_wall(self, x: int, y: int, direction: int) -> None:
        """Remove wall between cell (x, y) and its neighbor
          in the given direction."""
        dx, dy = self.DELTA[direction]
        nx, ny = x + dx, y + dy

        self.grid[y][x] &= ~direction
        self.animate(x, y)
        self.grid[ny][nx] &= ~self.OPPOSITE[direction]
        self.animate(nx, ny)

    def _get_42_cells(self) -> set[tuple[int, int]] | None:
        """Generate set of cells that form the '42' pattern,
          or None if maze is too small."""
        DIGIT_W, DIGIT__H, GAP = 3, 5, 1
        TOTAL_W = DIGIT_W * 2 + GAP
        TOTAL_H = DIGIT__H

        if self.width < TOTAL_W + 4 or self.height < TOTAL_H + 4:
            return None

        start_x = (self.width - TOTAL_W) // 2
        start_y = (self.height - TOTAL_H) // 2

        FOUR = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ]
        TWO = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 1],
        ]

        cells: set[tuple[int, int]] = set()

        for row, line in enumerate(FOUR):
            for col, filled in enumerate(line):
                if filled:
                    cells.add((start_x + col, start_y + row))

        for row, line in enumerate(TWO):
            for col, filled in enumerate(line):
                if filled:
                    cells.add((start_x + DIGIT_W + GAP + col, start_y + row))

        return cells

    def _lock_42_cells(self) -> None:
        """Freeze pattern cells so algorithms won't carve through them."""
        for (x, y) in self.pattern_cells:
            self.grid[y][x] = 0xF

    def _get_pattern_bounds(self) -> tuple[int, int, int, int]:
        """Return bounding box (min_x, min_y, max_x, max_y) of
          the pattern cells."""
        if not self.pattern_cells:
            return (0, 0, 0, 0)

        xs = [x for x, y in self.pattern_cells]
        ys = [y for x, y in self.pattern_cells]
        return (min(xs), min(ys), max(xs), max(ys))

    def _run_dfs(self) -> None:
        """Generate maze using Depth-First Search algorithm."""
        print('\n=== Generating Maze with DFS ===\n')

        start_x, start_y = self.config.get('entry', (0, 0))

        visited: set[tuple[int, int]] = set()
        visited.add((start_x, start_y))

        # Also mark pattern cells as visited so DFS never enters them
        visited.update(self.pattern_cells)

        stack = [(start_x, start_y)]
        p_bar = tqdm(total=(self.width * self.height - len(visited)),
                     desc="Generating maze", colour='green', ascii='  =')

        while stack:
            x, y = stack[-1]
            directions = [self.NORTH, self.SOUTH, self.EAST, self.WEST]
            self.rng.shuffle(directions)

            moved = False
            for direction in directions:
                dx, dy = self.DELTA[direction]
                nx, ny = x + dx, y + dy

                # Check bounds + not visited
                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in visited):

                    #  calls the method above
                    self._carve_wall(x, y, direction)
                    visited.add((nx, ny))
                    p_bar.update(1)
                    stack.append((nx, ny))
                    self.animate(nx, ny)
                    moved = True
                    break

            if not moved:
                stack.pop()   # backtrack

    def _scan(self, directions: list[int],
              stack: set[tuple[int, int]],
              unvisited: list[tuple[int, int]]) -> Optional[tuple[int, int]]:
        """Find an unvisited cell adjacent to visited
          stack for Hunt and Kill algorithm."""

        for u in unvisited:
            for direction in directions:
                dx, dy = self.DELTA[direction]
                nx, ny = u[0] + dx, u[1] + dy

                if (nx, ny) in stack:
                    self._carve_wall(u[0], u[1], direction)
                    stack.add(u)
                    unvisited.pop(unvisited.index(u))
                    return u
        return None

    def _run_hunt_and_kill(self) -> None:
        """Generate maze using Hunt and Kill algorithm."""
        print('\n=== Generating Maze with Hunt and Kill ===\n')

        start_x, start_y = (self.rng.randint(0, self.width - 1),
                            self.rng.randint(0, self.height - 1))

        pattern: set[tuple[int, int]] = set()
        unvisited: list[tuple[int, int]] = list()
        stack: set[tuple[int, int]] = set()
        stack.add((start_x, start_y))

        # Also mark pattern cells as visited so H&K never enters them
        pattern.update(self.pattern_cells)

        for ly in range(0, self.height):
            for lx in range(0, self.width):
                if (lx, ly) not in pattern and (lx, ly) not in stack:
                    unvisited.append((lx, ly))

        x, y = start_x, start_y
        for _ in tqdm(range(0, len(unvisited)),
                      desc='Generating maze',
                      colour='green', ascii='  ='):
            directions = [self.NORTH, self.SOUTH, self.EAST, self.WEST]
            self.rng.shuffle(directions)

            moved = False
            for direction in directions:
                dx, dy = self.DELTA[direction]
                nx, ny = x + dx, y + dy

                # Check bounds + not visited / stacked
                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in stack and (nx, ny) not in pattern):

                    #  calls the method above
                    self._carve_wall(x, y, direction)
                    x, y = nx, ny
                    stack.add((nx, ny))
                    unvisited.pop(unvisited.index((nx, ny)))
                    # self.animate(nx, ny)
                    moved = True
                    break

            if moved is False:
                scan_result = self._scan(directions, stack, unvisited)
                if scan_result is None:
                    return
                x, y = scan_result

    def _fix_open_areas(self) -> None:
        """
        The subject forbids corridors wider than 2 cells (no 3x3 open area).
        This scans every possible 2x2 block of cells. If all 4 cells are
        mutually open (no walls between them), it adds one wall to break it.
        Repeats until no violations remain.

        A 3x3 open area necessarily contains a 2x2 sub-block that is
          fully open,
        so fixing all 2x2 violations removes all 3x3 (and larger) ones too.
        Never touches pattern_cells.
        """
        changed = True
        while changed:
            changed = False
            for y in range(self.height - 1):
                for x in range(self.width - 1):
                    if self._is_2x2_open(x, y):
                        self._add_wall_in_2x2(x, y)
                        changed = True

    def _is_2x2_open(self, x: int, y: int) -> bool:
        """
        Check if the 2x2 block starting at (x,y) is fully open.
        We check:
        - (x,y)   has no EAST wall   → connected to (x+1, y)
        - (x,y)   has no SOUTH wall  → connected to (x, y+1)
        - (x+1,y) has no SOUTH wall  → connected to (x+1, y+1)
        - (x,y+1) has no EAST wall   → connected to (x+1, y+1)
        If all 4 internal walls are missing, the block is fully open.
        """
        # Skip if any cell is a locked pattern cell
        for cx, cy in [(x, y), (x+1, y), (x, y + 1), (x + 1, y+1)]:
            if (cx, cy) in self.pattern_cells:
                return False

        g = self.grid
        top_left_east = not (g[y][x] & self.EAST)
        top_left_south = not (g[y][x] & self.SOUTH)
        top_right_south = not (g[y][x+1] & self.SOUTH)
        bot_left_east = not (g[y+1][x] & self.EAST)

        return (top_left_east and top_left_south and top_right_south
                and bot_left_east)

    def _add_wall_in_2x2(self, x: int, y: int) -> None:
        """
        Add one internal wall randomly inside the 2x2 block.
        Pick randomly to avoid bias.
        """
        # 4 internal walls to choose from:
        # EAST of (x,y), SOUTH of (x,y), SOUTH of (x+1,y), EAST of (x,y+1)
        choices = [
            (x, y,   self.EAST),
            (x, y,   self.SOUTH),
            (x+1, y, self.SOUTH),
            (x, y+1, self.EAST),
        ]
        cx, cy, direction = self.rng.choice(choices)
        dx, dy = self.DELTA[direction]
        nx, ny = cx + dx, cy + dy
        # Add wall on both sides
        self.grid[cy][cx] |= direction
        self.grid[ny][nx] |= self.OPPOSITE[direction]

    def _solve(self) -> None:
        """
        BFS from entry to exit to find the shortest valid path.
        A move is valid only if the wall between two cells is OPEN (bit = 0).

        Stores the result as a string in self.path e.g. "NNEESW".
        Sets self.path = "" if no solution exists
        (shouldn't happen in valid maze).
        """
        from collections import deque

        DIR_LETTER = {
            self.NORTH: 'N',
            self.EAST:  'E',
            self.SOUTH: 'S',
            self.WEST:  'W',
        }

        ex, ey = self.config.get('entry', (0, 0))
        exit_ = self.config.get('exit', (1, 1))

        # Queue stores (x, y, path_string_so_far)
        queue: deque[tuple[int, int, str]] = deque()
        queue.append((ex, ey, ""))
        visited: set[tuple[int, int]] = {(ex, ey)}

        while queue:
            x, y, path = queue.popleft()

            if (x, y) == exit_:
                self.path = path
                return

            for direction, letter in DIR_LETTER.items():
                # Wall is CLOSED if the bit is SET — can't pass
                if self.grid[y][x] & direction:
                    continue

                dx, dy = self.DELTA[direction]
                nx, ny = x + dx, y + dy

                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + letter))
                    self.animate(x, y)

        self.path = ""  # no solution found

    def _add_loops(self) -> None:
        """Create loops in the maze by randomly removing ~20% of walls,
          avoiding critical paths."""
        protected: set[tuple[int, int]] = set(self.pattern_cells)

        entry = self.config.get('entry', (0, 0))    # e.g. (0, 0)
        exit_ = self.config.get('exit', (1, 1))     # e.g. (19, 14)

        # Protect entry and exit cells directly
        protected.add(entry)
        protected.add(exit_)

        # Protect each immediate neighbour of entry and exit
        # A neighbour is any in-bounds cell adjacent to them
        for cell in (entry, exit_):
            cx, cy = cell
            for direction in (self.NORTH, self.SOUTH,
                              self.EAST, self.WEST):
                dx, dy = self.DELTA[direction]
                nx, ny = cx + dx, cy + dy

                if (0 <= nx < self.width
                        and 0 <= ny < self.height):
                    protected.add((nx, ny))

        candidates: list[tuple[int, int, int]] = []

        for y in range(self.height):
            for x in range(self.width):

                if (x, y) in protected:
                    continue

                for direction in (self.EAST, self.SOUTH):
                    dx, dy = self.DELTA[direction]
                    nx, ny = x + dx, y + dy

                    if not (0 <= nx < self.width
                            and 0 <= ny < self.height):
                        continue

                    # neighbour must also not be protected
                    if (nx, ny) in protected:
                        continue

                    # wall must currently be CLOSED
                    if self.grid[y][x] & direction:
                        candidates.append((x, y, direction))

        # ── Shuffle and remove walls
        self.rng.shuffle(candidates)

        loop_count = int(len(candidates) * 0.2)

        for x, y, direction in candidates[:loop_count]:
            self._carve_wall(x, y, direction)
            self.animate(x, y)

    def generate(self) -> None:
        """
        PUBLIC METHOD — call this to build the maze.
        Calls all private methods in the correct order:

        1. _init_grid        → blank grid, all walls closed
        2. _get_42_cells     → figure out where "42" goes
        3. _lock_42_cells    → freeze those cells (DFS will skip them)
        4. _run_dfs          → carve the maze paths
        5. _fix_open_areas   → enforce the no-3x3 rule
        6. _open_border x2   → open entry and exit outer walls
        7. _solve            → find shortest path, store in self.path
        """
        self._init_grid()
        self.frames = []

        pattern = self._get_42_cells()
        if pattern is None:
            print("Error: maze too small to display the '42' pattern.")
            self.pattern_cells = set()
        else:
            self.pattern_cells = pattern
            self._lock_42_cells()

        if self.pattern_cells:
            bounds = self._get_pattern_bounds()
            sx, sy, ex, ey = bounds

            if self.config.get('entry', (0, 0)) in self.pattern_cells:
                raise ValueError(
                    f"ENTRY {self.config.get('entry', (0, 0))} is inside the "
                    f"'42' pattern (columns {sx}-{ex}, rows {sy}-{ey}). "
                    f"Move ENTRY or change SEED."
                )

            if self.config.get('exit', (1, 1)) in self.pattern_cells:
                raise ValueError(
                    f"EXIT {self.config.get('exit', (1, 1))} is inside the "
                    f"'42' pattern (columns {sx}-{ex}, rows {sy}-{ey}). "
                    f"Move EXIT or change SEED."
                )

        if self.config.get('algorithm', 'dfs') == 'hunt_and_kill':
            self._run_hunt_and_kill()
        else:
            self._run_dfs()
        self._fix_open_areas()
        if not self.config.get('perfect', True):
            self._add_loops()

        self._solve()
        self.animate_short_path()

    def save(self) -> None:
        """
        PUBLIC METHOD — call after generate() to write the output file.
        Format (from subject):
        - one hex digit per cell, one row per line  (uppercase)
        - empty line
        - entry coords as "x,y"
        - exit  coords as "x,y"
        - solution path as string of N/E/S/W
        """
        ex, ey = self.config.get('entry', (0, 0))
        exit_ = self.config.get('exit', (1, 1))

        try:
            with open(self.config.get('output_file', 'maze.txt'), 'w') as f:
                for row in self.grid:
                    f.write(''.join(format(cell, 'X') for cell in row) + '\n')
                f.write('\n')
                f.write(f"{ex},{ey}\n")
                f.write(f"{exit_[0]},{exit_[1]}\n")
                f.write(self.path + '\n')
        except OSError as e:
            raise ValueError(f"Cannot write output file: {e}")

    def animate(self, x: int, y: int) -> None:
        """Record animation frame for cell update at (x, y)."""
        hexadecimal = '0123456789ABCDEF'
        self.frames.append([x, y, hexadecimal[self.grid[y][x]]])

    def animate_save_file(self) -> list[list[int | int | str]]:
        """Return list of animation frames for visualization."""
        return self.frames

    def animate_short_path(self) -> None:
        """Record animation frames for the solution path from entry to exit."""
        x, y = self.config.get('entry', (0, 0))

        MOVE = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        for move in self.path:
            dx, dy = MOVE[move]
            x += dx
            y += dy

            self.animate(x, y)

    # Constants
    NORTH = 0x1
    EAST = 0x2
    SOUTH = 0x4
    WEST = 0x8

    DELTA = {
        NORTH: (0, -1),
        EAST: (1, 0),
        SOUTH: (0, 1),
        WEST: (-1, 0),
    }

    OPPOSITE = {
        NORTH: SOUTH,
        EAST: WEST,
        SOUTH: NORTH,
        WEST: EAST,
    }
