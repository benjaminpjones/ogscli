from typing import NamedTuple
from string import ascii_uppercase


LETTERS = ascii_uppercase.replace("I", "")


class Coordinate(NamedTuple):
  x: int
  y: int

class Grid:
  def __init__(self, width, height, v=None):
    self.width = width
    self.height = height
    self.arr = [[v for _ in range(width)] for _ in range(height)]

  def neighbors(self, pos: Coordinate):
    x, y = pos
    ret = []

    if x > 0:
      ret.append(Coordinate(x-1, y))
    if y > 0:
      ret.append(Coordinate(x, y-1))
    if x < self.width - 1:
      ret.append(Coordinate(x+1, y))
    if y < self.height - 1:
      ret.append(Coordinate(x, y+1))
 
    return ret

  def __getitem__(self, pos: Coordinate):
    return self.arr[pos.y][pos.x]

  def __setitem__(self, pos: Coordinate, v):
    self.arr[pos.y][pos.x] = v

  def __str__(self):
    return "\n".join([" ".join([str(v) for v in row]) for row in self.arr])


def get_group(g: Grid, pos: Coordinate):
  seen = set()
  color = g[pos]
  
  def helper(pos):
    if g[pos] != color:
      return
    if pos in seen:
      return
    seen.add(pos)
    for neighbor in g.neighbors(pos):
      helper(neighbor)

  helper(pos)
  return seen

def get_outer_border(grid: Grid, group: set[Coordinate]):
  expanded_group = { neighbor for pos in group for neighbor in grid.neighbors(pos) }
  return expanded_group - group


class Baduk:

  def __init__(self, width, height):
    self.board = Grid(width, height, 0)
    self.active_player = 1

  def has_liberties(self, pos):
    border = get_outer_border(self.board, get_group(self.board, pos))
    return any(self.board[pos] == 0 for pos in border)   

  def remove_group(self, pos):
    g = get_group(self.board, pos)
    for pos in g:
      self.board[pos] = 0


  def play_move(self, pos):
    self.board[pos] = self.active_player
    opponent = 2 if self.active_player == 1 else 1
    for neighbor in self.board.neighbors(pos):
      if self.board[neighbor] == opponent:
        if not self.has_liberties(neighbor):
          self.remove_group(neighbor)
          
    self.active_player = opponent

  def __str__(self):
    MAP = [".", "X", "O"]
    ret = []
    letter_coords = "    " + " ".join(LETTERS[0:self.board.width])
    ret.append(letter_coords)

    for i, row in enumerate(self.board.arr):
      number_coords = f"{self.board.height - i: >3}"
      ret.append(number_coords + " " + " ".join(MAP[val] for val in row) + number_coords)
    ret.append(letter_coords)
    return "\n".join(ret)


if __name__ == "__main__":
  g = Grid(3, 3)

  g[Coordinate(1, 0)] = 1
  g[Coordinate(1, 1)] = 1
  g[Coordinate(1, 2)] = 1

  print(g)
  print(get_group(g, Coordinate(0, 1)))

  middle_group = get_group(g, Coordinate(1, 1))
  print(get_outer_border(g, middle_group))

  b = Baduk(3, 3)
  print(b, "\n")
  b.play_move(Coordinate(0, 0))
  print(b, "\n")
  b.play_move(Coordinate(0, 1))
  print(b, "\n")
  b.play_move(Coordinate(1, 1))
  print(b, "\n")
  b.play_move(Coordinate(1, 0))
  print(b, "\n")

