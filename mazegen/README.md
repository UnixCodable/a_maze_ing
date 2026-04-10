# Maze Generator Module

A Python module for generating mazes with customizable parameters, multiple algorithms, and animation support.

## Description

The `mazegen` module provides a `MazeGenerator` class that creates perfect mazes (or imperfect with loops) using configurable algorithms. It supports embedding patterns like "42", solving mazes, and generating animation frames for visualization.

## Features

- **Multiple Algorithms**: Depth-First Search (DFS) and Hunt-and-Kill algorithms
- **Configurable Mazes**: Custom width, height, entry/exit points, and seeds
- **Pattern Embedding**: Automatically embeds a "42" pattern in larger mazes
- **Maze Solving**: Finds the shortest path from entry to exit
- **Animation Support**: Generates frame-by-frame animation data
- **Loop Addition**: Option to add loops for imperfect mazes
- **Validation**: Ensures no 3x3 open areas and protects entry/exit areas

## Installation

This module is part of the `mazegen` package. Install the package using pip:

```bash
pip install .
```

Or for development:

```bash
pip install -e .[dev]
```

## Usage

```python
from mazegen import MazeGenerator
from config_parser import MazeConfig

# Create a configuration
config = MazeConfig(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    seed=42,
    algorithm='dfs',  # or 'hunt_and_kill'
    perfect=True,     # False to add loops
    output_file='maze.txt'
)

# Generate the maze
generator = MazeGenerator(config)
generator.generate()

# Save to file
generator.save()

# Access results
print(f"Shortest path: {generator.path}")
frames = generator.animate_save_file()
```

## API Reference

### MazeGenerator Class

#### `__init__(config: MazeConfig)`
Initializes the maze generator with the given configuration.

#### `generate() -> None`
Generates the maze by running the selected algorithm and applying post-processing.

#### `save() -> None`
Saves the generated maze to the configured output file in the required format.

#### Properties
- `grid`: 2D list representing the maze walls (bitwise flags)
- `path`: String of moves ('N', 'E', 'S', 'W') for the shortest path
- `frames`: List of animation frames for visualization

## Configuration

The module uses a `MazeConfig` object (from `config_parser`) with the following parameters:

- `width`, `height`: Maze dimensions
- `entry`, `exit`: Tuples for start and end coordinates
- `seed`: Random seed for reproducible generation
- `algorithm`: 'dfs' or 'hunt_and_kill'
- `perfect`: Boolean for perfect maze (no loops)
- `output_file`: Path to save the maze

## Output Format

The saved maze file contains:
- Hexadecimal grid representation (one row per line)
- Empty line separator
- Entry coordinates (x,y)
- Exit coordinates (x,y)
- Solution path string

## Dependencies

- Python 3.10+
- `config_parser` module (part of the project)
- "tqdm" package for for visualization loading bar

