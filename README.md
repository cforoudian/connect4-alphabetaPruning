# Connect 4 AI Player Implementation

Overview
This repository contains an implementation of Connect 4 AI players using minimax and alpha-beta pruning algorithms. The project was developed as part of an AI course at UC Davis, focusing on game-playing algorithms and decision-making strategies.

Key Features
-- Minimax Algorithm: Implementation of the classic minimax algorithm without alpha-beta pruning

-- Alpha-Beta Pruning: Enhanced version with alpha-beta pruning for more efficient search


Performance: The alpha-beta implementation consistently outperforms Monte Carlo-based approaches (winning 17 out of 20 games)


Optimization Techniques:

-- Move ordering to improve pruning efficiency

-- Pre-computed evaluation windows

-- Early termination checks

-- Strategic position evaluation



Implementation Details
Minimax AI

-- Conservative depth limit (4) to ensure moves complete within the 3-second time constraint

-- First-move optimization (center column)

-- Comprehensive position evaluation function (split between evaluate_window and evaluate_position)


Alpha-Beta AI
The alphaBetaAI class extends the minimax funcitonality with:

-- Alpha-beta pruning to reduce the search space

-- Deeper search depth (5) enabled by pruning efficiency

-- Move ordering to maximize pruning effectiveness

-- Pre-computed evaluation windows for faster board assessment

-- Quick terminal state detection


How to Run
The game can be run using the main.py file with various command-line arguments:

Ex:
-- python main.py -p1 alphaBetaAI -p2 monteCarloAI

Command Line Options:
  -w: Number of rows (default: 6)
  
  -l: Number of columns (default: 7)
  
  -p1: Player 1 agent type
  
  -p2: Player 2 agent type
  
  -seed: Random seed for reproducibility
  
  -visualize: Enable/disable GUI
  
  -verbose: Print board states to console
  
  -time_limit: Set time limits for players


Player Types Available:
-- humanGUI: Human player with GUI interface

-- humanConsole: Human player with console interface

-- stupidAI: Simple deterministic AI

-- randomAI: Random move selection

-- monteCarloAI: Monte Carlo Tree Search implementation

-- minimaxAI: Minimax algorithm implementation (Produced by Cyrus)

-- alphaBetaAI: Alpha-beta pruning implementation (Produced by Cyrus)

Performance
The alpha-beta implementation consistently outperforms the Monte Carlo algorithm, winning roughly 17 out of 20 games, with almost every move being made in under 3 seconds on CSIF UC Davis computers.
This demonstrates the effectiveness and efficiency of the pruning technique and the strategic evaluation functions implemented.

Requirements
-- Python 3.x

-- NumPy

-- Pygame (for visualization)

Acknowledgments
This project was completed as part of an AI course at UC Davis, focusing on adversarial search algorithms and their application to game playing. The only file edited by me was player.py, specifically the minimaxAI() and alphaBetaAI() functions.
