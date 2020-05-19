"""
NAME: Nick Liccini

@brief: The component of knowledge that handles interpreting an input

@detail: The cognitive architecture is a production system. The deliberation
model for the production system is based on the Soar architecture. The production
system is preloaded with domain knowledge.

Here, the domain knowledge is represented by a Context subclass. The Context
contains Cases for experience and information stored as an unordered set.
Case-based reasoning is applied to retrieve the most similar case based on
the input. Each Case subclass implements its rules for comparing data
"""


class CognitiveArchitecture:
    def __init__(self):
        self.deliberation = Soar()
        self.reaction = Reaction()

    def preload(self, context):
        self.deliberation.preload_domain(context.name, context.knowledge)
        self.reaction.preload_reaction(context.name, context.reaction)


class Soar:
    def __init__(self):
        self.episodic_knowledge = dict()

    def preload_domain(self, context_name, knowledge):
        self.episodic_knowledge[context_name] = knowledge

    def retrieve(self, working_memory, context):
        closest_score = 0.0
        closest_match = None

        # Find the closest matching case in memory using the case's similarity/comparison function
        alternative_cases = dict()
        data = working_memory.GetData()
        for case in self.episodic_knowledge[context.name]:
            match, score = case.compare(data)
            if match and score == closest_score:
                alternative_cases[case.label] = case
            if match and score > closest_score:
                closest_score = score
                closest_match = case

        # Find all relevant cases (cases having the same label)
        if closest_score > 0.0:
            relevant_cases = []
            for case in self.episodic_knowledge[context.name]:
                if closest_match.label == case.label:
                    relevant_cases.append(case)

        # Remove all cases that have the same label as the closest match
        same_cases = []
        for label, case in alternative_cases.items():
            if label == closest_match.label:
                same_cases.append(label)
        for label in same_cases:
            alternative_cases.pop(label)

        # If there were multiple conflicting cases, an impasse occurred
        if len(alternative_cases.items()) > 0:
            return None

        return closest_match

    def adapt(self, case, answer):
        # Fit the answer's information into the generalized case
        pass

    def evaluate(self, case):
        # Evaluate how correct this adapted case is
        pass

    def store(self, case):
        # If this case is not in memory, add it
        pass

"""
@brief: Episodic knowledge collection organized by context. 
Episodic knowledge consists of experiences from each context
Episodic knowledge also consists of domain knowledge information

Case objects make up the episodic knowledge
"""
class Case:
    def __init__(self):
        self.label = None

    def compare(self, to_comp):
        '''
        Compares this case to the input

        :param to_comp: input case to compare against
        :return: the score result, a tuple of (match, score) where
        match indicates if to_comp was at least close enough and
        score indicates this similarity based on the similarity
        function of this case
        '''
        pass


"""
@brief: Reaction level of cognition. Preloaded with a default
response (in the form of a case) based on the context
"""
class Reaction:
    def __init__(self):
        self.reactions = dict()

    def preload_reaction(self, context_name, reaction):
        self.reactions[context_name] = reaction

    def react(self, context):
        # Provide a default action based on the context
        return self.reactions[context.name]
