## Pathfinding Algorithm Visualizer
* Interactive tool for path exploration between two nodes using popular algorithms.
* Provides visual representation of algorithms in-action.
* Supports loading and saving your own boards, as well as randomized preloaded mazes.

## Images
<p float="left">
  <img src="/images/screenshot1.PNG" width=45% height=40% />
  <img src="/images/screenshot2.PNG" width=45% height=40% />
</p>

## Technologies
Project is created with:
* Python 3.10.6
* Pygame 2.1.2

## Setup
To use this project on Windows, need to download libraries:
```
> pip install pygame
```

## Usage
Run in terminal:
```
> python pathfinder.py
```
Node color indications:
* Blue/yellow are the start/end
* White is unexplored area
* Black are barriers
* Green is the edge of exploration
* Red is explored area
* Purple is the identified path


Program controls:
* Your first left mouse click will place the start node
* Second click will place the end node
* All remaining clicks will place walls
* Your right mouse click will remove selected node
* Keyboard press "1" runs the A* search algorithm
* Keyboard press "2" runs the Dijkstra's algorithm
* Keyboard press "3" runs the Depth-first search algorithm
* Keyboard press "R" loads a random preloaded maze
* Keyboard press "C" clears the board
* Keyboard press "S" saves your current board layout
* Keyboard press "L" loads a saved board layout
* Keyboard press "H" prints this menu for help
