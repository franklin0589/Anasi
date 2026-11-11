from enum import Enum
from typing import Protocol
import cairo



class iColor(Protocol):
    r:float
    g:float
    b:float
    a:float
    values: tuple[float,float, float,float]    

class iCFont(Protocol):
    name:str
    size:int
    slant:cairo.FontSlant
    weight:cairo.FontWeight


