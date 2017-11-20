import sys
import random
import time
import pygame
import pygame.locals

INFINITY = 1000000
SMALL_INIFINITY = 1000
MINIMAX_DEPTH = 7
ALPHA_0 = -INFINITY
BETA_0 = INFINITY
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOARDWIDTH = 350
BOARDHEIGHT = 350
X_MARGIN = (WINDOWWIDTH - BOARDWIDTH) / 2
Y_MARGIN = (WINDOWHEIGHT - BOARDHEIGHT) / 2
SQUARE_SIZE = BOARDWIDTH / 7
DISC_RADIUS = int(SQUARE_SIZE * 0.4)
TEXT_SIZE = 40
TEXT_SIZE_FIRST_MOVE = 22
TEXT_SIZE_PLAY_AGAIN = int(SQUARE_SIZE * 0.5)
TEXT_SIZE_GAME_RESULT = int(SQUARE_SIZE * 0.75)

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (250, 10, 10)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (250, 250, 10)
#BACKGROUND_COLOR = (0, 255, 150)
BACKGROUND_COLOR = (100, 100, 100)
BOARD_COLOR = (60, 60, 250)




class Game_window:

	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
		pygame.display.set_caption("Four in a row")		



class Bot:
	def __init__(self):
		self.timebank = None
		self.time_per_move = None
		self.player_names = None
		self.bot_name = None
		self.bot_id = None
		self.color = None		
		self.num_cols = 7
		self.num_rows = 6
		self.round = None
		self.board = [["0"] * self.num_cols for i in range(self.num_rows)]
		self.window = Game_window()
		self.is_finished = False
		self.move_number = 0
		self.play_again = True



	def store_settings(self, msg):
		self.timebank = int(msg[2])
		#print("set timebank to {}, type: {}".format(self.timebank, type(self.timebank)))
		self.time_per_move = int(sys.stdin.readline().strip().split(" ")[2])
		#print("set time_per_move to {}".format(self.time_per_move))
		self.player_names = sys.stdin.readline().strip().split(" ")[2]
		#print("set player_names to {}".format(self.player_names))
		self.bot_name = sys.stdin.readline().strip().split(" ")[2]
		#print("set bot_name to {}".format(self.bot_name))
		self.bot_id = sys.stdin.readline().strip().split(" ")[2]
		if (self.bot_id == "1"): self.color = 1
		else: self.color = -1
		#print("set bot_id to {}".format(self.bot_id))
		self.num_cols = int(sys.stdin.readline().strip().split(" ")[2])
		#print("set num_cols to {}".format(self.num_cols))
		self.num_rows = int(sys.stdin.readline().strip().split(" ")[2])
		#print("set num_rows to {}".format(self.num_rows))
		self.board = [[0] * self.num_cols for i in range(self.num_rows)]
		#self.board = [[0] * self.num_cols for i in range(self.num_rows)]
		#print("initial board state: {}".format(self.board))

	def update(self, msg):
		if (msg[2] == "round"):
			#self.board = [[0] * self.num_cols for i in range(self.num_rows)]
			# print("initial board state: {}".format(self.board))
			self.round = int(msg[3])
		elif (msg[2] == "field"):
			#print("set round number to {}".format(self.round))
			#a = (sys.stdin.readline().split(" "))[3].split(";")
			a = msg[3].split(";")
			#print("a = {}".format(a))
			for i in range(self.num_rows):
				b = a[i].split(",")
				for j in range(self.num_cols):
					self.board[i][j] = b[j]
		#print("elem: {}, type: {}".format(self.board[0][0], type(self.board[0][0])))
			#print("updated board state: {}".format(self.board))

	def eval_board(self, l_color):
		# the higher is returned score, the better for the first player
		num_threats_first = 0
		num_threats_second = 0


		# check for bottom_left -> top_right diagonal threats
		if (self.board[3][0] == self.board[2][1] == self.board[1][2] == '1' and self.board[0][3] == '0'):    num_threats_first += 1
		if (self.board[3][0] == '0' and self.board[2][1] == self.board[1][2] == self.board[0][3] == '1'):    num_threats_first += 1
		if (self.board[3][0] == self.board[1][2] == self.board[0][3] == '1' and self.board[2][1] == '0'):    num_threats_first += 1
		if (self.board[3][0] == self.board[2][1] == self.board[0][3] == '1' and self.board[1][2] == '0'):    num_threats_first += 1
		if (self.board[3][0] == self.board[2][1] == self.board[1][2] == '2' and self.board[0][3] == '0'): num_threats_second += 1
		if (self.board[3][0] == '0' and self.board[2][1] == self.board[1][2] == self.board[0][3] == '2'): num_threats_second += 1
		if (self.board[3][0] == self.board[1][2] == self.board[0][3] == '2' and self.board[2][1] == '0'): num_threats_second += 1
		if (self.board[3][0] == self.board[2][1] == self.board[0][3] == '2' and self.board[1][2] == '0'): num_threats_second += 1

		if (self.board[4][0] == self.board[3][1] == self.board[2][2] == '1' and self.board[1][3] == '0'):    num_threats_first += 1
		if (self.board[4][0] == '0' and self.board[3][1] == self.board[2][2] == self.board[1][3] == '1'):    num_threats_first += 1
		if (self.board[4][0] == self.board[2][2] == self.board[1][3] == '1' and self.board[3][1] == '0'):    num_threats_first += 1
		if (self.board[4][0] == self.board[3][1] == self.board[1][3] == '1' and self.board[2][2] == '0'):    num_threats_first += 1
		if (self.board[4][0] == self.board[3][1] == self.board[2][2] == '2' and self.board[1][3] == '0'): num_threats_second += 1
		if (self.board[4][0] == '0' and self.board[3][1] == self.board[2][2] == self.board[1][3] == '2'): num_threats_second += 1
		if (self.board[4][0] == self.board[2][2] == self.board[1][3] == '2' and self.board[3][1] == '0'): num_threats_second += 1
		if (self.board[4][0] == self.board[3][1] == self.board[1][3] == '2' and self.board[2][2] == '0'): num_threats_second += 1

		if (self.board[3][1] == self.board[2][2] == self.board[1][3] == '1' and self.board[0][4] == '0'):    num_threats_first += 1
		if (self.board[3][1] == '0' and self.board[2][2] == self.board[1][3] == self.board[0][4] == '1'):    num_threats_first += 1
		if (self.board[3][1] == self.board[1][3] == self.board[0][4] == '1' and self.board[2][2] == '0'):    num_threats_first += 1
		if (self.board[3][1] == self.board[2][2] == self.board[0][4] == '1' and self.board[1][3] == '0'):    num_threats_first += 1
		if (self.board[3][1] == self.board[2][2] == self.board[1][3] == '2' and self.board[0][4] == '0'): num_threats_second += 1
		if (self.board[3][1] == '0' and self.board[2][2] == self.board[1][3] == self.board[0][4] == '2'): num_threats_second += 1
		if (self.board[3][1] == self.board[1][3] == self.board[0][4] == '2' and self.board[2][2] == '0'): num_threats_second += 1
		if (self.board[3][1] == self.board[2][2] == self.board[0][4] == '2' and self.board[1][3] == '0'): num_threats_second += 1

		if (self.board[5][0] == self.board[4][1] == self.board[3][2] == '1' and self.board[2][3] == '0'): num_threats_first += 1
		if (self.board[5][0] == '0' and self.board[4][1] == self.board[3][2] == self.board[2][3] == '1'): num_threats_first += 1
		if (self.board[5][0] == self.board[4][1] == self.board[2][3] == '1' and self.board[3][2] == '0'): num_threats_first += 1
		if (self.board[5][0] == self.board[3][2] == self.board[2][3] == '1' and self.board[4][1] == '0'): num_threats_first += 1
		if (self.board[5][0] == self.board[4][1] == self.board[3][2] == '2' and self.board[2][3] == '0'): num_threats_second += 1
		if (self.board[5][0] == '0' and self.board[4][1] == self.board[3][2] == self.board[2][3] == '2'): num_threats_second += 1
		if (self.board[5][0] == self.board[4][1] == self.board[2][3] == '2' and self.board[3][2] == '0'): num_threats_second += 1
		if (self.board[5][0] == self.board[3][2] == self.board[2][3] == '2' and self.board[4][1] == '0'): num_threats_second += 1

		if (self.board[4][1] == self.board[3][2] == self.board[2][3] == '1' and self.board[1][4] == '0'): num_threats_first += 1
		if (self.board[4][1] == '0' and self.board[3][2] == self.board[2][3] == self.board[1][4] == '1'): num_threats_first += 1
		if (self.board[4][1] == self.board[2][3] == self.board[1][4] == '1' and self.board[3][2] == '0'): num_threats_first += 1
		if (self.board[4][1] == self.board[3][2] == self.board[1][4] == '1' and self.board[2][3] == '0'): num_threats_first += 1
		if (self.board[4][1] == self.board[3][2] == self.board[2][3] == '2' and self.board[1][4] == '0'): num_threats_second += 1
		if (self.board[4][1] == '0' and self.board[3][2] == self.board[2][3] == self.board[1][4] == '2'): num_threats_second += 1
		if (self.board[4][1] == self.board[2][3] == self.board[1][4] == '2' and self.board[3][2] == '0'): num_threats_second += 1
		if (self.board[4][1] == self.board[3][2] == self.board[1][4] == '2' and self.board[2][3] == '0'): num_threats_second += 1

		if (self.board[3][2] == self.board[2][3] == self.board[1][4] == '1' and self.board[0][5] == '0'): num_threats_first += 1
		if (self.board[3][2] == '0' and self.board[2][3] == self.board[1][4] == self.board[0][5] == '1'): num_threats_first += 1
		if (self.board[3][2] == self.board[1][4] == self.board[0][5] == '1' and self.board[2][3] == '0'): num_threats_first += 1
		if (self.board[3][2] == self.board[2][3] == self.board[0][5] == '1' and self.board[1][4] == '0'): num_threats_first += 1
		if (self.board[3][2] == self.board[2][3] == self.board[1][4] == '2' and self.board[0][5] == '0'): num_threats_second += 1
		if (self.board[3][2] == '0' and self.board[2][3] == self.board[1][4] == self.board[0][5] == '2'): num_threats_second += 1
		if (self.board[3][2] == self.board[1][4] == self.board[0][5] == '2' and self.board[2][3] == '0'): num_threats_second += 1
		if (self.board[3][2] == self.board[2][3] == self.board[0][5] == '2' and self.board[1][4] == '0'): num_threats_second += 1

		if (self.board[5][1] == self.board[4][2] == self.board[3][3] == '1' and self.board[2][4] == '0'): num_threats_first += 1
		if (self.board[5][1] == '0' and self.board[4][2] == self.board[3][3] == self.board[2][4] == '1'): num_threats_first += 1
		if (self.board[5][1] == self.board[3][3] == self.board[2][4] == '1' and self.board[4][2] == '0'): num_threats_first += 1
		if (self.board[5][1] == self.board[4][2] == self.board[2][4] == '1' and self.board[3][3] == '0'): num_threats_first += 1
		if (self.board[5][1] == self.board[4][2] == self.board[3][3] == '2' and self.board[2][4] == '0'): num_threats_second += 1
		if (self.board[5][1] == '0' and self.board[4][2] == self.board[3][3] == self.board[2][4] == '2'): num_threats_second += 1
		if (self.board[5][1] == self.board[3][3] == self.board[2][4] == '2' and self.board[4][2] == '0'): num_threats_second += 1
		if (self.board[5][1] == self.board[4][2] == self.board[2][4] == '2' and self.board[3][3] == '0'): num_threats_second += 1

		if (self.board[4][2] == self.board[3][3] == self.board[2][4] == '1' and self.board[1][5] == '0'): num_threats_first += 1
		if (self.board[4][2] == '0' and self.board[3][3] == self.board[2][4] == self.board[1][5] == '1'): num_threats_first += 1
		if (self.board[4][2] == self.board[2][4] == self.board[1][5] == '1' and self.board[3][3] == '0'): num_threats_first += 1
		if (self.board[4][2] == self.board[3][3] == self.board[1][5] == '1' and self.board[2][4] == '0'): num_threats_first += 1
		if (self.board[4][2] == self.board[3][3] == self.board[2][4] == '2' and self.board[1][5] == '0'): num_threats_second += 1
		if (self.board[4][2] == '0' and self.board[3][3] == self.board[2][4] == self.board[1][5] == '2'): num_threats_second += 1
		if (self.board[4][2] == self.board[2][4] == self.board[1][5] == '2' and self.board[3][3] == '0'): num_threats_second += 1
		if (self.board[4][2] == self.board[3][3] == self.board[1][5] == '2' and self.board[2][4] == '0'): num_threats_second += 1

		if (self.board[3][3] == self.board[2][4] == self.board[1][5] == '1' and self.board[0][6] == '0'): num_threats_first += 1
		if (self.board[3][3] == '0' and self.board[2][4] == self.board[1][5] == self.board[0][6] == '1'): num_threats_first += 1
		if (self.board[3][3] == self.board[1][5] == self.board[0][6] == '1' and self.board[2][4] == '0'): num_threats_first += 1
		if (self.board[3][3] == self.board[2][4] == self.board[0][6] == '1' and self.board[1][5] == '0'): num_threats_first += 1
		if (self.board[3][3] == self.board[2][4] == self.board[1][5] == '2' and self.board[0][6] == '0'): num_threats_second += 1
		if (self.board[3][3] == '0' and self.board[2][4] == self.board[1][5] == self.board[0][6] == '2'): num_threats_second += 1
		if (self.board[3][3] == self.board[1][5] == self.board[0][6] == '2' and self.board[2][4] == '0'): num_threats_second += 1
		if (self.board[3][3] == self.board[2][4] == self.board[0][6] == '2' and self.board[1][5] == '0'): num_threats_second += 1

		if (self.board[5][2] == self.board[4][3] == self.board[3][4] == '1' and self.board[2][5] == '0'): num_threats_first += 1
		if (self.board[5][2] == '0' and self.board[4][3] == self.board[3][4] == self.board[2][5] == '1'): num_threats_first += 1
		if (self.board[5][2] == self.board[3][4] == self.board[2][5] == '1' and self.board[4][3] == '0'): num_threats_first += 1
		if (self.board[5][2] == self.board[4][3] == self.board[2][5] == '1' and self.board[3][4] == '0'): num_threats_first += 1
		if (self.board[5][2] == self.board[4][3] == self.board[3][4] == '2' and self.board[2][5] == '0'): num_threats_second += 1
		if (self.board[5][2] == '0' and self.board[4][3] == self.board[3][4] == self.board[2][5] == '2'): num_threats_second += 1
		if (self.board[5][2] == self.board[3][4] == self.board[2][5] == '2' and self.board[4][3] == '0'): num_threats_second += 1
		if (self.board[5][2] == self.board[4][3] == self.board[2][5] == '2' and self.board[3][4] == '0'): num_threats_second += 1

		if (self.board[4][3] == self.board[3][4] == self.board[2][5] == '1' and self.board[1][6] == '0'): num_threats_first += 1
		if (self.board[4][3] == '0' and self.board[3][4] == self.board[2][5] == self.board[1][6] == '1'): num_threats_first += 1
		if (self.board[4][3] == self.board[2][5] == self.board[1][6] == '1' and self.board[3][4] == '0'): num_threats_first += 1
		if (self.board[4][3] == self.board[3][4] == self.board[1][6] == '1' and self.board[2][5] == '0'): num_threats_first += 1
		if (self.board[4][3] == self.board[3][4] == self.board[2][5] == '2' and self.board[1][6] == '0'): num_threats_second += 1
		if (self.board[4][3] == '0' and self.board[3][4] == self.board[2][5] == self.board[1][6] == '2'): num_threats_second += 1
		if (self.board[4][3] == self.board[2][5] == self.board[1][6] == '2' and self.board[3][4] == '0'): num_threats_second += 1
		if (self.board[4][3] == self.board[3][4] == self.board[1][6] == '2' and self.board[2][5] == '0'): num_threats_second += 1

		if (self.board[5][3] == self.board[4][4] == self.board[3][5] == '1' and self.board[2][6] == '0'): num_threats_first += 1
		if (self.board[5][3] == '0' and self.board[4][4] == self.board[3][5] == self.board[2][6] == '1'): num_threats_first += 1
		if (self.board[5][3] == self.board[3][5] == self.board[2][6] == '1' and self.board[4][4] == '0'): num_threats_first += 1
		if (self.board[5][3] == self.board[4][4] == self.board[2][6] == '1' and self.board[3][5] == '0'): num_threats_first += 1
		if (self.board[5][3] == self.board[4][4] == self.board[3][5] == '2' and self.board[2][6] == '0'): num_threats_second += 1
		if (self.board[5][3] == '0' and self.board[4][4] == self.board[3][5] == self.board[2][6] == '2'): num_threats_second += 1
		if (self.board[5][3] == self.board[3][5] == self.board[2][6] == '2' and self.board[4][4] == '0'): num_threats_second += 1
		if (self.board[5][3] == self.board[4][4] == self.board[2][6] == '2' and self.board[3][5] == '0'): num_threats_second += 1





		# check for bottom_right -> top_left diagonal threats
		if (self.board[2][0] == self.board[3][1] == self.board[4][2] == '1' and self.board[5][3] == '0'):    num_threats_first += 1
		if (self.board[2][0] == '0' and self.board[3][1] == self.board[4][2] == self.board[5][3] == '1'):    num_threats_first += 1
		if (self.board[2][0] == self.board[4][2] == self.board[5][3] == '1' and self.board[3][1] == '0'):    num_threats_first += 1
		if (self.board[2][0] == self.board[3][1] == self.board[5][3] == '1' and self.board[4][2] == '0'):    num_threats_first += 1
		if (self.board[2][0] == self.board[3][1] == self.board[4][2] == '2' and self.board[5][3] == '0'): num_threats_second += 1
		if (self.board[2][0] == '0' and self.board[3][1] == self.board[4][2] == self.board[5][3] == '2'): num_threats_second += 1
		if (self.board[2][0] == self.board[4][2] == self.board[5][3] == '2' and self.board[3][1] == '0'): num_threats_second += 1
		if (self.board[2][0] == self.board[3][1] == self.board[5][3] == '2' and self.board[4][2] == '0'): num_threats_second += 1

		if (self.board[1][0] == self.board[2][1] == self.board[3][2] == '1' and self.board[4][3] == '0'):    num_threats_first += 1
		if (self.board[1][0] == '0' and self.board[2][1] == self.board[3][2] == self.board[4][3] == '1'):    num_threats_first += 1
		if (self.board[1][0] == self.board[3][2] == self.board[4][3] == '1' and self.board[2][1] == '0'):    num_threats_first += 1
		if (self.board[1][0] == self.board[2][1] == self.board[4][3] == '1' and self.board[3][2] == '0'):    num_threats_first += 1
		if (self.board[1][0] == self.board[2][1] == self.board[3][2] == '2' and self.board[4][3] == '0'): num_threats_second += 1
		if (self.board[1][0] == '0' and self.board[2][1] == self.board[3][2] == self.board[4][3] == '2'): num_threats_second += 1
		if (self.board[1][0] == self.board[3][2] == self.board[4][3] == '2' and self.board[2][1] == '0'): num_threats_second += 1
		if (self.board[1][0] == self.board[2][1] == self.board[4][3] == '2' and self.board[3][2] == '0'): num_threats_second += 1

		if (self.board[2][1] == self.board[3][2] == self.board[4][3] == '1' and self.board[5][4] == '0'):    num_threats_first += 1
		if (self.board[2][1] == '0' and self.board[3][2] == self.board[4][3] == self.board[5][4] == '1'):    num_threats_first += 1
		if (self.board[2][1] == self.board[4][3] == self.board[5][4] == '1' and self.board[3][2] == '0'):    num_threats_first += 1
		if (self.board[2][1] == self.board[3][2] == self.board[5][4] == '1' and self.board[4][3] == '0'):    num_threats_first += 1
		if (self.board[2][1] == self.board[3][2] == self.board[4][3] == '2' and self.board[5][4] == '0'): num_threats_second += 1
		if (self.board[2][1] == '0' and self.board[3][2] == self.board[4][3] == self.board[5][4] == '2'): num_threats_second += 1
		if (self.board[2][1] == self.board[4][3] == self.board[5][4] == '2' and self.board[3][2] == '0'): num_threats_second += 1
		if (self.board[2][1] == self.board[3][2] == self.board[5][4] == '2' and self.board[4][3] == '0'): num_threats_second += 1

		if (self.board[0][0] == self.board[1][1] == self.board[2][2] == '1' and self.board[3][3] == '0'): num_threats_first += 1
		if (self.board[0][0] == '0' and self.board[1][1] == self.board[2][2] == self.board[3][3] == '1'): num_threats_first += 1
		if (self.board[0][0] == self.board[2][2] == self.board[3][3] == '1' and self.board[1][1] == '0'): num_threats_first += 1
		if (self.board[0][0] == self.board[1][1] == self.board[3][3] == '1' and self.board[2][2] == '0'): num_threats_first += 1
		if (self.board[0][0] == self.board[1][1] == self.board[2][2] == '2' and self.board[3][3] == '0'): num_threats_second += 1
		if (self.board[0][0] == '0' and self.board[1][1] == self.board[2][2] == self.board[3][3] == '2'): num_threats_second += 1
		if (self.board[0][0] == self.board[2][2] == self.board[3][3] == '2' and self.board[1][1] == '0'): num_threats_second += 1
		if (self.board[0][0] == self.board[1][1] == self.board[3][3] == '2' and self.board[2][2] == '0'): num_threats_second += 1

		if (self.board[1][1] == self.board[2][2] == self.board[3][3] == '1' and self.board[4][4] == '0'): num_threats_first += 1
		if (self.board[1][1] == '0' and self.board[2][2] == self.board[3][3] == self.board[4][4] == '1'): num_threats_first += 1
		if (self.board[1][1] == self.board[3][3] == self.board[4][4] == '1' and self.board[2][2] == '0'): num_threats_first += 1
		if (self.board[1][1] == self.board[2][2] == self.board[4][4] == '1' and self.board[3][3] == '0'): num_threats_first += 1
		if (self.board[1][1] == self.board[2][2] == self.board[3][3] == '2' and self.board[4][4] == '0'): num_threats_second += 1
		if (self.board[1][1] == '0' and self.board[2][2] == self.board[3][3] == self.board[4][4] == '2'): num_threats_second += 1
		if (self.board[1][1] == self.board[3][3] == self.board[4][4] == '2' and self.board[2][2] == '0'): num_threats_second += 1
		if (self.board[1][1] == self.board[2][2] == self.board[4][4] == '2' and self.board[3][3] == '0'): num_threats_second += 1

		if (self.board[2][2] == self.board[3][3] == self.board[4][4] == '1' and self.board[5][5] == '0'): num_threats_first += 1
		if (self.board[2][2] == '0' and self.board[3][3] == self.board[4][4] == self.board[5][5] == '1'): num_threats_first += 1
		if (self.board[2][2] == self.board[4][4] == self.board[5][5] == '1' and self.board[3][3] == '0'): num_threats_first += 1
		if (self.board[2][2] == self.board[3][3] == self.board[5][5] == '1' and self.board[4][4] == '0'): num_threats_first += 1
		if (self.board[2][2] == self.board[3][3] == self.board[4][4] == '2' and self.board[5][5] == '0'): num_threats_second += 1
		if (self.board[2][2] == '0' and self.board[3][3] == self.board[4][4] == self.board[5][5] == '2'): num_threats_second += 1
		if (self.board[2][2] == self.board[4][4] == self.board[5][5] == '2' and self.board[3][3] == '0'): num_threats_second += 1
		if (self.board[2][2] == self.board[3][3] == self.board[5][5] == '2' and self.board[4][4] == '0'): num_threats_second += 1

		if (self.board[0][1] == self.board[1][2] == self.board[2][3] == '1' and self.board[3][4] == '0'): num_threats_first += 1
		if (self.board[0][1] == '0' and self.board[1][2] == self.board[2][3] == self.board[3][4] == '1'): num_threats_first += 1
		if (self.board[0][1] == self.board[2][3] == self.board[3][4] == '1' and self.board[1][2] == '0'): num_threats_first += 1
		if (self.board[0][1] == self.board[1][2] == self.board[3][4] == '1' and self.board[2][3] == '0'): num_threats_first += 1
		if (self.board[0][1] == self.board[1][2] == self.board[2][3] == '2' and self.board[3][4] == '0'): num_threats_second += 1
		if (self.board[0][1] == '0' and self.board[1][2] == self.board[2][3] == self.board[3][4] == '2'): num_threats_second += 1
		if (self.board[0][1] == self.board[2][3] == self.board[3][4] == '2' and self.board[1][2] == '0'): num_threats_second += 1
		if (self.board[0][1] == self.board[1][2] == self.board[3][4] == '2' and self.board[2][3] == '0'): num_threats_second += 1

		if (self.board[1][2] == self.board[2][3] == self.board[3][4] == '1' and self.board[4][5] == '0'): num_threats_first += 1
		if (self.board[1][2] == '0' and self.board[2][3] == self.board[3][4] == self.board[4][5] == '1'): num_threats_first += 1
		if (self.board[1][2] == self.board[3][4] == self.board[4][5] == '1' and self.board[2][3] == '0'): num_threats_first += 1
		if (self.board[1][2] == self.board[2][3] == self.board[4][5] == '1' and self.board[3][4] == '0'): num_threats_first += 1
		if (self.board[1][2] == self.board[2][3] == self.board[3][4] == '2' and self.board[4][5] == '0'): num_threats_second += 1
		if (self.board[1][2] == '0' and self.board[2][3] == self.board[3][4] == self.board[4][5] == '2'): num_threats_second += 1
		if (self.board[1][2] == self.board[3][4] == self.board[4][5] == '2' and self.board[2][3] == '0'): num_threats_second += 1
		if (self.board[1][2] == self.board[2][3] == self.board[4][5] == '2' and self.board[3][4] == '0'): num_threats_second += 1

		if (self.board[2][3] == self.board[3][4] == self.board[4][5] == '1' and self.board[5][6] == '0'): num_threats_first += 1
		if (self.board[2][3] == '0' and self.board[3][4] == self.board[4][5] == self.board[5][6] == '1'): num_threats_first += 1
		if (self.board[2][3] == self.board[4][5] == self.board[5][6] == '1' and self.board[3][4] == '0'): num_threats_first += 1
		if (self.board[2][3] == self.board[3][4] == self.board[5][6] == '1' and self.board[4][5] == '0'): num_threats_first += 1
		if (self.board[2][3] == self.board[3][4] == self.board[4][5] == '2' and self.board[5][6] == '0'): num_threats_second += 1
		if (self.board[2][3] == '0' and self.board[3][4] == self.board[4][5] == self.board[5][6] == '2'): num_threats_second += 1
		if (self.board[2][3] == self.board[4][5] == self.board[5][6] == '2' and self.board[3][4] == '0'): num_threats_second += 1
		if (self.board[2][3] == self.board[3][4] == self.board[5][6] == '2' and self.board[4][5] == '0'): num_threats_second += 1

		if (self.board[0][2] == self.board[1][3] == self.board[2][4] == '1' and self.board[3][5] == '0'): num_threats_first += 1
		if (self.board[0][2] == '0' and self.board[1][3] == self.board[2][4] == self.board[3][5] == '1'): num_threats_first += 1
		if (self.board[0][2] == self.board[2][4] == self.board[3][5] == '1' and self.board[1][3] == '0'): num_threats_first += 1
		if (self.board[0][2] == self.board[1][3] == self.board[3][5] == '1' and self.board[2][4] == '0'): num_threats_first += 1
		if (self.board[0][2] == self.board[1][3] == self.board[2][4] == '2' and self.board[3][5] == '0'): num_threats_second += 1
		if (self.board[0][2] == '0' and self.board[1][3] == self.board[2][4] == self.board[3][5] == '2'): num_threats_second += 1
		if (self.board[0][2] == self.board[2][4] == self.board[3][5] == '2' and self.board[1][3] == '0'): num_threats_second += 1
		if (self.board[0][2] == self.board[1][3] == self.board[3][5] == '2' and self.board[2][4] == '0'): num_threats_second += 1

		if (self.board[1][3] == self.board[2][4] == self.board[3][5] == '1' and self.board[4][6] == '0'): num_threats_first += 1
		if (self.board[1][3] == '0' and self.board[2][4] == self.board[3][5] == self.board[4][6] == '1'): num_threats_first += 1
		if (self.board[1][3] == self.board[3][5] == self.board[4][6] == '1' and self.board[2][4] == '0'): num_threats_first += 1
		if (self.board[1][3] == self.board[2][4] == self.board[4][6] == '1' and self.board[3][5] == '0'): num_threats_first += 1
		if (self.board[1][3] == self.board[2][4] == self.board[3][5] == '2' and self.board[4][6] == '0'): num_threats_second += 1
		if (self.board[1][3] == '0' and self.board[2][4] == self.board[3][5] == self.board[4][6] == '2'): num_threats_second += 1
		if (self.board[1][3] == self.board[3][5] == self.board[4][6] == '2' and self.board[2][4] == '0'): num_threats_second += 1
		if (self.board[1][3] == self.board[2][4] == self.board[4][6] == '2' and self.board[3][5] == '0'): num_threats_second += 1

		if (self.board[0][3] == self.board[1][4] == self.board[2][5] == '1' and self.board[3][6] == '0'): num_threats_first += 1
		if (self.board[0][3] == '0' and self.board[1][4] == self.board[2][5] == self.board[3][6] == '1'): num_threats_first += 1
		if (self.board[0][3] == self.board[2][5] == self.board[3][6] == '1' and self.board[1][4] == '0'): num_threats_first += 1
		if (self.board[0][3] == self.board[1][4] == self.board[3][6] == '1' and self.board[2][5] == '0'): num_threats_first += 1
		if (self.board[0][3] == self.board[1][4] == self.board[2][5] == '2' and self.board[3][6] == '0'): num_threats_second += 1
		if (self.board[0][3] == '0' and self.board[1][4] == self.board[2][5] == self.board[3][6] == '2'): num_threats_second += 1
		if (self.board[0][3] == self.board[2][5] == self.board[3][6] == '2' and self.board[1][4] == '0'): num_threats_second += 1
		if (self.board[0][3] == self.board[1][4] == self.board[3][6] == '2' and self.board[2][5] == '0'): num_threats_second += 1

		for i in range(6):#check for horizontal threats

			if (self.board[i][1] == self.board[i][2] == self.board[i][3] == '1'):
				if (self.board[i][0] == '0'): num_threats_first += 1
				if (self.board[i][4] == '0'): num_threats_first += 1
			if (self.board[i][2] == self.board[i][3] == self.board[i][4] == '1'):
				if (self.board[i][1] == '0'): num_threats_first += 1
				if (self.board[i][5] == '0'): num_threats_first += 1
			if (self.board[i][3] == self.board[i][4] == self.board[i][5] == '1'):
				if (self.board[i][2] == '0'): num_threats_first += 1
				if (self.board[i][6] == '0'): num_threats_first += 1
			if (self.board[i][3] == '0'):
				if (self.board[i][4] == self.board[i][5] == self.board[i][6] == '1'): num_threats_first += 1
				if (self.board[i][0] == self.board[i][1] == self.board[i][2] == '1'): num_threats_first += 1
			if (self.board[i][0] == self.board[i][2] == self.board[i][3] == '1' and self.board[i][1] == '0'): num_threats_first += 1#*_** pattern
			if (self.board[i][1] == self.board[i][3] == self.board[i][4] == '1' and self.board[i][2] == '0'): num_threats_first += 1
			if (self.board[i][2] == self.board[i][4] == self.board[i][5] == '1' and self.board[i][3] == '0'): num_threats_first += 1
			if (self.board[i][3] == self.board[i][5] == self.board[i][6] == '1' and self.board[i][4] == '0'): num_threats_first += 1
			if (self.board[i][0] == self.board[i][1] == self.board[i][3] == '1' and self.board[i][2] == '0'): num_threats_first += 1#**_* pattern
			if (self.board[i][1] == self.board[i][2] == self.board[i][4] == '1' and self.board[i][3] == '0'): num_threats_first += 1
			if (self.board[i][2] == self.board[i][3] == self.board[i][5] == '1' and self.board[i][4] == '0'): num_threats_first += 1
			if (self.board[i][3] == self.board[i][4] == self.board[i][6] == '1' and self.board[i][5] == '0'): num_threats_first += 1

			if (self.board[i][1] == self.board[i][2] == self.board[i][3] == '2'):
				if (self.board[i][0] == '0'): num_threats_second += 1
				if (self.board[i][4] == '0'): num_threats_second += 1
			if (self.board[i][2] == self.board[i][3] == self.board[i][4] == '2'):
				if (self.board[i][1] == '0'): num_threats_second += 1
				if (self.board[i][5] == '0'): num_threats_second += 1
			if (self.board[i][3] == self.board[i][4] == self.board[i][5] == '2'):
				if (self.board[i][2] == '0'): num_threats_second += 1
				if (self.board[i][6] == '0'): num_threats_second += 1
			if (self.board[i][3] == '0'):
				if (self.board[i][4] == self.board[i][5] == self.board[i][6] == '2'): num_threats_second += 1
				if (self.board[i][0] == self.board[i][1] == self.board[i][2] == '2'): num_threats_second += 1
			if (self.board[i][0] == self.board[i][2] == self.board[i][3] == '2' and self.board[i][1] == '0'): num_threats_second += 1  # *_** pattern
			if (self.board[i][1] == self.board[i][3] == self.board[i][4] == '2' and self.board[i][2] == '0'): num_threats_second += 1
			if (self.board[i][2] == self.board[i][4] == self.board[i][5] == '2' and self.board[i][3] == '0'): num_threats_second += 1
			if (self.board[i][3] == self.board[i][5] == self.board[i][6] == '2' and self.board[i][4] == '0'): num_threats_second += 1
			if (self.board[i][0] == self.board[i][1] == self.board[i][3] == '2' and self.board[i][2] == '0'): num_threats_second += 1  # **_* pattern
			if (self.board[i][1] == self.board[i][2] == self.board[i][4] == '2' and self.board[i][3] == '0'): num_threats_second += 1
			if (self.board[i][2] == self.board[i][3] == self.board[i][5] == '2' and self.board[i][4] == '0'): num_threats_second += 1
			if (self.board[i][3] == self.board[i][4] == self.board[i][6] == '2' and self.board[i][5] == '0'): num_threats_second += 1

		for i in range(7):#check for vertical threats
			if (self.board[0][i] == self.board[1][i] == self.board[2][i] == '1' and self.board[3][i] == '0'): num_threats_first += 1
			if (self.board[1][i] == self.board[2][i] == self.board[3][i]) == '1':
				if (self.board[0][i] == '0'): num_threats_first += 1
				if (self.board[4][i] == '0'): num_threats_first += 1
			if (self.board[2][i] == self.board[3][i] == self.board[4][i]) == '1':
				if (self.board[1][i] == '0'): num_threats_first += 1
				if (self.board[5][i] == '0'): num_threats_first += 1
			if (self.board[3][i] == self.board[4][i] == self.board[5][i] == '1' and self.board[2][i] == '0'): num_threats_first += 1
			if (self.board[0][i] == self.board[2][i] == self.board[3][i] == '1' and self.board[1][i] == '0'): num_threats_first += 1
			if (self.board[1][i] == self.board[3][i] == self.board[4][i] == '1' and self.board[2][i] == '0'): num_threats_first += 1
			if (self.board[2][i] == self.board[4][i] == self.board[5][i] == '1' and self.board[3][i] == '0'): num_threats_first += 1
			if (self.board[0][i] == self.board[1][i] == self.board[3][i] == '1' and self.board[2][i] == '0'): num_threats_first += 1
			if (self.board[1][i] == self.board[2][i] == self.board[4][i] == '1' and self.board[3][i] == '0'): num_threats_first += 1
			if (self.board[2][i] == self.board[3][i] == self.board[5][i] == '1' and self.board[4][i] == '0'): num_threats_first += 1


			if (self.board[0][i] == self.board[1][i] == self.board[2][i] == '2' and self.board[3][i] == '0'): num_threats_second += 1
			if (self.board[1][i] == self.board[2][i] == self.board[3][i]) == '2':
				if (self.board[0][i] == '0'): num_threats_second += 1
				if (self.board[4][i] == '0'): num_threats_second += 1
			if (self.board[2][i] == self.board[3][i] == self.board[4][i]) == '2':
				if (self.board[1][i] == '0'): num_threats_second += 1
				if (self.board[5][i] == '0'): num_threats_second += 1
			if (self.board[3][i] == self.board[4][i] == self.board[5][i] == '2' and self.board[2][i] == '0'): num_threats_second += 1
			if (self.board[0][i] == self.board[2][i] == self.board[3][i] == '2' and self.board[1][i] == '0'): num_threats_second += 1
			if (self.board[1][i] == self.board[3][i] == self.board[4][i] == '2' and self.board[2][i] == '0'): num_threats_second += 1
			if (self.board[2][i] == self.board[4][i] == self.board[5][i] == '2' and self.board[3][i] == '0'): num_threats_second += 1
			if (self.board[0][i] == self.board[1][i] == self.board[3][i] == '2' and self.board[2][i] == '0'): num_threats_second += 1
			if (self.board[1][i] == self.board[2][i] == self.board[4][i] == '2' and self.board[3][i] == '0'): num_threats_second += 1
			if (self.board[2][i] == self.board[3][i] == self.board[5][i] == '2' and self.board[4][i] == '0'): num_threats_second += 1

		# print("returned score from valid moves: {}".format((my_count - opp_count)))
		# print("threats_first = {}, threats_second = {}.".format(num_threats_first, num_threats_second))
		return l_color * (num_threats_first - num_threats_second)

	def is_terminal_node(self, l_color):

		terminal_val = l_color * SMALL_INIFINITY

		for i in range(6):  # check for horizontal win/loss
			for j in range(4):
				if (self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] == '1'): return terminal_val
				if (self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] == '2'): return -terminal_val
		for j in range(7):  # check for vertical win/loss
			for i in range(3):
				if (self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] == '1'): return terminal_val
				if (self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] == '2'): return -terminal_val

		# check for bottom_left -> top_right diagonal win/loss
		if (self.board[3][0] == self.board[2][1] == self.board[1][2] == self.board[0][3] == '1'): return terminal_val
		if (self.board[3][0] == self.board[2][1] == self.board[1][2] == self.board[0][3] == '2'): return -terminal_val
		if (self.board[4][0] == self.board[3][1] == self.board[2][2] == self.board[1][3] == '1'): return terminal_val
		if (self.board[4][0] == self.board[3][1] == self.board[2][2] == self.board[1][3] == '2'): return -terminal_val
		if (self.board[3][1] == self.board[2][2] == self.board[1][3] == self.board[0][4] == '1'): return terminal_val
		if (self.board[3][1] == self.board[2][2] == self.board[1][3] == self.board[0][4] == '2'): return -terminal_val
		if (self.board[5][0] == self.board[4][1] == self.board[3][2] == self.board[2][3] == '1'): return terminal_val
		if (self.board[5][0] == self.board[4][1] == self.board[3][2] == self.board[2][3] == '2'): return -terminal_val
		if (self.board[4][1] == self.board[3][2] == self.board[2][3] == self.board[1][4] == '1'): return terminal_val
		if (self.board[4][1] == self.board[3][2] == self.board[2][3] == self.board[1][4] == '2'): return -terminal_val
		if (self.board[3][2] == self.board[2][3] == self.board[1][4] == self.board[0][5] == '1'): return terminal_val
		if (self.board[3][2] == self.board[2][3] == self.board[1][4] == self.board[0][5] == '2'): return -terminal_val
		if (self.board[5][1] == self.board[4][2] == self.board[3][3] == self.board[2][4] == '1'): return terminal_val
		if (self.board[5][1] == self.board[4][2] == self.board[3][3] == self.board[2][4] == '2'): return -terminal_val
		if (self.board[4][2] == self.board[3][3] == self.board[2][4] == self.board[1][5] == '1'): return terminal_val
		if (self.board[4][2] == self.board[3][3] == self.board[2][4] == self.board[1][5] == '2'): return -terminal_val
		if (self.board[3][3] == self.board[2][4] == self.board[1][5] == self.board[0][6] == '1'): return terminal_val
		if (self.board[3][3] == self.board[2][4] == self.board[1][5] == self.board[0][6] == '2'): return -terminal_val
		if (self.board[5][2] == self.board[4][3] == self.board[3][4] == self.board[2][5] == '1'): return terminal_val
		if (self.board[5][2] == self.board[4][3] == self.board[3][4] == self.board[2][5] == '2'): return -terminal_val
		if (self.board[4][3] == self.board[3][4] == self.board[2][5] == self.board[1][6] == '1'): return terminal_val
		if (self.board[4][3] == self.board[3][4] == self.board[2][5] == self.board[1][6] == '2'): return -terminal_val
		if (self.board[5][3] == self.board[4][4] == self.board[3][5] == self.board[2][6] == '1'): return terminal_val
		if (self.board[5][3] == self.board[4][4] == self.board[3][5] == self.board[2][6] == '2'): return -terminal_val


		# check for bottom_right -> top_left diagonal win/loss
		if (self.board[2][0] == self.board[3][1] == self.board[4][2] == self.board[5][3] == '1'): return terminal_val
		if (self.board[2][0] == self.board[3][1] == self.board[4][2] == self.board[5][3] == '2'): return -terminal_val
		if (self.board[1][0] == self.board[2][1] == self.board[3][2] == self.board[4][3] == '1'): return terminal_val
		if (self.board[1][0] == self.board[2][1] == self.board[3][2] == self.board[4][3] == '2'): return -terminal_val
		if (self.board[2][1] == self.board[3][2] == self.board[4][3] == self.board[5][4] == '1'): return terminal_val
		if (self.board[2][1] == self.board[3][2] == self.board[4][3] == self.board[5][4] == '2'): return -terminal_val
		if (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[3][3] == '1'): return terminal_val
		if (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[3][3] == '2'): return -terminal_val
		if (self.board[1][1] == self.board[2][2] == self.board[3][3] == self.board[4][4] == '1'): return terminal_val
		if (self.board[1][1] == self.board[2][2] == self.board[3][3] == self.board[4][4] == '2'): return -terminal_val
		if (self.board[2][2] == self.board[3][3] == self.board[4][4] == self.board[5][5] == '1'): return terminal_val
		if (self.board[2][2] == self.board[3][3] == self.board[4][4] == self.board[5][5] == '2'): return -terminal_val
		if (self.board[0][1] == self.board[1][2] == self.board[2][3] == self.board[3][4] == '1'): return terminal_val
		if (self.board[0][1] == self.board[1][2] == self.board[2][3] == self.board[3][4] == '2'): return -terminal_val
		if (self.board[1][2] == self.board[2][3] == self.board[3][4] == self.board[4][5] == '1'): return terminal_val
		if (self.board[1][2] == self.board[2][3] == self.board[3][4] == self.board[4][5] == '2'): return -terminal_val
		if (self.board[2][3] == self.board[3][4] == self.board[4][5] == self.board[5][6] == '1'): return terminal_val
		if (self.board[2][3] == self.board[3][4] == self.board[4][5] == self.board[5][6] == '2'): return -terminal_val
		if (self.board[0][2] == self.board[1][3] == self.board[2][4] == self.board[3][5] == '1'): return terminal_val
		if (self.board[0][2] == self.board[1][3] == self.board[2][4] == self.board[3][5] == '2'): return -terminal_val
		if (self.board[1][3] == self.board[2][4] == self.board[3][5] == self.board[4][6] == '1'): return terminal_val
		if (self.board[1][3] == self.board[2][4] == self.board[3][5] == self.board[4][6] == '2'): return -terminal_val
		if (self.board[0][3] == self.board[1][4] == self.board[2][5] == self.board[3][6] == '1'): return terminal_val
		if (self.board[0][3] == self.board[1][4] == self.board[2][5] == self.board[3][6] == '2'): return -terminal_val

		return 0#returns 0 in case the node is not terminal


	def make_move_on_board(self, move, l_color):
		#makes move in the column with number equal to move, returns number of row the tile was placed
		#print("entered make move with move = {}".format(move))
		if (l_color == 1): tile = "1"
		else: tile = "2"
		column = int(move)
		for i in range(6):
			if (self.board[5 - i][column] == "0"):
				self.board[5 - i][column] = tile
				return  5 - i

	def unmake_move(self, row, columm):
		self.board[row][columm] = "0"

	def get_valid_moves(self):
		#returns [of column numbers for valid moves
		#print("ENTERED GET_VALID_MOVES")
		#print("board in valid moves: {}".format(self.board))
		#print("type: {}".format(type(self.board[0][0])))
		#print("type: {}".format(type(self.board[3][3])))
		valid_moves = []
		for j in range(7):
			if (self.board[0][j] == '0'):
				valid_moves.append(str(j))
		#print("valid moves: {}".format(valid_moves))
		return valid_moves

	def negamax(self, l_color, depth, alpha, beta):
		#print("entered negamax with color = {}, depth = {}, alpha = {}, beta = {}".format(color, depth, alpha, beta))
		if (depth == 0): return  self.eval_board(l_color)
		is_terminal = self.is_terminal_node(l_color)
		if (is_terminal != 0):
			#print("IS TERMINAL!")
			return is_terminal
		possible_moves = self.get_valid_moves()
		#print("possible moves: {}".format(possible_moves))
		#random.shuffle(possible_moves)
		#possible_moves = self.order_moves(possible_moves, l_color)
		#print("possible moves: {}".format(possible_moves))
		if (len(possible_moves) == 0):
			#print("__________________________________EMPTY POSSIBLE MOVES________________________________________")
			return self.eval_board(l_color)
		for current_move in possible_moves:
			row = self.make_move_on_board(current_move, l_color)
			#print("made move {}".format(current_move))
			#print("current board: {}".format(self.board))
			new_score = -self.negamax(-l_color, depth - 1, -beta, -alpha)
			#print("returned with value {}".format(new_score))
			self.unmake_move(row, int(current_move))
			if (new_score >= beta): return beta
			if (new_score > alpha): alpha =  new_score
		return alpha

	def root_search_negamax(self, l_color, depth, alpha, beta):
		best_score = -INFINITY
		best_move = ""
		possible_moves = self.get_valid_moves()
		if (len(possible_moves) == 0):
			return self.eval_board(l_color)
		#random.shuffle(possible_moves)
		# possible_moves = self.order_moves(possible_moves, l_color)
		#print("AT ROOT current board: {}".format(self.board))
		for current_move in possible_moves:
			# print("board before move: {}".format(self.board))
			row = self.make_move_on_board(current_move, l_color)
			# print("board after move: {}".format(self.board))
			# print("entering negamax with color = {}, depth = {}, alpha = {}, beta = {}".format(-color, depth - 1, -beta, -alpha))
			new_score = -self.negamax(-l_color, depth - 1, -beta, -alpha)
			# print("board before unmake move: {}".format(self.board))
			self.unmake_move(row, int(current_move))
			# print("unmade move {} {}".format(row, int(current_move)))
			# print("board after unmake move: {}".format(self.board))
			if (new_score > alpha):
				alpha = new_score
				best_move = current_move
			if (new_score >= beta):
				break
		return best_move



	def pvs(self, l_color, depth, alpha, beta):
		#print("entered pvs with color = {}, depth = {}, alpha = {}, beta = {}".format(l_color, depth, alpha, beta))
		if (depth == 0): return self.eval_board(l_color)
		is_terminal = self.is_terminal_node(l_color)
		if (is_terminal != 0):
			# print("IS TERMINAL!")
			return is_terminal

		possible_moves = self.get_valid_moves()
		#print("possible moves: {}".format(possible_moves))
		#random.shuffle(possible_moves)
		#possible_moves = self.order_moves(possible_moves, l_color)
		# print("possible moves: {}".format(possible_moves))
		if (len(possible_moves) == 0):
			#print("__________________________________EMPTY POSSIBLE MOVES________________________________________")
			return self.eval_board(l_color)
		found_pv = False
		for current_move in possible_moves:
			row = self.make_move_on_board(current_move, l_color)
			#print("made move {}".format(current_move))
			# print("current board: {}".format(self.board))
			if (found_pv):
				new_score = -self.pvs(-l_color, depth - 1, -alpha - 1, -alpha)
				if (new_score > alpha and new_score < beta):
					new_score = -self.pvs(-l_color, depth - 1, -beta, -alpha)
			else: new_score = -self.pvs(-l_color, depth - 1, -beta, -alpha)
			#print("returned with value {}".format(new_score))
			self.unmake_move(row, int(current_move))
			if (new_score >= beta): return beta
			if (new_score > alpha):
				alpha = new_score
				found_pv = True
		return alpha

	def root_search_pvs(self, l_color, depth, alpha, beta):
		#print("AT ROOT entered pvs with color = {}, depth = {}, alpha = {}, beta = {}".format(l_color, depth, alpha, beta))
		best_score = -INFINITY
		best_move = ""
		possible_moves = self.get_valid_moves()
		if (len(possible_moves) == 0):
			return self.eval_board(l_color)
		#random.shuffle(possible_moves)
		possible_moves = self.order_moves(possible_moves, l_color)
		#print("AT ROOT current board: {}".format(self.board))
		#print("AT ROOT possible moves: {}".format(possible_moves))
		found_pv = False
		for current_move in possible_moves:
			#print("AT ROOT current best move: {}".format(best_move))
			#print("board before move: {}".format(self.board))
			row = self.make_move_on_board(current_move, l_color)
			#print("AT ROOT made move {}".format(current_move))
			if (found_pv):
				new_score = -self.pvs(-l_color, depth - 1, -alpha - 1, -alpha)
				if (new_score > alpha and new_score < beta):
					new_score = -self.pvs(-l_color, depth - 1, -beta, -alpha)
			else:
				new_score = -self.pvs(-l_color, depth - 1, -beta, -alpha)
			#print("board after move: {}".format(self.board))
			#print("entering negamax with color = {}, depth = {}, alpha = {}, beta = {}".format(-color, depth - 1, -beta, -alpha))
			#print("AT ROOT returned with value {} for move {}".format(new_score, current_move))
			#print("board before unmake move: {}".format(self.board))
			self.unmake_move(row, int(current_move))
			#print("unmade move {} {}".format(row, int(current_move)))
			#print("board after unmake move: {}".format(self.board))

			if (new_score > alpha):
				alpha = new_score
				best_move = current_move
				found_pv = True
			if (new_score >= beta):
				#print("TRIGGERED BETA")
				break
		#print("AT ROOT FINALLY possible moves: {}".format(possible_moves))
		#print("AT ROOT FINALLY best move: {}".format(best_move))
		#print("AT ROOT FINALLY best move: {}".format(best_move))
		return best_move

	def order_moves(self, valid_moves, l_color):
		possible_move_score_pairs = []
		valid_moves_ordered = []
		for curr_move in valid_moves:
			row = self.make_move_on_board(curr_move, l_color)
			curr_eval = self.eval_board(l_color)
			self.unmake_move(row, int(curr_move))
			possible_move_score_pairs.append((curr_eval, curr_move))

		possible_move_score_pairs_ordered = sorted(possible_move_score_pairs, key=lambda x: x[0], reverse=True)
		#for pair in possible_move_score_pairs_ordered:
			#valid_moves_ordered.append(pair[1])
		#return valid_moves_ordered
		return [pair[1] for pair in possible_move_score_pairs_ordered]



	def send_move(self, move):
		sys.stdout.write("place_disc {}".format(move) + "\n")
		sys.stdout.flush()

	def get_random_move(self): return random.randint(0, 6)

	def run(self):
		print("hi")
		while not sys.stdin.closed:
			# print("CURRENT BOARD: {}".format(my_bot.board))
			m_input = sys.stdin.readline().strip()
			if (m_input):
				msg = m_input.split(" ")
				if (msg[0] == "settings"):
					my_bot.store_settings(msg)
				elif (msg[0] == "update"):
					my_bot.update(msg)
				elif (msg[0] == "action"):
					# my_bot.make_move(self.get_random_move())
					computer_move = my_bot.root_search_negamax(my_bot.color, MINIMAX_DEPTH, ALPHA_0, BETA_0)
					my_bot.make_move(computer_move, my_bot.color)
					my_bot.send_move(computer_move)

	def draw_board(self):
		pygame.init()
		pygame.display.init()
		FONT = pygame.font.Font('ubuntu.ttf', TEXT_SIZE)
		self.window.window.fill(BACKGROUND_COLOR)
		pygame.draw.polygon(self.window.window, BOARD_COLOR, (((WINDOWWIDTH - BOARDWIDTH) / 2, (WINDOWHEIGHT - BOARDHEIGHT) / 2), (BOARDWIDTH + (WINDOWWIDTH - BOARDWIDTH) / 2, (WINDOWHEIGHT - BOARDHEIGHT) / 2), (BOARDWIDTH + (WINDOWWIDTH - BOARDWIDTH) / 2, BOARDHEIGHT + (WINDOWHEIGHT - BOARDHEIGHT) / 2), ((WINDOWWIDTH - BOARDWIDTH) / 2, BOARDHEIGHT + (WINDOWHEIGHT - BOARDHEIGHT) / 2)))
		pygame.draw.polygon(self.window.window, WHITE, (((WINDOWWIDTH - BOARDWIDTH) / 2, (WINDOWHEIGHT - BOARDHEIGHT) / 2), (BOARDWIDTH + (WINDOWWIDTH - BOARDWIDTH) / 2, (WINDOWHEIGHT - BOARDHEIGHT) / 2), (BOARDWIDTH + (WINDOWWIDTH - BOARDWIDTH) / 2, BOARDHEIGHT / 7 + (WINDOWHEIGHT - BOARDHEIGHT) / 2),	((WINDOWWIDTH - BOARDWIDTH) / 2, BOARDHEIGHT / 7 + (WINDOWHEIGHT - BOARDHEIGHT) / 2)))

		for i in range(8):
			pygame.draw.line(self.window.window, BLACK, ((WINDOWWIDTH - BOARDWIDTH) / 2, (WINDOWHEIGHT - BOARDHEIGHT) / 2 + i * BOARDHEIGHT / 7), ((WINDOWWIDTH - BOARDWIDTH) / 2 + BOARDWIDTH, (WINDOWHEIGHT - BOARDHEIGHT) / 2 + i * BOARDHEIGHT / 7), 2)
			pygame.draw.line(self.window.window, BLACK, ((WINDOWWIDTH - BOARDWIDTH) / 2 + i * BOARDWIDTH / 7, (WINDOWHEIGHT - BOARDHEIGHT) / 2 ), ((WINDOWWIDTH - BOARDWIDTH) / 2 + i * BOARDWIDTH / 7, (WINDOWHEIGHT - BOARDHEIGHT) / 2 + BOARDHEIGHT), 2)

		for i in range(7):
			text = FONT.render(str(i), True, BLACK, WHITE)
			textRect = text.get_rect()
			textRect.centerx = self.window.window.get_rect().centerx
			textRect.centery = self.window.window.get_rect().centery
			self.window.window.blit(text, ((WINDOWWIDTH - BOARDWIDTH) / 2 + i * BOARDWIDTH / 7 + (BOARDWIDTH / 7 - TEXT_SIZE / 2) / 2, (WINDOWHEIGHT - BOARDHEIGHT) / 2 + (BOARDHEIGHT / 7 - TEXT_SIZE) / 2))

		for i in range(6):
			for j in range(7):
				if (self.board[i][j] == '1'):
					pygame.draw.circle(self.window.window, RED, (int(X_MARGIN + j * BOARDWIDTH / 7 + BOARDWIDTH / (7 * 2)), int(Y_MARGIN + (i + 1) * BOARDHEIGHT / 7 + BOARDHEIGHT / (7 * 2))), DISC_RADIUS, 0)
				elif (self.board[i][j] == '2'):
					pygame.draw.circle(self.window.window, YELLOW, (int(X_MARGIN + j * BOARDWIDTH / 7 + BOARDWIDTH / (7 * 2)), int(Y_MARGIN + (i + 1) * BOARDHEIGHT / 7 + BOARDHEIGHT / (7 * 2))), DISC_RADIUS, 0)
				elif (self.board[i][j] == '0'):
					pygame.draw.circle(self.window.window, WHITE, (
					int(X_MARGIN + j * BOARDWIDTH / 7 + BOARDWIDTH / (7 * 2)), int(Y_MARGIN + (i + 1) * BOARDHEIGHT / 7 + BOARDHEIGHT / (7 * 2))), DISC_RADIUS, 0)

		pygame.display.update()


	def draw_choose_first_move2(self):
		WINDOWHEIGHT_FIRST_MOVE = WINDOWHEIGHT // 2
		WINDOWWIDTH_FIRST_MOVE = WINDOWWIDTH // 2
		TEXT_SIZE_FIRST_MOVE = 16

		first_move_window = pygame.display.set_mode((WINDOWWIDTH_FIRST_MOVE, WINDOWHEIGHT_FIRST_MOVE))
		pygame.display.set_caption("Four in a row")
		FONT = pygame.font.Font('ubuntu.ttf', TEXT_SIZE_FIRST_MOVE)
		first_move_window.fill(BACKGROUND_COLOR)
		text_choose = FONT.render("Choose who moves first: ", True, BLACK, WHITE)
		textRect_choose = text_choose.get_rect()
		textRect_choose.centerx = first_move_window.get_rect().centerx
		textRect_choose.centery = first_move_window.get_rect().centery
		first_move_window.blit(text_choose, (WINDOWWIDTH_FIRST_MOVE // 4, WINDOWHEIGHT_FIRST_MOVE // 4))
		text_player = FONT.render("Player ", True, BLACK, WHITE)
		text_player_rect = text_player.get_rect()
		#text_player_rect.centerx = first_move_window.get_rect().centerx
		#text_player_rect.centery = first_move_window.get_rect().centery
		text_player_rect.centerx = WINDOWWIDTH_FIRST_MOVE // 4 + text_player_rect.w / 2
		text_player_rect.centery = WINDOWHEIGHT_FIRST_MOVE // 2 + text_player_rect.h / 2
		first_move_window.blit(text_player, (WINDOWWIDTH_FIRST_MOVE // 4, WINDOWHEIGHT_FIRST_MOVE // 2))
		text_computer = FONT.render("Computer", True, BLACK, WHITE)
		text_computer_rect = text_computer.get_rect()
		text_computer_rect.centerx = WINDOWWIDTH_FIRST_MOVE // 2 + text_computer_rect.w / 2
		text_computer_rect.centery = WINDOWHEIGHT_FIRST_MOVE // 2 + text_computer_rect.h / 2
		first_move_window.blit(text_computer, (WINDOWWIDTH_FIRST_MOVE // 2, WINDOWHEIGHT_FIRST_MOVE // 2))
		no_input = True
		#print(text_player_rect.top, text_player_rect.bottom, text_player_rect.left, text_player_rect.right, text_player_rect.topleft)
		print(text_player_rect.topleft, text_player_rect.bottomright)
		while (no_input):
			for event in pygame.event.get():
				if event.type == pygame.locals.QUIT:
					pygame.quit()
					sys.exit()
				elif (event.type == pygame.locals.MOUSEBUTTONUP and event.button == 1):
					cursor_x = pygame.mouse.get_pos()[0]
					cursor_y = pygame.mouse.get_pos()[1]
					if (text_player_rect.collidepoint(cursor_x, cursor_y)):
						self.color = -1
						self.side_to_move = 42
						no_input = False
					if (text_computer_rect.collidepoint(cursor_x, cursor_y)):
						self.color = 1
						self.side_to_move = -42
						no_input = False
			pygame.display.update()
			time.sleep(0.1)
		pygame.display.quit()
		#pygame.quit()

	def draw_choose_first_move(self):

		pygame.display.set_caption("Four in a row")
		FONT = pygame.font.Font('ubuntu.ttf', TEXT_SIZE_FIRST_MOVE)
		self.window.window.fill(BACKGROUND_COLOR)
		text_choose = FONT.render("Choose who moves first: ", True, BLACK, WHITE)
		textRect_choose = text_choose.get_rect()
		textRect_choose.centerx = self.window.window.get_rect().centerx
		textRect_choose.centery = self.window.window.get_rect().centery
		self.window.window.blit(text_choose, (WINDOWWIDTH // 4, WINDOWHEIGHT // 3))
		text_player = FONT.render("Player ", True, BLACK, WHITE)
		text_player_rect = text_player.get_rect()
		# text_player_rect.centerx = first_move_window.get_rect().centerx
		# text_player_rect.centery = first_move_window.get_rect().centery
		text_player_rect.centerx = WINDOWWIDTH // 4 + text_player_rect.w / 2
		text_player_rect.centery = WINDOWHEIGHT // 2 + text_player_rect.h / 2
		self.window.window.blit(text_player, (WINDOWWIDTH // 4, WINDOWHEIGHT // 2))
		text_computer = FONT.render("Computer", True, BLACK, WHITE)
		text_computer_rect = text_computer.get_rect()
		text_computer_rect.centerx = WINDOWWIDTH // 2 + text_computer_rect.w / 2
		text_computer_rect.centery = WINDOWHEIGHT // 2 + text_computer_rect.h / 2
		self.window.window.blit(text_computer, (WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
		no_input = True
		# print(text_player_rect.top, text_player_rect.bottom, text_player_rect.left, text_player_rect.right, text_player_rect.topleft)
		#print(text_player_rect.topleft, text_player_rect.bottomright)
		while (no_input):
			for event in pygame.event.get():
				if event.type == pygame.locals.QUIT:
					pygame.quit()
					sys.exit()
				elif (event.type == pygame.locals.MOUSEBUTTONUP and event.button == 1):
					cursor_x = pygame.mouse.get_pos()[0]
					cursor_y = pygame.mouse.get_pos()[1]
					#print("clicked at ({}, {})".format(cursor_x, cursor_y))
					if (text_player_rect.collidepoint(cursor_x, cursor_y)):
						# print("player!!!")
						self.color = -1
						self.side_to_move = 42
						no_input = False
					if (text_computer_rect.collidepoint(cursor_x, cursor_y)):
						# print("computer!!!")
						self.color = 1
						self.side_to_move = -42
						no_input = False
			pygame.display.update()
			time.sleep(0.1)
		#pygame.display.quit()

	# pygame.quit()

	def show_game_result(self):
		game_result_caption = ""
		print("Game is finished!")
		if (self.check_is_finished() == 1):
			if (self.color == 1):
				game_result_caption = "Computer won!"
			else:
				game_result_caption = "Player won!"
		elif (self.check_is_finished() == 2):
			if (self.color == -1):
				game_result_caption = "Computer won!"
			else:
				game_result_caption = "Player won!"
		else:
			game_result_caption = "Computer won!"
		pygame.display.set_caption(game_result_caption)

		FONT = pygame.font.Font('ubuntu.ttf', TEXT_SIZE_GAME_RESULT)
		#self.window.window.fill(BACKGROUND_COLOR)
		text_game_result = FONT.render(game_result_caption, True, BLACK, WHITE)
		text_game_result_rect = pygame.Rect(X_MARGIN, (Y_MARGIN  - SQUARE_SIZE) // 2, BOARDWIDTH, BOARDHEIGHT // 7)
		text_game_result_rect = text_game_result.get_rect()
		text_game_result_rect.centerx = X_MARGIN // 2 #+ BOARDWIDTH // 2
		text_game_result_rect.centery = Y_MARGIN // 2 #+ BOARDHEIGHT // 2
		self.window.window.blit(text_game_result, (X_MARGIN, (Y_MARGIN  - SQUARE_SIZE) // 2))
		pygame.display.update()


	def show_play_again_dialog(self):
		FONT = pygame.font.Font('ubuntu.ttf', TEXT_SIZE_PLAY_AGAIN)

		text_play_again = FONT.render("Play again?", True, BLACK, WHITE)
		text_play_again_rect = pygame.Rect(int(X_MARGIN * 1.1) + BOARDWIDTH, Y_MARGIN, X_MARGIN, BOARDHEIGHT // 7)
		text_play_again_rect = text_play_again.get_rect()
		text_play_again_rect.centerx = X_MARGIN + BOARDWIDTH + X_MARGIN // 2
		text_play_again_rect.centery = Y_MARGIN + BOARDHEIGHT // (2 * 7)
		self.window.window.blit(text_play_again, (int(X_MARGIN * 1.1) + BOARDWIDTH, Y_MARGIN))

		text_yes = FONT.render("Yes", True, BLACK, WHITE)
		yes_rect = text_yes.get_rect()
		text_yes_rect = pygame.Rect(X_MARGIN + BOARDWIDTH + BOARDWIDTH // (4 * 7), Y_MARGIN + BOARDHEIGHT // (7), yes_rect.w, yes_rect.h)
		text_yes_rect = text_yes.get_rect()
		text_yes_rect.centerx = X_MARGIN + BOARDWIDTH + BOARDWIDTH // (4 * 7) + yes_rect.w // 2
		text_yes_rect.centery = Y_MARGIN + BOARDHEIGHT // (7) + yes_rect.h // 2
		self.window.window.blit(text_yes, (X_MARGIN + BOARDWIDTH + BOARDWIDTH // (4 * 7), Y_MARGIN + BOARDHEIGHT // (7)))

		text_no = FONT.render("No", True, BLACK, WHITE)
		no_rect = text_no.get_rect()
		text_no_rect = pygame.Rect(X_MARGIN + BOARDWIDTH + BOARDWIDTH * 0.2, Y_MARGIN + BOARDHEIGHT // (7), no_rect.w, no_rect.h)
		text_no_rect = text_no.get_rect()
		text_no_rect.centerx = X_MARGIN + BOARDWIDTH + BOARDWIDTH * 0.2 + no_rect.w // 2
		text_no_rect.centery = Y_MARGIN + BOARDHEIGHT // (7) + no_rect.h // 2
		self.window.window.blit(text_no, (X_MARGIN + BOARDWIDTH + BOARDWIDTH * 0.2, Y_MARGIN + BOARDHEIGHT // (7)))
		pygame.display.update()
		no_input = True
		while (no_input):
			for event in pygame.event.get():
				if event.type == pygame.locals.QUIT:
					pygame.quit()
					sys.exit()
				elif (event.type == pygame.locals.MOUSEBUTTONUP and event.button == 1):
					cursor_x = pygame.mouse.get_pos()[0]
					cursor_y = pygame.mouse.get_pos()[1]
					#print("clicked at ({}, {})".format(cursor_x, cursor_y))
					if (text_yes_rect.collidepoint(cursor_x, cursor_y)):
						no_input = False
					elif (text_no_rect.collidepoint(cursor_x, cursor_y)):
						self.play_again = False
						no_input = False


	def change_end_game_caption(self):
		game_result_caption = ""
		print("Game is finished!")
		if (self.check_is_finished() == 1):
			if (self.color == 1): game_result_caption = "Computer won!"
			else: game_result_caption = "Player won!"
		elif (self.check_is_finished() == 2):
			if (self.color == -1): game_result_caption = "Computer won!"
			else: game_result_caption = "Player won!"
		else: game_result_caption = "Computer won!"
		pygame.display.set_caption(game_result_caption)



	def get_input(self):
		no_input = True
		while(no_input):
			for event in pygame.event.get():
				if event.type == pygame.locals.QUIT:
					pygame.quit()
					sys.exit()
				elif (event.type == pygame.locals.MOUSEBUTTONUP and event.button == 1):
					cursor_x = pygame.mouse.get_pos()[0]
					cursor_y = pygame.mouse.get_pos()[1]
					if ((cursor_x > X_MARGIN) and (cursor_x < BOARDWIDTH + X_MARGIN) and (cursor_y > Y_MARGIN) and (cursor_y < (BOARDHEIGHT / (7) + Y_MARGIN))):
						x_coord = (cursor_x - X_MARGIN) / SQUARE_SIZE
						#y_coord = (cursor_y - Y_MARGIN) / SQUARE_SIZE
						#print("clicked at {}".format(x_coord))
						no_input = False
			time.sleep(0.1)
		#print("left while loop with x_coord = {}".format(int(x_coord)))
		#self.make_move_on_board(int(x_coord), -self.color)
		return int(x_coord)

	def make_move(self):
		#if (self.move_number == 42):
			#self.is_finished ==
		#print("entered make move!")
		if (self.side_to_move == 42):#it's player turn
			input_move = self.get_input()
			#print("move received from input: {}".format(input_move))
			if (str(input_move) in self.get_valid_moves()):
				self.make_move_on_board(input_move, -self.color)
				self.move_number += 1
				self.side_to_move *= -1
		else:#it's computer turn
			start_time = time.time()
			computer_move = self.root_search_negamax(self.color, MINIMAX_DEPTH, ALPHA_0, BETA_0)
			#computer_move = self.root_search_pvs(self.color, MINIMAX_DEPTH, ALPHA_0, BETA_0)
			#computer_move = random.randint(0, 6)
			self.make_move_on_board(computer_move, self.color)
			#print("made move {}".format(computer_move))
			#print("current board: {}".format(self.board))
			self.move_number += 1
			self.side_to_move *= -1
			end_time = time.time()
			print("computer thought for {} seconds".format(end_time - start_time))

	def check_is_finished(self):
		#if (self.is_terminal_node(1) == 0): self.is_finished = True

		for i in range(6):  # check for horizontal win/loss
			for j in range(4):
				if (self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] == '1'): return 1
				if (self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] == '2'): return 2
		for j in range(7):  # check for vertical win/loss
			for i in range(3):
				if (self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] == '1'): return 1
				if (self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] == '2'): return 2

			# check for bottom_left -> top_right diagonal win/loss
		if (self.board[3][0] == self.board[2][1] == self.board[1][2] == self.board[0][3] == '1'): return 1
		if (self.board[3][0] == self.board[2][1] == self.board[1][2] == self.board[0][3] == '2'): return 2
		if (self.board[4][0] == self.board[3][1] == self.board[2][2] == self.board[1][3] == '1'): return 1
		if (self.board[4][0] == self.board[3][1] == self.board[2][2] == self.board[1][3] == '2'): return 2
		if (self.board[3][1] == self.board[2][2] == self.board[1][3] == self.board[0][4] == '1'): return 1
		if (self.board[3][1] == self.board[2][2] == self.board[1][3] == self.board[0][4] == '2'): return 2
		if (self.board[5][0] == self.board[4][1] == self.board[3][2] == self.board[2][3] == '1'): return 1
		if (self.board[5][0] == self.board[4][1] == self.board[3][2] == self.board[2][3] == '2'): return 2
		if (self.board[4][1] == self.board[3][2] == self.board[2][3] == self.board[1][4] == '1'): return 1
		if (self.board[4][1] == self.board[3][2] == self.board[2][3] == self.board[1][4] == '2'): return 2
		if (self.board[3][2] == self.board[2][3] == self.board[1][4] == self.board[0][5] == '1'): return 1
		if (self.board[3][2] == self.board[2][3] == self.board[1][4] == self.board[0][5] == '2'): return 2
		if (self.board[5][1] == self.board[4][2] == self.board[3][3] == self.board[2][4] == '1'): return 1
		if (self.board[5][1] == self.board[4][2] == self.board[3][3] == self.board[2][4] == '2'): return 2
		if (self.board[4][2] == self.board[3][3] == self.board[2][4] == self.board[1][5] == '1'): return 1
		if (self.board[4][2] == self.board[3][3] == self.board[2][4] == self.board[1][5] == '2'): return 2
		if (self.board[3][3] == self.board[2][4] == self.board[1][5] == self.board[0][6] == '1'): return 1
		if (self.board[3][3] == self.board[2][4] == self.board[1][5] == self.board[0][6] == '2'): return 2
		if (self.board[5][2] == self.board[4][3] == self.board[3][4] == self.board[2][5] == '1'): return 1
		if (self.board[5][2] == self.board[4][3] == self.board[3][4] == self.board[2][5] == '2'): return 2
		if (self.board[4][3] == self.board[3][4] == self.board[2][5] == self.board[1][6] == '1'): return 1
		if (self.board[4][3] == self.board[3][4] == self.board[2][5] == self.board[1][6] == '2'): return 2
		if (self.board[5][3] == self.board[4][4] == self.board[3][5] == self.board[2][6] == '1'): return 1
		if (self.board[5][3] == self.board[4][4] == self.board[3][5] == self.board[2][6] == '2'): return 2

		# check for bottom_right -> top_left diagonal win/loss
		if (self.board[2][0] == self.board[3][1] == self.board[4][2] == self.board[5][3] == '1'): return 1
		if (self.board[2][0] == self.board[3][1] == self.board[4][2] == self.board[5][3] == '2'): return 2
		if (self.board[1][0] == self.board[2][1] == self.board[3][2] == self.board[4][3] == '1'): return 1
		if (self.board[1][0] == self.board[2][1] == self.board[3][2] == self.board[4][3] == '2'): return 2
		if (self.board[2][1] == self.board[3][2] == self.board[4][3] == self.board[5][4] == '1'): return 1
		if (self.board[2][1] == self.board[3][2] == self.board[4][3] == self.board[5][4] == '2'): return 2
		if (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[3][3] == '1'): return 1
		if (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[3][3] == '2'): return 2
		if (self.board[1][1] == self.board[2][2] == self.board[3][3] == self.board[4][4] == '1'): return 1
		if (self.board[1][1] == self.board[2][2] == self.board[3][3] == self.board[4][4] == '2'): return 2
		if (self.board[2][2] == self.board[3][3] == self.board[4][4] == self.board[5][5] == '1'): return 1
		if (self.board[2][2] == self.board[3][3] == self.board[4][4] == self.board[5][5] == '2'): return 2
		if (self.board[0][1] == self.board[1][2] == self.board[2][3] == self.board[3][4] == '1'): return 1
		if (self.board[0][1] == self.board[1][2] == self.board[2][3] == self.board[3][4] == '2'): return 2
		if (self.board[1][2] == self.board[2][3] == self.board[3][4] == self.board[4][5] == '1'): return 1
		if (self.board[1][2] == self.board[2][3] == self.board[3][4] == self.board[4][5] == '2'): return 2
		if (self.board[2][3] == self.board[3][4] == self.board[4][5] == self.board[5][6] == '1'): return 1
		if (self.board[2][3] == self.board[3][4] == self.board[5][5] == self.board[5][6] == '2'): return 2
		if (self.board[0][2] == self.board[1][3] == self.board[2][4] == self.board[3][5] == '1'): return 1
		if (self.board[0][2] == self.board[1][3] == self.board[2][4] == self.board[3][5] == '2'): return 2
		if (self.board[1][3] == self.board[2][4] == self.board[3][5] == self.board[4][6] == '1'): return 1
		if (self.board[1][3] == self.board[2][4] == self.board[3][5] == self.board[4][6] == '2'): return 2
		if (self.board[0][3] == self.board[1][4] == self.board[2][5] == self.board[3][6] == '1'): return 1
		if (self.board[0][3] == self.board[1][4] == self.board[2][5] == self.board[3][6] == '2'): return 2


		for row in self.board:# returns 0 in case the node is not terminal
			if ('0' in row): return 0

		return 3  # returns 3 in case the node is terminal



def main():
	random.seed()
	my_bot = Bot()
	my_bot.draw_choose_first_move()
	my_bot.draw_board()
	while(my_bot.play_again):
		while (not my_bot.is_finished):			
			my_bot.make_move()
			my_bot.draw_board()
			if (my_bot.check_is_finished() != 0): break

		my_bot.show_game_result()
		my_bot.show_play_again_dialog()
		if (not my_bot.play_again):
			pygame.quit()
			sys.exit()
			break
		my_bot = Bot()
		my_bot.draw_choose_first_move()
	time.sleep(5)






if __name__ == "__main__":
	main()
