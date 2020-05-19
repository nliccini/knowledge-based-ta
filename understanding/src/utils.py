"""
NAME: Nick Liccini

@brief: Some useful data structures

@detail:
Counter is a data structure for counting and choosing max values
    WeightedCounter is a data structure that uses preferences to count
"""


class Counter:
    def __init__(self):
        self.contents = dict()

    def push(self, key):
        if key not in self.contents.keys():
            self.contents[key] = 0
        self.contents[key] += 1

    def get(self, key):
        return self.contents[key]

    def argmax(self):
        if len(self.contents.keys()) == 0:
            return ''

        out = ''
        max_val = 0
        for key, val in self.contents.items():
            if out == '':
                out = key
            if val > max_val:
                max_val = val
                out = key

        return out


class WeightedCounter(Counter):
    def __init__(self, weights, weighting=1):
        super().__init__()
        self.weights = weights
        self.weighting = weighting

    def weighted_push(self, key, word):
        super().push(key)
        values = self.weights[key]
        if word in values:
            for i in range(0, self.weighting):
                super().push(key)

