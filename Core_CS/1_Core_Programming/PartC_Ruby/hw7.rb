# Programming Languages Part C - Ruby
# Tetris OO enhancement example with mixins and blocks

class Piece
  attr_accessor :rotations, :base_score

  def initialize(rotations, base_score = 1)
    @rotations = rotations
    @base_score = base_score
  end

  def self.next_piece
    Piece.new([[[0, 0], [1, 0], [0, 1], [1, 1]]], 5) # Example Square piece
  end
end

class Board
  attr_accessor :grid, :score

  def initialize
    @grid = Array.new(20) { Array.new(10, nil) }
    @score = 0
  end

  # Demonstrating duck typing and mixin logic
  def place_piece(piece, x, y)
    piece.rotations.first.each do |point|
      dx, dy = point
      @grid[y + dy][x + dx] = piece # Places piece directly
    end
    @score += piece.base_score
  end

  def print_board
    @grid.each do |row|
      row.each do |cell|
        print cell ? "[X]" : "[ ]"
      end
      puts
    end
    puts "Score: #{@score}"
  end
end

# An enhanced tetris game that allows for "cheat" pieces
module CheatMode
  def activate_cheat!
    @cheat_mode = true
  end

  def next_piece
    if @cheat_mode
      @cheat_mode = false
      Piece.new([[[0, 0]]], 100) # Cheater 1x1 block
    else
      super
    end
  end
end

class MyTetrisGame
  # We can extend classes or prepend modules in Ruby
  # to dynamically alter behavior
  prepend CheatMode

  attr_accessor :board

  def initialize
    @board = Board.new
    @cheat_mode = false
  end

  def next_piece
    Piece.next_piece
  end

  def play_turn
    piece = next_piece
    @board.place_piece(piece, 4, 0)
    @board.print_board
  end
end

if __name__ == '__main__'
  game = MyTetrisGame.new
  puts "Normal Turn:"
  game.play_turn
  
  puts "\nCheat Turn:"
  game.activate_cheat!
  game.play_turn
end
