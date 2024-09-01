import pygame

from const import *
from square import Square
from piece import *
from move import Move

class Board :

	def __init__(self) :
		self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
		self.last_move = None
		self._create()
		self._add_pieces('white')
		self._add_pieces('black')

	def move(self, piece, move) :
		initial = move.initial
		final = move.final

		# console board move update
		self.squares[initial.row][initial.col].piece = None
		self.squares[final.row][final.col].piece = piece

		# pawn promotion
		if isinstance(piece, Pawn) :
			self.check_promotion(piece, final)

		# king castling
		if isinstance(piece, King) :
			if self.castling(initial, final) :
				difference = final.col - initial.col
				rook = piece.left_rook if (difference < 0) else piece.right_rook
				self.move(rook, rook.moves[-1])

		# move
		piece.moved = True

		# remove valid moves
		piece.remove_moves()

		# set last move
		self.last_move = move

	def valid_move(self, piece, move) :
		return move in piece.moves
	
	def check_promotion(self, piece, final) :
		if final.row == 0 or final.row == 7 :
			self.squares[final.row][final.col].piece = Queen(piece.color)

	def castling(self, initial, final) :
		return abs(initial.col - final.col) == 2

	def calc_moves(self, piece, row, col) :
		'''
			Calculate all possible moves for a piece on the board.
		'''

		def pawn_moves() :
			# steps
			steps = 1 if piece.moved else 2

			# vertical moves
			start = row + piece.dir
			end = row + (piece.dir * (1 + steps))
			for possible_move_row in range(start, end, piece.dir) :
				if Square.in_range(possible_move_row) :
					if self.squares[possible_move_row][col].isempty() :
						# create initial and final move squares
						initial = Square(row, col)
						final = Square(possible_move_row, col)
						# create a new move
						move = Move(initial, final)
						# append new move
						piece.add_move(move)
					# blocked
					else :
						break
				# not in range
				else :
					break

			# diagonal moves
			possible_move_row = row + piece.dir
			possible_move_cols = [col - 1, col + 1]

			for possible_move_col in possible_move_cols :
				if Square.in_range(possible_move_row, possible_move_col) :
					if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color) :
						# create initial and final move squares
						initial = Square(row, col)
						final = Square(possible_move_row, possible_move_col)
						# create a new move
						move = Move(initial, final)
						# append new move
						piece.add_move(move)

		# pawn en passant move

		def knight_moves() :
			# 8 possible moves
			possible_moves = [
				(row - 1, col - 2),
				(row - 1, col + 2),
				(row + 1, col - 2),
				(row + 1, col + 2),
				(row - 2, col - 1),
				(row - 2, col + 1),
				(row + 2, col - 1),
				(row + 2, col + 1),
			]

			for possible_move in possible_moves :
				possible_move_row, possible_move_col = possible_move

				if Square.in_range(possible_move_row, possible_move_col) :
					if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color) :
						# create squares of the new move
						initial = Square(row, col)
						final = Square(possible_move_row, possible_move_col)
						# create new move
						move = Move(initial, final)
						# add valid move to moves
						piece.add_move(move)

		def straightline_moves(incrs) :
			for incr in incrs :
				row_incr, col_incr = incr
				possible_move_row = row + row_incr
				possible_move_col = col + col_incr

				while True :
					if Square.in_range(possible_move_row, possible_move_col) :
						# create squares of the possible new move
						initial = Square(row, col)
						final = Square(possible_move_row, possible_move_col)
						# create a possible new move
						move = Move(initial, final)

						# empty = continue looping
						if self.squares[possible_move_row][possible_move_col].isempty() :
							# append new move
							piece.add_move(move)

						# has rival piece = add move + break
						if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color) :
							# append new move
							piece.add_move(move)
							break

						# has team piece = break
						if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color) :
							break

					# not in range
					else :
						break

					# incrementing incr					
					possible_move_row = possible_move_row + row_incr
					possible_move_col = possible_move_col + col_incr
		
		def king_moves() :
			# 8 possible moves
			possible_moves = [
				(row - 1, col - 1), # up-left
				(row - 1, col), # up
				(row - 1, col + 1), # up-right
				(row, col - 1), # left
				(row, col + 1), # right
				(row + 1, col - 1), # down-left
				(row + 1, col), # down
				(row + 1, col + 1), # down-right
			]

			# normal moves
			for possible_move in possible_moves :
				possible_move_row, possible_move_col = possible_move
				# check if move is in range
				if Square.in_range(possible_move_row, possible_move_col) :
					if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color) :
						# create squares of the new move
						initial = Square(row, col)
						final = Square(possible_move_row, possible_move_col) # piece=piece
						# create new move
						move = Move(initial, final)
						# add valid move to moves
						piece.add_move(move)

			# castling move
			if not piece.moved:			
				# king castling
				right_rook = self.squares[row][7].piece
				if isinstance(right_rook, Rook) and not right_rook.moved :
					for column in range(5, 7) :
						# castling is not possible because there are pieces in between ?
						if self.squares[row][column].has_piece() :
							break

						if column == 6 :
							# add right rook to king
							piece.right_rook = right_rook

							# rook move
							initial = Square(row, 7)
							final = Square(row, 5)
							move = Move(initial, final)
							right_rook.add_move(move)

							# king move
							initial = Square(row, col)
							final = Square(row, 6)
							move = Move(initial, final)
							piece.add_move(move)

				# queen castling
				left_rook = self.squares[row][0].piece
				if isinstance(left_rook, Rook) and not left_rook.moved :
					for column in range(1, 4) :
						# castling is not possible because there are pieces in between ?
						if self.squares[row][column].has_piece() :
							break

						if column == 3 :
							# add left rook to king
							piece.left_rook = left_rook

							# rook move
							initial = Square(row, 0)
							final = Square(row, 3)
							move = Move(initial, final)
							left_rook.add_move(move)

							# king move
							initial = Square(row, col)
							final = Square(row, 2)
							move = Move(initial, final)
							piece.add_move(move)

		if isinstance(piece, Pawn) :
			pawn_moves()

		elif isinstance(piece, Knight) :
			knight_moves()

		elif isinstance(piece, Bishop) :
			straightline_moves([
				(-1, -1), # up-left
				(-1, 1), # up-right
				(1, -1), # down-left
				(1, 1), # down-right
			])

		elif isinstance(piece, Rook) :
			straightline_moves([
				(-1, 0), # up
				(0, -1), # left
				(0, 1), # right
				(1, 0), # down
			])

		elif isinstance(piece, Queen) :
			straightline_moves([
				(-1, -1), # up-left
				(-1, 0), # up
				(-1, 1), # up-right
				(0, -1), # left
				(0, 1), # right
				(1, -1), # down-left
				(1, 0), # down
				(1, 1), # down-right
			])

		elif isinstance(piece, King) :
			king_moves()

	def _create(self) :
		for row in range(ROWS) :
			for col in range(COLS) :
				self.squares[row][col] = Square(row, col)

	def _add_pieces(self, color) :
		row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

		# pawns
		for col in range(COLS) :
			self.squares[row_pawn] [col] = Square(row_pawn, col, Pawn(color))

		# knights
		self.squares[row_other][1] = Square(row_other, 1, Knight(color))
		self.squares[row_other][6] = Square(row_other, 6, Knight(color))

		# bishops
		self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
		self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

		# rooks
		self.squares[row_other][0] = Square(row_other, 0, Rook(color))
		self.squares[row_other][7] = Square(row_other, 7, Rook(color))

		# queen
		self.squares[row_other][3] = Square(row_other, 3, Queen(color))

		# king
		self.squares[row_other][4] = Square(row_other, 4, King(color))