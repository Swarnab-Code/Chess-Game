import pygame

from const import *
from board import Board
from dragger import Dragger

class Game :

	def __init__(self) :
		self.board = Board()
		self.dragger = Dragger()

	# blit Methods

	def show_bg(self, surface) :
		for row in range(ROWS) :
			for col in range(COLS) :
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
				# Royal Purple
					# Light: (218, 112, 214) (Orchid)
					# Dark: (75, 0, 130) (Indigo)
				# Sunset Orange
					# Light: (255, 228, 181) (Moccasin)
					# Dark: (255, 140, 0) (Dark Orange)
				# Cool Mint
					# Light: (152, 255, 152) (Pale Green)
					# Dark: (0, 128, 128) (Teal)
					
				# Desert Sand
					# Light: (Wheat)
					# Dark: (Tan)
				if (row + col) % 2 == 0 :
					color = (245, 222, 179) #Wheat
				else :
					color = (210, 180, 140) #Tan
				rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
				pygame.draw.rect(surface, color, rect)

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
		if self.dragger.dragging :
			piece = self.dragger.piece

			# loop all valid moves
			for move in piece.moves :
				# color
				# Vibrant Green
				# Light Square Highlight: #64C864
				# Dark Square Highlight: #46C846

				# Cool Blue
				# Light Square Highlight: #6496C8
				# Dark Square Highlight: #4674C8

				# Soft Pink
				# Light Square Highlight: #C864A8
				# Dark Square Highlight: #C8468A

				# Golden Yellow
				# Light Square Highlight: #C8C864
				# Dark Square Highlight: #C8A846

				# Muted Purple
				# Light Square Highlight: #9A64C8
				# Dark Square Highlight: #7C46C8
				color = '#C8C864' if (move.final.row + move.final.col) % 2 == 0 else '#C8A846'
				# rect
				rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
				# blit
				pygame.draw.rect(surface, color, rect)