class CacheLine:
    def __init__(self):
        self.valid = False
        self.tag = None
        self.data = None
        self.dirtyBit = False

    def __repr__(self):
        return f"CacheLine(valid={self.valid}, tag={self.tag}, dirty={self.dirtyBit}, data={self.data})"
