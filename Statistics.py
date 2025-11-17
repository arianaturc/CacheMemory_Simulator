class Statistics:
    def __init__(self):
        self.hits = 0
        self.misses = 0

    def count_hits(self):
        self.hits += 1

    def count_misses(self):
        self.misses += 1

    def get_hit_ratio(self):
        return float(self.hits) / float(self.hits + self.misses)