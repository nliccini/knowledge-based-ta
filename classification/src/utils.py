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


def compare_words(words1, words2):
    primary = words1
    secondary = words2
    if len(words2) > len(words1):
        primary = words2
        secondary = words1

    score = 0.0
    for i in range(len(primary)):
        if i >= len(secondary):
            break
        if secondary[i] in primary:
            score += 1.0
    score = score / len(primary)
    return score


def convert_numerals(words):
    numerals = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth',
                'tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth']
    spelled_out_numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
                           'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    converted = []
    i = 0
    while i < len(words):
        for j in range(len(numerals)):
            if words[i] == spelled_out_numbers[j]:
                converted.append(numbers[j])
                break
            if words[i] == numerals[j]:
                if i+1 < len(words):
                    converted.append(words[i+1])
                    i += 1
                converted.append(numbers[j])
                break
        else:
            converted.append(words[i])
        i += 1
    return converted


def remove_numerals(words):
    words = convert_numerals(words)
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    out = []
    for word in words:
        if word not in numbers:
            out.append(word)
    return out

