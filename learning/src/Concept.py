class Concept:
    def __init__(self, label):
        self.rules = dict()
        self.label = label

    def classify(self, perception):
        score = 0.0
        for rule in self.rules.values():
            score += rule.apply(perception)
        return score

    def update(self, rule):
        pass


class Rule:
    def __init__(self, name="UNKNOWN", weight_factor=1.0):
        self.name = name
        self.weight = weight_factor

    def apply(self, perception):
        pass

