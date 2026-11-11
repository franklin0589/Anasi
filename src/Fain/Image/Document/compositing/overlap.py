from .protocols import iBounds, iPin, iOverlapService, iPinService

class Bounds:
    def __init__(self:iBounds, width, height):
        self.width  = width
        self.height = height



# overlap is true if
# if new_pin_y-_pin_height < (_pin_y)
# if new_pin_y + new_pin_height > pin_y
# and
# if new_pin_x < (_pin_x + width)
# if new_pin_x + new_pin_width > pin_x


class OverlapService:
    def __init__(self:iOverlapService, pinner:iPinService):
        self.pinner = pinner
        self.bounds:dict[iPin,iBounds] = {}

    def get_bounds(self, pin:iPin, width, height)->iBounds:
        _bounds = Bounds(width, height)
        self.bounds[pin] = _bounds
        return _bounds
    
    def get_overlap(self, _opin:iPin):
        if _opin not in self.bounds:
            raise AttributeError("Pin not found in bounds")
        _opin_bounds = self.bounds[_opin]
        overlaps:list[iPin] = []
        for _npin in self.bounds:
            _npin_bounds =self.bounds[_npin]
            pin_y_overlap = _npin.y+_npin_bounds.height >_opin.y  and _npin.y  < _opin.y +_opin_bounds.height
            pin_x_overlap = _npin.x+_npin_bounds.width > _opin.x  and _npin.x < _opin.x + _opin_bounds.width
            if pin_y_overlap and pin_x_overlap:
                overlaps += [_npin]
        return overlaps