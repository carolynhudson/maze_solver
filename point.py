class Point:
    def __init__(self, x : float = 0, y: float = 0):
        self.x = x
        self.y = y
    
    def coord(self) -> tuple[float, float]: return (self.x, self.y)
        