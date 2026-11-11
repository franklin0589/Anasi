from ..Math.context import *

class Text(Object):
    def update(self, text, color):
        self.text = text
        self.color = color
        self.offset = Vector2D(1,2)
        return self
    def render(self, board: Board):
        board.start_pen()
        extents = board.text_bb(self.text, 4)
        back_origin = Vector2D(0, -3)
        board.rect(back_origin, 80, max(extents.height, 20), Color.WHITE)
        if "\n" in self.text:
            for idx, line in enumerate(self.text.split("\n")):
                _l = mat_translate(self.offset, 0, idx*4 )
                _l = Vector2D(*u_hvec(_l))
                board.text(_l,line,self.color,4)
        
        else:
            board.text(self.offset,self.text,self.color,4)
        board.finish_pen()

class Sprite(Object):
    def update(self, ref, index, square, margins =[2,2,30,30]):
        self.img2 = load_image_png(ref)
        self.index = index
        self.square_pack = square
        self.row_size = 5
        self.margins = margins
        return self
    def render(self, board):
        board.start_pen()
        board.pen.rectangle(*self.margins)
        board.pen.clip()
        position = Vector2D(
            -(self.square_pack)*(self.index%self.row_size), 
            -(self.square_pack)*(self.index//self.row_size))
        board.set_image(self.img2, position)
        board.fill_clip()
        board.finish_pen()


class Body(Object):
    def update(self, nbr):
        self.ref = "data/limbs.png"
        self.frame = nbr
        return self

    def render(self, board: Board):
        #Hips
        board.start_pen()
        Sprite(0,16,0).update(self.ref,10,32).draw(board)
        # RLeg
        Sprite(-10,28,0).update(self.ref,5,32).draw(board)
        # LLeg
        Sprite(10,28,0).update(self.ref,5,32).draw(board)
        # Torso
        Sprite(1,-10,0).update(self.ref,12,32).draw(board)
        # RLeg
        Sprite(-18,-4,0).update(self.ref,5,32).draw(board)
        # LLeg
        Sprite(18,-4,0).update(self.ref,5,32).draw(board)
        # Head 
        Sprite(0,-34,0).update(self.ref,0,32).draw(board)
        
        board.finish_pen()

class Ball(Object):
    def update(self, color):
        self.color = color
        return self

    def render(self, board: Board):
        board.circle(ORIGIN, 15, self.color)
        ...