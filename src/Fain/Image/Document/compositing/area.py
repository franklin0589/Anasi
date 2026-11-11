from .protocols import iPin, iBounds
from .pin import PinService
from .overlap import OverlapService





class Area:
    def __init__(self, _pin: iPin, _bounds:iBounds):
        self.pin = _pin
        self.bounds = _bounds

    def set_instruct(self, instruction):
        self.instruct.add_instruction(instruction)

    def render(self):
        return self.instruct.render()
        

class Table:
    def __init__(self):

        self.pinner = PinService()
        self.overlapper = OverlapService(self.pinner)
        
    def get_board_frame(self, x, y, width, height):
        _pin = self.pinner.get_pin(x,y)
        _bounds = self.overlapper.get_bounds(_pin, width, height)
        return _board
    
    
    
