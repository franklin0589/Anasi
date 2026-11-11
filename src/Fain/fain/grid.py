from .context import *
import itertools as It



# Grid Structure and Method
create_grid = lambda s, r, c: [updateattr(s, {"row":r,"column": c,"buffer": Buffer(r*c)   }),None][-1]
display_row = lambda tup:  " ".join([str(char) if char != None else "0" for char in tup])+"\n"
Grid = type("Grid", (object,), {"__init__":create_grid,'__str__':lambda s: "\n".join([display_row(tup) for tup in It.batched(s.buffer.data, s.row)])})



lreplace = lambda l, index, object: (list.pop(l, index), list.insert(l, index, object), l)[-1]


index_2D = lambda r, c, len: c + r*len
put_2D = lambda g, r, c, obj: lreplace(g.buffer.data, index_2D(r, c, g.column), obj)
delete_2D = lambda g, r, c: put_2D(g, r, c, None)
get_2D = lambda g,r,c: g.buffer.data[index_2D(r,c,g.column)]
move_2D = lambda g,r,c, nr,nc: [put_2D(g, nr, nc, get_2D(g, r, c)), delete_2D(g, r, c), None][-1] 



create_node = lambda s, grid, n, pos: [success(setattr(s, "grid", grid) or setattr(s, "char", n) or setattr(s, "pos", pos) , None, None), put_2D(grid, pos.x, pos.y, s), None][-1]# type: ignore
move_node = lambda s, x, y: (move_2D(s.grid, s.pos.x, s.pos.y, x, y) or s.pos.set(x, y))
Node = type("Node", (object,) , {"__init__":create_node, "move":move_node, "__str__":lambda s: s.char})