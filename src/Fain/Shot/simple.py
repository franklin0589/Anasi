
def get_canvas(width, height, background):
    return Image.new("RGBA", (width, height), background)


ease_none = lambda x:x
ease_cubic_in_out = lambda x: 4*x**3 if x<0.5 else 1 - math.pow(-2 * x + 2, 3) / 2;
ease_sine_in = lambda x: 1 - math.cos((x * math.pi) / 2);
ease_sine_out = lambda x: math.sin((x * math.pi) / 2);
ease_sine_in_out = lambda x: -(math.cos(math.pi * x) - 1) / 2;


# Movement Components
idrag = lambda x, dx, t, duration, speed=1, ease=ease_none: x+clamp(int(ease(translate(t, 0, duration, 0, 1))*dx)*speed, dx, 0)
drag = lambda x, dx, t, duration, speed=1, ease=ease_none: x+clamp(int(ease(translate(t, 0, duration, 0, 1))*dx)*speed, 0, dx)

frames_draw = lambda fc, draw_frame: ([(draw_frame(nbr)) for nbr in range(fc)] if not isinstance(draw_frame,int) else [None])
gif_save = lambda frames, file_name, duration: frames[0].save(file_name, format="GIF", append_images=frames, save_all=True, duration=duration, loop=0)


text_index = lambda t, fc,text_str: int(translate(t, 0, fc, 0, len(text_str)))
anim_text = lambda canvas, text_str, x, y, t, duration, fill, font, anchor =None, align =None: text(canvas, x, y, text_str[:text_index(t,duration,text_str)], fill, font)

def draw_character(canvas, x, y):
    character_png = "data/Sprites/character.png"
    d_png_image(canvas, character_png, x, y)

def say(canvas, x,y, dialogue, t,duration, dist=100, ang=0):
    tx, ty =polar(x,y, dist, math.pi*2*ang/360)
    font = ImageFont.truetype("arial.ttf", 15)
    anim_text(canvas, dialogue, tx, ty, t, duration, "white", font)


triangle_pos = lambda x: (x//10, x%10, -1 if x//10 < 2 else 1,(x//10) % 2, 1 if x % 10 == 0 else 0)
get_t_origin = lambda x, dx, y, dy, _ts, _tr :[lambda tside: (x, lerp(tside/10, dy, y)), lambda tr: (lerp(tr/10,x,dx), y),lambda tside: (dx, lerp(tside/10, y, dy)), lambda tr: (lerp(tr/10,x,dx),dy)][_ts](_tr)

def _blurb_triangle(canvas,x,y,dx,dy,direction_index, fill):
    width = 15
    ts, tr, sub, orient, crn= triangle_pos(direction_index)
    tx, ty = get_t_origin(x,dx,y,dy,ts, tr)
    triangle(canvas,
        tx + 2*width *sub* (1-orient) - crn*2*width*orient,
        ty + (2*width * sub)*orient - crn*2*width*(1-orient),
        tx + width *orient,
        ty + width*(1-orient),
        tx - width*orient *(1-crn),
        ty - width*(1-orient)*(1-crn), fill)

def word_bubble(canvas, x, y, dialogue, direction_index, font, pad, fill, background):
    # pl,pt,pr,pb = (10,10,10,10)
    # index= 29
    if dialogue == "":
        return
    rx,ry,rdx,rdy = get_textbbox(canvas, x, y,dialogue, font)
    _blurb_triangle(canvas, rx,ry,rdx,rdy, direction_index, background)
    srnd_rect(canvas, x-pad[0], y-pad[1], rdx+pad[2], rdy+pad[3], background)
    text(canvas, (x+rdx)/2, (y+rdy)/2, dialogue, fill = fill, font = font)
    
def dialogue(text, draw):
    def functor(t):
        return draw(t, text)
    return functor    

   

def canvas_slides(image, draw):
    def functor(t):
        return draw(image, t)
    return functor

def draw_talking_character(canvas, x, y, dialogue, t,duration, dist=100, ang=0):
    draw_character(canvas, x, y)
    say(canvas,x,y, dialogue, t,duration,dist, ang)

def animated_caption(canvas, paragraph, x,y,t,duration, font, fill,background,pad=(15,15,50,50), anchor="la", align="center"):
    text = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    char_index = int(translate(t, 0, duration, 0, len(paragraph)))
    rx,ry,rw,rh = get_textbbox(text, x, y, paragraph[:char_index], font, anchor, align)
    rect(text, rx-pad[0],ry-pad[1],rw-rx+pad[2],rh-ry+pad[3],background)
    mtext(text, x, y, paragraph[:char_index], fill, font, anchor=anchor,align=align )
    return Image.alpha_composite(canvas, text)

def caption(canvas, paragraph, x,y, font, fill,background,pad=(15,15,20,20), anchor="la", align="center"):
    text = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    rx,ry,rw,rh = get_textbbox(text, x, y, paragraph, font, anchor, align)
    rect(text, rx-pad[0],ry-pad[1],rw-rx+pad[2],rh-ry+pad[3],background)
    mtext(text, x, y, paragraph, fill, font, anchor=anchor,align=align )
    return Image.alpha_composite(canvas, text)
## Images


def gif_engine(name, frame_count, duration, dfs):
    frames = []
    for df in dfs:
        frames += frames_draw(frame_count//len(dfs), df)    
    gif_save(frames, "dist/"+name+".gif", duration)
    
    
basket = {}
def basket_image(image):
    global basket
    if image in basket:
        return basket[image]
    else:
        basket[image] = load_image(f"data\\Images\\{image}")
        return basket[image]

def frame_slides(image, text, draw):
    def functor(t):
        return draw(t, image, text)
    return functor 

slide_gen = lambda s, draw, photo_reel: [setattr(s,"draw",draw), setattr(s, "photo_reel", photo_reel), None][-1]
slide_add = lambda s, index, text: s.slides.append((s.photo_reel[index], text))
slide_render = lambda self, name, fc, dur: gif_engine(name, fc, dur, [frame_slides(i, t, self.draw) for (i, t) in self.slides])
Slides = type("Slides", (object,), {"__init__":slide_gen, "slides":[], "add":slide_add, "render":slide_render})

