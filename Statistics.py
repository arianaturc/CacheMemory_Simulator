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

    def display_statistics(self):
        print("*" * 25)
        print(f"Cache Statistics ")
        print("*" * 25)
        print("Cache Hits:", self.hits)
        print("Cache Misses:", self.misses)
        print(f"Cache Hit Ratio:{self.get_hit_ratio(): .2f}")