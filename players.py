import random
import pygame
import math
from connect4 import connect4
import sys
import time

class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move_dict: dict) -> None:
		move_dict["move"] = -1

class humanConsole(connect4Player):
	'''
	Human player where input is collected from the console
	'''
	def play(self, env: connect4, move_dict: dict) -> None:
		move_dict['move'] = int(input('Select next move: '))
		while True:
			if int(move_dict['move']) >= 0 and int(move_dict['move']) <= 6 and env.topPosition[int(move_dict['move'])] >= 0:
				break
			move_dict['move'] = int(input('Index invalid. Select next move: '))

class humanGUI(connect4Player):
	'''
	Human player where input is collected from the GUI
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move_dict['move'] = col
					done = True

class randomAI(connect4Player):
	'''
	connect4Player that elects a random playable column as its move
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move_dict['move'] = random.choice(indices)

class stupidAI(connect4Player):
	'''
	connect4Player that will play the same strategy every time
	Tries to fill specific columns in a specific order 
	'''
	def play(self, env: connect4, move_dict: dict) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move_dict['move'] = 3
		elif 2 in indices:
			move_dict['move'] = 2
		elif 1 in indices:
			move_dict['move'] = 1
		elif 5 in indices:
			move_dict['move'] = 5
		elif 6 in indices:
			move_dict['move'] = 6
		else:
			move_dict['move'] = 0

class minimaxAI(connect4Player):
    '''
    A Connect 4 player that uses the minimax algorithm without alpha-beta pruning
    for the C4RC tournament. Complies with all tournament rules:
    - No multithreading
    - No saved state between turns
    - Only first move can be hardcoded
    - Must complete moves within 3 seconds on CSIF computers
    '''
    
    def __init__(self, position, seed=0, CVDMode=False):
        super().__init__(position, seed, CVDMode)
        # Set a conservative depth limit to ensure we stay within 3 second limit
        # Less than the alpha-beta version as it this is a slower algorithm
        self.max_depth = 4
        # Track if this is our first move
        self.is_first_move = True
    
    def play(self, env: connect4, move_dict: dict) -> None:
        # Hardcoding the first move to be the center column as it is mathematically the bset move
        if self.is_first_move and env.topPosition[3] >= 0:
            move_dict["move"] = 3
            self.is_first_move = False
            return
        
        self.is_first_move = False
        valid_moves = [col for col in range(7) if env.topPosition[col] >= 0]
        
        # Find best move using minimax
        best_score = float('-inf')
        best_move = valid_moves[0]
        
        for move in valid_moves:
            # Try this move
            env.board[env.topPosition[move]][move] = self.position
            env.topPosition[move] -= 1
            
            # Get score for this move
            score = self.minimax(env, self.max_depth - 1, False)
            
            # Undo the move
            env.topPosition[move] += 1
            env.board[env.topPosition[move]][move] = 0
            
            if score > best_score:
                best_score = score
                best_move = move
        
        move_dict["move"] = best_move
    
    def minimax(self, env: connect4, depth: int, max_player: bool) -> float:
        """
        Implementation of the minimax algorithm.
        """
        # Check terminal states first for efficiency
        winner = env.gameOver()
        if winner == self.position:
            return 100000.0  # took a W
        elif winner == self.opponent.position:
            return -100000.0  # took an L
        elif winner == -1:
            return 0.0  # welp
        elif depth == 0:
            return self.evaluate_position(env)
        
        valid_moves = [col for col in range(7) if env.topPosition[col] >= 0]
        
        if max_player:
            max_score = float('-inf')
            for move in valid_moves:
                # Try move
                env.board[env.topPosition[move]][move] = self.position
                env.topPosition[move] -= 1
                
                score = self.minimax(env, depth - 1, False)
                
                # Undo move
                env.topPosition[move] += 1
                env.board[env.topPosition[move]][move] = 0
                
                max_score = max(max_score, score)
            return max_score
        
        else:
            min_score = float('inf')
            for move in valid_moves:
                # Try move
                env.board[env.topPosition[move]][move] = self.opponent.position
                env.topPosition[move] -= 1
                
                score = self.minimax(env, depth - 1, True)
                
                # Undo move
                env.topPosition[move] += 1
                env.board[env.topPosition[move]][move] = 0
                
                min_score = min(min_score, score)
            return min_score
    
    def evaluate_position(self, env: connect4) -> float:
        """
        Evaluates the current board position using pattern matching and piece counting.
        Optimized for efficiency while maintaining good strategic evaluation.
        """
        score = 0.0
        
        # Evaluate all possible winning windows (horizontal, vertical, diagonal)
        # Horizontal
        for row in range(6):
            for col in range(4):
                window = [env.board[row][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Vertical
        for row in range(3):
            for col in range(7):
                window = [env.board[row+i][col] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Right diagonal
        for row in range(3):
            for col in range(4):
                window = [env.board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Left diagonal
        for row in range(3, 6):
            for col in range(4):
                window = [env.board[row-i][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Incentivize center control
        center_ct = sum(1 for row in range(6) if env.board[row][3] == self.position)
        score += center_ct * 3.0
        
        return score
    
    def evaluate_window(self, window: list) -> float:
        """
        Evaluates a window of 4 positions.
        Uses integer counting for efficiency.
        """
        score = 0.0
        player_ct = sum(1 for x in window if x == self.position)
        opponent_ct = sum(1 for x in window if x == self.opponent.position)
        empty_ct = sum(1 for x in window if x == 0)
        
        # Winning patterns
        if player_ct == 4:
            score += 1000.0
        elif player_ct == 3 and empty_ct == 1:
            score += 5.0
        elif player_ct == 2 and empty_ct == 2:
            score += 2.0
        
        # Defensive patterns
        if opponent_ct == 3 and empty_ct == 1:
            score -= 4.0
        
        return score
		

class alphaBetaAI(connect4Player):
    def __init__(self, position, seed=0, CVDMode=False):
        super().__init__(position, seed, CVDMode)
        self.max_depth = 5 # a value of 5 seems to be the sweet spot for performance vs accuracy
        self.is_first_move = True
        self.transposition_table = {}

        self.all_windows = self._precomp_windows()
        
    # by precomputing windows we are able to be more efficient at each stage of decision making
    def _precomp_windows(self):
        windows = []

        # Horizontal checks
        for row in range(6):
            for col in range(4):
                windows.append([(row, col+i) for i in range(4)])
        # Vertical checks
        for row in range(3):
            for col in range(7):
                windows.append([(row+i, col) for i in range(4)])
        # Right diagonal checks
        for row in range(3):
            for col in range(4):
                windows.append([(row+i, col+i) for i in range(4)])
        # Left diagonal checks
        for row in range(3, 6):
            for col in range(4):
                windows.append([(row-i, col+i) for i in range(4)])
        return windows

    def alpha_beta(self, env, depth, alpha, beta, max_player, last_move_row, last_move_col):
        """Optimized alpha-beta implementation"""
        # Quick terminal state check
        if max_player and env.gameOver(last_move_col, self.opponent.position):
            return -100000.0
        if not max_player and env.gameOver(last_move_col, self.position):
            return 100000.0

        # Check transposition table
        board_hash = hash(str(env.board))
        cache_key = (board_hash, depth, maximizing_player)
        if cache_key in self.transposition_table:
            return self.transposition_table[cache_key]

        if depth == 0:
            eval_score = self.quick_eval(env)
            self.transposition_table[cache_key] = eval_score
            return eval_score

        # Early draw detection
        if all(pos < 0 for pos in env.topPosition):
            return 0.0

        # Optimized move ordering
        moves = self._get_order(env)
        
        if max_player:
            max_score = float('-inf')
            for move in moves:
                row = env.topPosition[move]
                # Quick move/undo using array operations
                env.board[row][move] = self.position
                env.topPosition[move] -= 1
                
                score = self.alpha_beta(env, depth - 1, alpha, beta, False, row, move)
                
                env.topPosition[move] += 1
                env.board[row][move] = 0
                
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            self.transposition_table[cache_key] = max_score
            return max_score
        else:
            min_score = float('inf')
            for move in moves:
                row = env.topPosition[move]
                env.board[row][move] = self.opponent.position
                env.topPosition[move] -= 1
                
                score = self.alpha_beta(env, depth - 1, alpha, beta, True, row, move)
                
                env.topPosition[move] += 1
                env.board[row][move] = 0
                
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            self.transposition_table[cache_key] = min_score
            return min_score

    def _get_order(self, env):
        """Returns moves in an optimized order based on position"""
        moves = []

        # Prioritize center and near-center columns
        # row 3 (middle row) is the most important
        # columns 2 and 4 are the next most important, so on so forth
        for col in [3, 2, 4, 1, 5, 0, 6]:
            if env.topPosition[col] >= 0:
                # Check if move creates/blocks immediate threat
                row = env.topPosition[col]
                env.board[row][col] = self.position
                if env.gameOver(col, self.position):
                    env.board[row][col] = 0
                    return [col]  # return on winning move
                env.board[row][col] = self.opponent.position
                if env.gameOver(col, self.opponent.position):
                    env.board[row][col] = 0
                    moves.insert(0, col)  # block opponent otherwise loss
                    continue
                env.board[row][col] = 0
                moves.append(col)
        return moves

    def quick_eval(self, env):
        """Faster board evaluation"""
        score = 0.0
        
        # Center control (high priority)
        center_count = sum(1 for row in range(6) if env.board[row][3] == self.position)
        score += center_count * 3.0
        
        # Run through pre-computed windows
        for win_coords in self.all_windows:
            window = [env.board[r][c] for r, c in win_coords]
            
            # Count pieces in window
            player_ct = window.count(self.position)
            opp_ct = window.count(self.opponent.position)
            empty_ct = window.count(0)
            
            # Quick pattern matching
            if player_ct == 4:
                return 100000.0  # Winning position, large value or infinity
            elif opp_ct == 4:
                return -100000.0  # Lost position, large negative value or negative infinity
            elif player_ct == 3 and empty_ct == 1:
                score += 5.0  # Potential win, small positive value
            elif opp_ct == 3 and empty_ct == 1:
                score -= 4.0  # Must block, small negative value
            elif player_ct == 2 and empty_ct == 2:
                score += 2.0  # Building threat, small positive value
                
        return score            



# Defining Constants
SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




