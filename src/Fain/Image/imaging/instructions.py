from .protocol import iBoard
from typing import Callable


class InstructionService:
    def __init__(self, board:iBoard):
        self.board = board
        self.instructions:list[Callable] = []
        
    def add_instruction(self, instruction):
        self.instructions += [instruction]

    def render(self):
        for instr in self.instructions:
            instr(self.board)
        return self.board.render_image()

def get_instruct(board:iBoard):
    return InstructionService(board)