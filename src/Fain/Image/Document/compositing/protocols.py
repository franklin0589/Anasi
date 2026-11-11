from typing import Protocol


class iPin(Protocol):
    id:int
    x:int
    y:int

class iBounds(Protocol):
    width:int
    height:int
    

class iPinService(Protocol):
    current_pin_id:int
    pins:dict[int, iPin]
    
    def create(self, x:int, y:int)->iPin:...
    def move(self, _id, x:int, y:int)->iPin:...
    def get(self, _id:int)->iPin: ...

class iOverlapService(Protocol):
    pinner:iPinService
    bounds:dict[iPin,iBounds]

    def get_bounds(self, x, y, width, height)->iPin:...
    def get_overlap(self, pin:iPin):...
    

class iArea(Protocol):
   pinner:iPinService 