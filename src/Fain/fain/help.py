import math

import tkinter as tk

import time


def sleep(delaySeconds:int):
    time.sleep(delaySeconds)

def sleep_min(delayMinutes:int):
    time.sleep(delayMinutes*60)


# Window Tools
def tkinter_setup(w, h):
    root = tk.Tk()
    root.geometry(f"{w}x{h}+0+0")
    canvas = tk.Canvas(root, background="white")
    canvas.pack(expand=True, fill="both")

    return root, canvas

create_circle = lambda c, x, y, r, *args, **kwargs: c.create_oval(x-r, y-r, x+r, y+r, *args, **kwargs)
start_window = lambda window : window.mainloop()

clear_canvas = lambda canvas: canvas.delete("all")


# Functools
success = lambda x, exp, r: r if x == exp else Exception("Set_Method_Return Invalid")

# Update Attribute
updateattr = lambda s, v: [setattr(s, k, v) for k,v in v.items()] # type: ignore

# Math Equations
identity = lambda x:x
cosine = lambda x : math.cos(x * (math.pi * 2)/ 360)
sine = lambda x : math.sin(x * (math.pi * 2) / 360)
lerp = lambda a, b, t: a + t*(b-a)
vec_add = lambda vec1, vec2: [x+y for x,y in zip(vec1, vec2)]
polar_cast = lambda len, ang: (len*cosine(ang), len*sine(ang))