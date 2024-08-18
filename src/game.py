import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game :

	def __init__(self) :
		self.next_player = 'white'
		self.hovered_square = None
		self.board = Board()
		self.dragger = Dragger()
		self.config = Config()

	# blit Methods

	def show_bg(self, surface) :
		theme = self.config.theme

		for row in range(ROWS) :
			for col in range(COLS) :
				# color
				# Classic Wood
					# Light: (222, 184, 135) (Burlywood)
					# Dark: (139, 69, 19) (Saddle Brown)
				# Modern Grey
					# Light: (200, 200, 200) (Light Grey)
					# Dark: (50, 50, 50) (Dark Grey)
				# Oceanic Blue
					# Light: (173, 216, 230) (Light Blue)
					# Dark: (0, 105, 148) (Medium Blue)
				# Forest Green
					# Light: (144, 238, 144) (Light Green)
					# Dark: (34, 139, 34) (Forest Green)
				# Sunset Orange
					# Light: (255, 228, 181) (Moccasin)
					# Dark: (255, 140, 0) (Dark Orange)
				# Cool Mint
					# Light: (152, 255, 152) (Pale Green)
					# Dark: (0, 128, 128) (Teal)
				# Desert Sand 
					# Light: (245, 222, 179) (Wheat)
					# Dark: (210, 180, 140) (Tan)
				color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
				# rect
				rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
				# blit
				pygame.draw.rect(surface, color, rect)

				# row coordinates
				if col == 0 :
					# color
					color = theme.bg.dark if row % 2 == 0 else theme.bg.light
					# label
					label = self.config.font.render(str(ROWS-row), 1, color)
					label_pos = (5, 5 + row * SQSIZE)
					# blit
					surface.blit(label, label_pos)

				# col coordinates
				if row == 7 :
					# color
					color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
					# label
					label = self.config.font.render(Square.get_alphacol(col), 1, color)
					label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
					# blit
					surface.blit(label, label_pos)

	def show_pieces(self, surface) :
		for row in range(ROWS) :
			for col in range(COLS) :
				# piece ?
				if self.board.squares[row][col].has_piece() :
					piece = self.board.squares[row][col].piece

					# all pieces except dragger piece
					if piece is not self.dragger.piece :
						piece.set_texture(size=80)
						img = pygame.image.load(piece.texture)
						img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
						piece.texture_rect = img.get_rect(center=img_center)
						surface.blit(img, piece.texture_rect)

	def show_moves(self, surface) :
		theme = self.config.theme

		if self.dragger.dragging :
			piece = self.dragger.piece

			# loop all valid moves
			for move in piece.moves :
				# color
				# Classic Wood
					# Light: (255, 239, 213) (Papaya Whip)
					# Dark: (210, 105, 30) (Chocolate)
				# Modern Grey
					# Light: (169, 169, 169) (Dark Grey)
					# Dark: (105, 105, 105) (Dim Grey)
				# Oceanic Blue
					# Light: (135, 206, 250) (Sky Blue)
					# Dark: (25, 25, 112) (Midnight Blue)
				# Forest Green
					# Light: (60, 179, 113) (Medium Sea Green)
					# Dark: (0, 100, 0) (Dark Green)
				# Sunset Orange
					# Light: (255, 165, 79) (Light Salmon)
					# Dark: (255, 69, 0) (Red Orange)
				# Cool Mint
					# Light: (144, 238, 144) (Light Green)
					# Dark: (0, 139, 139) (Dark Cyan)
				# Desert Sand 
					# Light: (255, 239, 213) (Papaya Whip)
					# Dark: (222, 184, 135) (Burlywood)
				color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
				# rect
				rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
				# blit
				pygame.draw.rect(surface, color, rect)

	def show_last_move(self, surface) :
		theme = self.config.theme

		if self.board.last_move :
			initial = self.board.last_move.initial
			final = self.board.last_move.final

			for pos in [initial, final] :
				# color
				# Classic Wood
					# Light: (255, 228, 181) (Moccasin)
					# Dark: (160, 82, 45) (Sienna)
				# Modern Grey
					# Light: (211, 211, 211) (Light Grey)
					# Dark: (169, 169, 169) (Dark Grey)
				# Oceanic Blue
					# Light: (175, 238, 238) (Pale Turquoise)
					# Dark: (70, 130, 180) (Steel Blue)
				# Forest Green
					# Light: (144, 238, 144) (Light Green)
					# Dark: (46, 139, 87) (Sea Green)
				# Sunset Orange
					# Light: (255, 160, 122) (Light Coral)
					# Dark: (255, 99, 71) (Tomato)
				# Cool Mint
					# Light: (175, 238, 238) (Pale Turquoise)
					# Dark: (32, 178, 170) (Light Sea Green)
				# Desert Sand 
					# Light: (250, 240, 230) (Linen)
					# Dark: (244, 164, 96) (Sandy Brown)
				color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
				# rect
				rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
				# blit
				pygame.draw.rect(surface, color, rect)

	def show_hover(self, surface) :
		if self.hovered_square :
			# color
			# Classic Wood
				# Light: (255, 218, 185) (Peach Puff)
			# Modern Grey
				# Light: (192, 192, 192) (Silver)
			# Oceanic Blue
				# Light: (176, 224, 230) (Powder Blue)
			# Forest Green
				# Light: (152, 251, 152) (Pale Green)
			# Sunset Orange
				# Light: (255, 218, 185) (Peach Puff)
			# Cool Mint
				# Light: (144, 238, 144) (Light Green)

			color = (255, 228, 196) # Desert Sand (Bisque)
			# rect
			rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
			# blit
			pygame.draw.rect(surface, color, rect, width=5)

	# other methods

	def next_turn(self) :
		self.next_player = 'white' if self.next_player == 'black' else 'black'

	def set_hover(self, row, col) :
		self.hovered_square = self.board.squares[row][col]

	def change_theme(self) :
		self.config.change_theme()

	def play_sound(self, captured=False) :
		if captured :
			self.config.capture_sound.play()
		else :
			self.config.move_sound.play()

	def restart(self) :
		self.__init__()
