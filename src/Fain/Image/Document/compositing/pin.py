from .protocols import iPin, iPinService

class Pin:
    def __init__(self:iPin, _id:int, _x:int, _y:int):
        self.id = _id
        self.x = _x
        self.y = _y
    def set(self, x, y):
        self.x = x
        self.y = y 

class PinService:
    def __init__(self:iPinService):
        self.current_pin_id = 0
        self.pins:dict[int, iPin] = {}       

    def create(self, x, y)->int:
        self.current_pin_id += 1
        _new_pin = Pin(self.current_pin_id, x, y)
        self.pins[self.current_pin_id] = _new_pin 
        return self.current_pin_id

    def get(self, pin_id):
        if pin_id in self.pins:
            return self.pins[pin_id]
        
    def move(self, pin_id, x, y):
        self.pins[pin_id].set(x, y)