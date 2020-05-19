"""
NAME: Nick Liccini

@brief: The interface for an agent's knowledge base can be centered
around multiple contexts that the agent knows

@detail:
Context is an interface for background knowledge

Knowledge represents the knowledge of grammar rules and contexts
"""

from utils import WeightedCounter


class Context:
    def __init__(self):
        self.keywords = dict()
        self.preferences = dict()
        self.topic = 'UNKNOWN'

    '''
    @brief: Use context keywords and preferences to determine which data
    type is requested.
    @detail: Count the number of keywords for each data type, where some
    keywords are weighted more for different keywords.
    '''
    def infer_topic(self, words):
        counter = WeightedCounter(self.preferences)
        for k, v in self.keywords.items():
            for word in words:
                if word in v:
                    counter.weighted_push(k, word)
        self.topic = counter.argmax()

    def score_relevance(self, words):
        score = 0
        for k, v in self.keywords.items():
            for word in words:
                if word in v:
                    score += 1
        return score


class Knowledge:
    def __init__(self):
        self.contexts = []

    def add_to_memory(self, context):
        self.contexts.append(context)

    def infer_context(self, words):
        max_points = 0
        most_relevant = None
        for context in self.contexts:
            points = context.score_relevance(words)
            if points > max_points:
                most_relevant = context
                max_points = points
        return most_relevant

