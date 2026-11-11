import math

clamp = lambda x, min_, max_: max(min(x, max_), min_)

class Ease:
    LINEAR = lambda x:x
    CUBIC_IN_OUT = lambda x: 4*x**3 if x<0.5 else 1 - math.pow(-2 * x + 2, 3) / 2
    SINE_IN= lambda x: 1 - math.cos((x * math.pi) / 2)
    SINE_OUT = lambda x: math.sin((x * math.pi) / 2)
    SINE_IN_OUT = lambda x: -(math.cos(math.pi * x) - 1) / 2

class Tween:
    def __init__(self, value, target, steps = 10):
        self.start = value
        self.target = target
        self.steps = steps
        self.easing_function = Ease.CUBIC_IN_OUT 
    
    def easing(self, t):
        return self.easing_function(t)
        
    def loop(self):
        def tween(t,d,s):
            return s + (self.easing(t)) * (d - s) 
        for i in range(self.steps):
            t = i/self.steps
            if isinstance(self.start, list):
               yield [tween(t,self.target[i],self.start[i])for i in range(len(self.start))]
            else:
                yield tween(t, self.target, self.start)

class Twine:
    def __init__(self, value):
        self.tweens = []
        self.start_value = value
    def add_tweens(self, next_value, steps):
        self.tweens += [Tween(self.start_value, next_value, steps)]
        self.start_value = next_value
    def generator(self):
        for tween in self.tweens:
            for inc in tween.loop():
                yield inc
        yield self.start_value