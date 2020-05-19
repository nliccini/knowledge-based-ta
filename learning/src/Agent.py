class Agent:
    def __init__(self):
        '''
        Agent.model: dict(label: concept)
        '''
        self._model = dict()

    def get_model(self):
        return self._model

    def induce(self, cause):
        '''
        Induction is the process of determining a rule (hypothesis)
        from a cause (sentence) and an effect (label).

        Using knowledge of pattern recognition in natural language,
        the agent produces a new rule for this label.

        :param cause:
        :return: A rule describing this data
        '''
        pass

    def learn(self, effect, rules):
        '''
        Use the effect and and induced rules to update the model
        the agent has about the world

        :param effect:
        :param rules:
        '''
        pass

    def reflect(self):
        '''
        Reflect on the model that this agent has built and
        update any rules as needed
        '''
        pass
