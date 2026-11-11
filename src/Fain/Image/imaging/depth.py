from .board import Board

class DepthService:
    def __init__(self, board:Board, focal_length):
        self.focal_length = focal_length
        self.board = board
    
    def calculate(self, depth):
        return self.focal_length / (self.focal_length + depth)
    
    def set_board_depth(self, depth):
        self.board.save()
        _persp = self.calculate(depth)
        self.board.set_pen(_persp,_persp)
        yield 
        self.board.load()