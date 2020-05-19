"""
NAME: Nick Liccini

@brief:

@detail:
"""


from knowledge import Knowledge
from cs4635context import CS4635Context


class StudentAgent:
    def __init__(self, verbose):
        self._verbose = verbose

        self.knowledge = Knowledge()
        self.knowledge.add_to_memory(CS4635Context())

        self.invalid_list = list()

    def input_output(self, word_list):
        # Understand
        context = self.knowledge.infer_context(word_list)
        working_memory = self.knowledge.understand(word_list, context)

        if working_memory is None:
            self.invalid_list.append(word_list)

        # Classify
        case = self.knowledge.classify(working_memory, context)

        _intent = case.label
        return _intent

