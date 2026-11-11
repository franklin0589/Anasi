from .help import *
from .event import *

# Buffer Structure and Method
create_buffer = lambda s, i: success(setattr(s, "data", [None]* i), None, None) # type: ignore
Buffer = type("Buffer", (object,), {"__init__":create_buffer, "__str__":lambda s: str(s.data)})

## Position Structure and Method
create_position = lambda s, x, y: success(setattr(s, "x", x) or setattr(s, "y", y), None, None) #type: ignore
Position = type("Position", (object,), {"__init__": create_position, "get":lambda s: (s.x,s.y), "set":lambda s, x, y: create_position(s,x,y)})
