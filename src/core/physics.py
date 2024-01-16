class Gravity:
    def __init__(self, g):
        self.g = g

    def apply(self, obj):
        obj.shift(0, self.g)
