import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import time
from .game import Board, Game
from .ai import AI
import os


def rel_path(file):
	"""
	This function will find the relative path of the file and make it
	available for opening.
	:param file:
	:return:
	"""
	return os.path.join(os.path.dirname(__file__), file)


class GUI:
	"""
	Main gui window
	"""

	def __init__(self):
		self.root = tk.Tk()
		self.root.resizable(False, False)
		self.main_menu = MainMenu(self.root, relief=tk.GROOVE, anchor=tk.N, width=1600, height=1200)
		self.main_menu.show(self.root)
		self.root.mainloop()


class MainMenu(tk.Label):
	"""
	Screen for the main menu
	"""

	def show(self, root: tk.Tk):
		"""
		Main menu Initialization
		:param root: tk
		"""
		PVP = tk.PhotoImage(file=rel_path("arcadePVP.resized.png"))
		PVC = tk.PhotoImage(file=rel_path("arcadePVC.resized.png"))
		CVP = tk.PhotoImage(file=rel_path("player_vs_computer.resized.png"))
		CVC = tk.PhotoImage(file=rel_path("computer_vs_computer.resized.png"))
		welcome = tk.PhotoImage(file=rel_path("welcome.png"))
		self.welcome = tk.Label(root, image=welcome)
		self.welcome.place(relx=.06, rely=0.1)

		self.pack()

		self.pvc_button = tk.Button(image=PVC, borderwidth=0)
		self.pvp_button = tk.Button(image=PVP, borderwidth=0)
		self.cvp_button = tk.Button(image=CVP, borderwidth=0)
		self.cvc_button = tk.Button(image=CVC, borderwidth=0)
		quit_button = tk.Button(text="QUIT", fg="black", compound=tk.CENTER, command=quit)

		self.pvp_button.bind("<Button-1>", lambda e: self.start_game(root, 'human', 'human'))
		self.pvc_button.bind("<Button-1>", lambda e: self.start_game(root, 'ai', 'human'))
		self.cvp_button.bind("<Button-1>", lambda e: self.start_game(root, 'human', 'ai'))
		self.cvc_button.bind("<Button-1>", lambda e: self.start_game(root, 'ai', 'ai'))
		self.pvp_button.place(relx=.02, rely=.3)
		self.pvc_button.place(relx=.02, rely=.4)
		self.cvp_button.place(relx=.02, rely=.5)
		self.cvc_button.place(relx=.02, rely=.6)
		quit_button.place(relx=.45, rely=.9)
		self.pvp_button.image = PVP
		self.pvc_button.image = PVC
		self.cvp_button.image = CVP
		self.cvc_button.image = CVC
		self.welcome.image = welcome

		self.load(rel_path('rain.gif'))

	def load(self, im):
		"""
		This is a special function that helps the GUI load a gif onto the
		main menu by loading frame by frame and transferring them to the main
		menu label.
		:param im: the gif
		:return: None
		"""
		if isinstance(im, str):
			im = Image.open(im)
		self.loc = 0
		self.frames = []

		try:
			for i in count(1):
				self.frames.append(ImageTk.PhotoImage(im.copy()))
				im.seek(i)
		except EOFError:
			pass

		try:
			self.delay = im.info['duration']
		except:
			self.delay = 100

		if len(self.frames) == 1:
			self.config(image=self.frames[0])
		else:
			self.next_frame()

	def unload(self):
		"""
		This function unloads the gif from the label
		:return: None
		"""
		self.config(image=None)
		self.frames = None

	def next_frame(self):
		"""
		This is a helper function for load.
		:return:
		"""
		if self.frames:
			self.loc += 1
			self.loc %= len(self.frames)
			self.config(image=self.frames[self.loc])
			self.after(self.delay, self.next_frame)

	def start_game(self, root, p1_type, p2_type):
		"""
		Starts the canvas that is responsible for the gam play and destroys
		the previous main menu label.
		:return: None
		"""
		time.sleep(0.1)
		self.unload()
		self.pvc_button.destroy()
		self.pvp_button.destroy()
		self.destroy()
		self.game_screen = GameScreen(root, p1_type, p2_type)


class GameScreen:
	"""
	Screen for the game

	Handles showing the game
	"""
	MAKE_AI_MOVE = "first_ai_move"
	def __init__(self, root, p1_type, p2_type):
		"""
		:param root:
		:param p1_type:  'ai' or 'human'
		:param p2_type: 'ai' or 'human'
		"""

		self.player1type = p1_type
		self.player2type = p2_type
		self.ai = [p1_type == 'ai', p2_type == 'ai']
		self.root = root
		self.game = Game()

		self.current_player_imgs = []
		canvas_image = tk.PhotoImage(file=rel_path("game_board2.png"))
		self.canvas = tk.Canvas(root, width=800, height=600)
		self.canvas.create_image(0, 0, image=canvas_image, anchor=tk.NW)
		self.canvas.pack()
		self.list_of_images = [canvas_image]
		self.canvas.images = self.list_of_images

		'''MAKE THE FIRST MOVE IF AI PLAYS FIRST'''
		if p1_type == 'ai' and p2_type == "human":
			self.player_1_ai = AI(self.game, 1)
			self.make_move(self.MAKE_AI_MOVE)

		self.winner = None

		if p1_type == "ai" and p2_type == "ai":
			self.player_1_ai = AI(self.game, 1)
			self.player_2_ai = AI(self.game, 2)

			for i in range(42):

				self.root.after(100)
				self.make_move(self.MAKE_AI_MOVE)
				self.update_board(self.game.board)
				self.root.update()
				if self.winner is not None:
					self.game_won()
					break

		else:
			self.canvas.bind('<ButtonRelease-1>', self.handle_click)
			self.player_2_ai = AI(self.game, 2)

	def make_move(self, col):
		"""
		Makes a turn
		:param player_id: int, player number ( 1 or 2)
		:param col:
		:return:
		"""

		''' THIS WORKS FOR PLAYER VS AI , PLAYER VS PLAYER,AI VS AI'''
		if col == self.MAKE_AI_MOVE:
			if self.game.current_player == 1:
				self.show_player_turn()
				ai_move = self.player_1_ai.find_legal_move()
			else:
				self.show_player_turn()
				ai_move = self.player_2_ai.find_legal_move()
			try:
				self.game.make_move(ai_move)
			except:
				pass

			self.update_board(self.game.board)
			self.game_won()
			return
		self.show_player_turn()
		self.game.make_move(col)
		self.update_board(self.game.board)

		if self.ai[self.game.current_player - 1] and not self.winner:
			self.show_player_turn()
			current_player = self.game.current_player
			if current_player == 1:
				ai_move = self.player_1_ai.find_legal_move()
			else:
				ai_move = self.player_2_ai.find_legal_move()
			self.game.make_move(ai_move)
			self.update_board(self.game.board)
			self.game_won()

	def get_mouse(self, event):
		"""
		This function will receive the event and check which column it matches.
		:param event: the mouse click
		:return: the column if the click is valid or None if it's not
		"""
		mouse_x = event.x
		if mouse_x < 200 and mouse_x > 120:
			column = 0
			if mouse_x < 110:
				column = None
			return column
		if mouse_x < 290 and mouse_x > 215:
			column = 1
			return column
		if mouse_x < 360 and mouse_x > 290:
			column = 2
			return column
		if mouse_x < 435 and mouse_x > 360:
			column = 3
			return column
		if mouse_x < 520 and mouse_x > 435:
			column = 4
			return column
		if mouse_x < 585 and mouse_x > 520:
			column = 5
			return column
		if mouse_x > 685:
			return None
		if mouse_x < 660 and mouse_x > 585:
			column = 6
			return column

	def update_board(self, board: Board,if_winner = False):
		"""
		This function will update the board
		:return: None
		"""
		img1 = tk.PhotoImage(file=rel_path('circle-blue.resized2.png'))
		img2 = tk.PhotoImage(file=rel_path('circle-red.resized.png'))
		mark_winner = tk.PhotoImage(file = rel_path('crown.png'))
		self.list_of_images.append(img1)
		self.list_of_images.append(img2)
		self.list_of_images.append(mark_winner)
		for i in range(7):  # columns
			for j in range(6):  # rows

				if board.board[j][i] == 1:

					self.canvas.create_image(133 + (76*i), 35 + (90*j), image=img1, anchor=tk.NW)

				elif board.board[j][i] == 2:
					self.canvas.create_image(133 + (76*i), 35 + (90*j), image=img2, anchor=tk.NW)






	def show_player_turn(self):
		"""
		This function will show the player's image
		:param side: 1 if left and 2 for right
		:param player_type: 'ai' or 'human'
		:return: None
		"""

			# self.list_of_images.pop()
		if not self.game_won():
			side = self.game.current_player
			if side<2:
				side += 1
			else:
				side -= 1
			coords = (175,5)
			current_turn_image = tk.PhotoImage(file=rel_path(f"player{side}turn.png"))
			self.canvas.create_image(*coords, image=current_turn_image, anchor=tk.NW)
			self.canvas.image = current_turn_image
		else:
			self


	def handle_click(self, mouse_event, column=None):
		"""
		This function will transfer the user's interaction with the board
		:param mouse_event: the click of the mouse
		:param column: the column the mouse clicked on
		:return: None
		"""
		if self.winner is not None:
			return
		if column is None:
			column = self.get_mouse(mouse_event)
		try:
			self.make_move(column)
		except:
			pass
		self.game_won()


	def game_won(self):
		"""
		This function will check if the game has been won or tied and will
		show the winner on the screen (the first player, the second player,
		or a tie)
		:return: None
		"""
		winner = self.game.get_winner()

		if winner is not None:
			# there is a winner
			self.winner = winner
			self.show_winner(winner)



	def show_winner(self, winner):
		"""
		This function will show the winner on the screen
		:param winner: the first player (1), the second player (2), or a tie
		:return: None
		"""
		if winner == 2 or winner == 1:
			img = tk.PhotoImage(file=rel_path(f'player-{winner}-won.png'))
		else:
			img = tk.PhotoImage(file=rel_path('tie.png'))
		self.list_of_images.append(img)
		self.canvas.create_image(180, 150, image=img, anchor=tk.NW)

		button = tk.Button(text="play again", borderwidth=0, command=self.startover)
		button.place(relx=.02, rely=.4)
		button2 = tk.Button(text="Quit", borderwidth=0, command=quit)
		button2.place(relx=.9, rely=0.4)


	def startover(self):
		"""
		This function will start the game over
		"""
		self.root.destroy()
		GUI()
