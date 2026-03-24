import random
from config_parser import MazeConfig


class MazeGenerator():

    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.width = config.width
        self.height = config.height

        self.rng = random.Random(config.seed)

        self.grid: list[list[int]] = []
        self.pattern_cells: set[tuple[int, int]] = set()

        self.path: str = ""

    def _init_grid(self) -> None:

        self.grid = [[0xF for _ in range(self.width)]
                     for _ in range(self.height)]

    def _carve_wall(self, x: int, y: int, direction: int) -> None:
        dx, dy = self.DELTA[direction]
        nx, ny = x + dx, y + dy

        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~self.OPPOSITE[direction]

    def _get_42_cells(self) -> set[tuple[int, int]] | None:
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
        for (x, y) in self.pattern_cells:
            self.grid[y][x] = 0xF

    def _run_dfs(self) -> None:

        start_x, start_y = self.config.entry

        visited: set[tuple[int, int]] = set()
        visited.add((start_x, start_y))

        # Also mark pattern cells as visited so DFS never enters them
        visited.update(self.pattern_cells)

        stack = [(start_x, start_y)]

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
                    stack.append((nx, ny))
                    moved = True
                    break

            if not moved:
                stack.pop()   # backtrack

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

    def _open_border(self, x: int, y: int) -> None:
        """
        Removes the outer border wall for a cell that sits on the maze edge.
        Entry and exit cells need one wall removed
        so the player can enter/exit.
        
        Determines which side to open based on position:
        top row    → remove NORTH
        bottom row → remove SOUTH
        left col   → remove WEST
        right col  → remove EAST
        
        Args:
            x, y: the entry or exit cell coordinates
        """
        if y == 0:
            self.grid[y][x] &= ~self.NORTH
        elif y == self.height - 1:
            self.grid[y][x] &= ~self.SOUTH
        elif x == 0:
            self.grid[y][x] &= ~self.WEST
        elif x == self.width - 1:
            self.grid[y][x] &= ~self.EAST
    
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
        
        ex, ey = self.config.entry
        exit_ = self.config.exit
        
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
        
        self.path = ""  # no solution found
    
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
        
        pattern = self._get_42_cells()
        if pattern is None:
            print("Error: maze too small to display the '42' pattern.")
            self.pattern_cells = set()
        else:
            self.pattern_cells = pattern
            self._lock_42_cells()
        
        self._run_dfs()
        self._fix_open_areas()
        
        self._open_border(*self.config.entry)
        self._open_border(*self.config.exit)
        
        self._solve()
    
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
        ex, ey = self.config.entry
        exit_ = self.config.exit
        
        try:
            with open(self.config.output_file, 'w') as f:
                for row in self.grid:
                    f.write(''.join(format(cell, 'X') for cell in row) + '\n')
                f.write('\n')
                f.write(f"{ex},{ey}\n")
                f.write(f"{exit_[0]},{exit_[1]}\n")
                f.write(self.path + '\n')
        except OSError as e:
            raise ValueError(f"Cannot write output file: {e}")

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
