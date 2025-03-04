class Point:
    def __init__(self, x : float = 0, y: float = 0):
        self.x = x
        self.y = y
    
    def coord(self) -> tuple[float, float]: return (self.x, self.y)
        
    def __add__(self, other) -> "Point":
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Point(self.x + other, self.y + other)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other) -> "Point":
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Point(self.x - other, self.y - other)
        else:
            raise TypeError("Unsupported operand type for -")
