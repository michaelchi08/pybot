import numpy as np
import shapely.geometry as sg

def reduce_funcs(*funcs): 
    from functools import wraps
    @wraps
    def wrapper(*args): 
        return reduce(funcs, args)
    return wrapper

class MethodDecorator(object):
    """
    Decorates class methods with wrapped methods. 
    Apply func=to_polygon to each of the methods intersection, union etc. 
    such that the returned value is chained resulting in to_polygon(intersection(x))
    """
    def __init__(self, func, methods):
        self.func = func
        self.methods = methods
    def __call__(self, cls):
        class Wrapped(cls):
            for attr in self.methods:
                if hasattr(cls, attr):
                    setattr(cls, attr, reduce_funcs(getattr(cls, self.func), getattr(cls, attr)))
        return Wrapped

@MethodDecorator(func='to_polygon', methods=('intersection', 'union'))
class Polygon(sg.Polygon): 
    def __init__(self, pts=None, pg=None): 
        assert(pts is not None or pg is not None)
        if pg is not None: 
            sg.Polygon.__init__(self, pg)
        else: 
            sg.Polygon.__init__(self, pts.tolist())

    @classmethod
    def to_polygon(cls, pg): 
        return cls(pg=pg)

    @property 
    def pts(self): 
        return np.array(self.exterior.coords)

class Box(sg.box): 
    def __init__(self, bounds=None, box=None):
        assert(bounds is not None or box is not None)
        if box is not None: 
            sg.box.__init__(self, box)
        else: 
            if type(bounds) == np.ndarray: 
                bounds = bounds.tolist()
            sg.box.__init__(self, bounds)

    @classmethod
    def from_pts(cls, pts): 
        xmin, xmax = np.min(pts[:,0]), np.max(pts[:,0])
        ymin, ymax = np.min(pts[:,1]), np.max(pts[:,1])
        return cls(bounds=[xmin, ymin, xmax, ymax])

if __name__ == "__main__": 
    pts = np.array([[0,0], [0,1], [1,1], [1,0]])
    pts2 = np.array([[0.5,0.5], [0.5,1.5], [1.5,1.5], [1.5,0.5]])
    a = Polygon(pts)
    b = Polygon(pts2)

    print a.pts
    print a.intersection(b).pts

    
