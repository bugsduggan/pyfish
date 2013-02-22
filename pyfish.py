#!/usr/bin/python2

import sys
from argparse import *
from subprocess import Popen, PIPE

def main(argv=None):
  if argv is None:
    argv = sys.argv
  parser = ArgumentParser(description='A simple Stockfish UI')

  # Add command line options
  parser.add_argument('--debug', action='store_true', help='Displays all of the output from the engine')
  parser.add_argument('-i', '--interactive', nargs='?', type=str, choices=['w', 'b'], help='Play interactively (can specify starting as white or black)', const='w')
  parser.add_argument('-b', '--book', metavar='PATH', help='The path to the book file', default='./book.bin')
  parser.add_argument('-e', '--engine', metavar='PATH', help='The path to the engine', default='./stockfish')
  parser.add_argument('-d', '--display', action='store_true', help='Output the board state graphically')
  parser.add_argument('moves', nargs='*', help='The starting board state as a list of moves', default=[])

  args = parser.parse_args()
  if args.debug:
    print args
  if args.interactive is None:
    if args.display:
      b = Board(args.moves)
      b.display()
    print __best_move__(args.moves, args.debug, args.engine, args.book)
  else:
    # Woo interactive mode!
    b = Board()
    playing = True
    moves = []
    if args.interactive is 'b':
      move = __best_move__(debug=args.debug, engine=args.engine, book=args.book)
      sys.stdout.write('\n  Opponent plays ' + move + '\n')
      moves.append(move)
      b.apply_move(move)
    while playing:
      b.display()
      move = raw_input('>> ')
      if move == 'quit': return 0
      moves.append(move)
      b.apply_move(move)
      move = __best_move__(moves=moves, debug=args.debug, engine=args.engine, book=args.book)
      sys.stdout.write('\n  Opponent plays ' + move + '\n')
      moves.append(move)
      b.apply_move(move)

  return 0

class Board:

  def __init__(self, moves=[]):
    self.board = []
    for i in range(8):
      row = []
      for j in range(8):
        # A8 is white as is every i+j which is even
        if (i+j) % 2 is 0:
          row.append(NullPiece(Color.WHITE))
        else:
          row.append(NullPiece(Color.BLACK))
      self.board.append(row)
    # now we need to add the sets of pieces
    self.board[0][0] = Rook(Color.BLACK)
    self.board[0][1] = Knight(Color.BLACK)
    self.board[0][2] = Bishop(Color.BLACK)
    self.board[0][3] = Queen(Color.BLACK)
    self.board[0][4] = King(Color.BLACK)
    self.board[0][5] = Bishop(Color.BLACK)
    self.board[0][6] = Knight(Color.BLACK)
    self.board[0][7] = Rook(Color.BLACK)
    for i in range(8):
      self.board[1][i] = Pawn(Color.BLACK)
      self.board[6][i] = Pawn(Color.WHITE)
    self.board[7][0] = Rook(Color.WHITE)
    self.board[7][1] = Knight(Color.WHITE)
    self.board[7][2] = Bishop(Color.WHITE)
    self.board[7][3] = Queen(Color.WHITE)
    self.board[7][4] = King(Color.WHITE)
    self.board[7][5] = Bishop(Color.WHITE)
    self.board[7][6] = Knight(Color.WHITE)
    self.board[7][7] = Rook(Color.WHITE)

    # now we need to apply any moves from that thar list
    for move in moves:
      self.apply_move(move)

  def apply_move(self, move):
    m = __parse_move__(move)
    fx = m[0][0]
    fy = m[0][1]
    tx = m[1][0]
    ty = m[1][1]
    self.board[ty][tx] = self.board[fy][fx]
    if (fx + fy) % 2 is 0:
      self.board[fy][fx] = NullPiece(Color.WHITE)
    else:
      self.board[fy][fx] = NullPiece(Color.BLACK)

  def display(self):
    sys.stdout.write('\n  ')
    for i in range(8):
      sys.stdout.write('+---')
    sys.stdout.write('+\n')
    for row in self.board:
      sys.stdout.write('  ')
      for p in row:
        sys.stdout.write('| ' + p.get_char() + ' ')
      sys.stdout.write('|\n  ')
      for i in range(8):
        sys.stdout.write('+---')
      sys.stdout.write('+\n')
    sys.stdout.write('\n')

def __query_engine__(moves=[], debug=False, engine='./stockfish', setup_str='uci\nsetoption name Book File value ./book.bin\nsetoption name OwnBook value true\nisready\n', cmd_str='go\n'):
  p = Popen(engine, stdin=PIPE, stdout=PIPE)
  move_str = 'position startpos moves'
  for move in moves:
    move_str = move_str + ' ' + move
  move_str = move_str + '\n'
  result = p.communicate(setup_str + move_str + cmd_str)[0].split('\n')
  if debug:
    for line in result:
      print 'SERVER> ' + line
  return result

def __best_move__(moves=[], debug=False, engine='./stockfish', book='./book.bin'):
  res = __query_engine__(moves=moves, debug=debug, engine=engine, setup_str='uci\nsetoption name Book File value ' + book + '\nsetoption name OwnBook value true\nisready\n')
  for line in res:
    if line.startswith('bestmove'):
      return line.split(' ')[1]

def __parse_move__(move):
  # this should get a move like a2a3 and return a tuple like ((0, 6), (0, 5))
  mx = move[0:2]
  my = move[2:4]
  return (__parse_loc__(mx), __parse_loc__(my))

def __parse_loc__(loc):
  # takes a location in the form a7 and return a tuple of the form (0, 1)
  r = ord(loc[0]) - ord('a')
  f = abs(int(loc[1]) - 8)
  return (r, f)

class Color:
  WHITE = 1
  BLACK = 2

class Piece:
  def __init__(self, color):
    self.color = color

# Pieces, yo
class NullPiece(Piece):
  def get_char(self):
    if self.color is Color.WHITE:
      return ' '
    else:
      return '.'

class Rook(Piece):
  def get_char(self):
    if self.color is Color.WHITE:
      return 'R'
    else:
      return 'r'

class Knight(Piece):
  def get_char(self):
    if self.color is Color.WHITE:
      return 'N'
    else:
      return 'n'

class Bishop(Piece):
  def get_char(self):
    if self.color is Color.WHITE:
      return 'B'
    else:
      return 'b'

class Queen(Piece):
  def get_char(self):
    if self.color is Color.WHITE:
      return 'Q'
    else:
      return 'q'

class King(Piece):
  def get_char(self):
    if self.color is Color.WHITE:
      return 'K'
    else:
      return 'k'

class Pawn(Piece):
  def get_char(self):
    if self.color is Color.WHITE:
      return 'P'
    else:
      return 'p'

if __name__ == '__main__':
  sys.exit(main())
