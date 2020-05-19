from Concept import Concept, Rule
from grammar import GrammarRules, GrammarTools
from Agent import Agent


class NLPAgent(Agent):
    def __init__(self):
        super().__init__()

    def induce(self, sentence):
        '''
        Use knowledge of natural language relationships, patterns,
        and heuristics to form a set of rules from this sentence.

        :param sentence: The cause
        :return: A set of rules describing this data
        '''
        rules = NaturalLanguageParser.parse(sentence)
        return rules

    def learn(self, label, rules):
        '''
        Add the induced natural language rules to the concept
        in this agent's model for the specified label.

        :param label: The effect
        :param rules: The rules to add to this model
        '''
        if label not in self._model.keys():
            self._model[label] = NLPConcept(label)

        self._model[label].update(rules[0])
        self._model[label].update(rules[1])

    def reflect(self):
        '''Normalize features based on importance in each category'''
        all_features = dict()
        for label, concept in self._model.items():
            for feature, weight in concept.rules['keyword'].words.items():
                if feature in all_features.keys():
                    all_features[feature] = (all_features[feature][0], all_features[feature][1], all_features[feature][2]+1)
                    if weight > all_features[feature][1]:
                        all_features[feature] = (label, weight, all_features[feature][2])
                else:
                    all_features[feature] = (label, weight, 1)

        for feature in all_features.keys():
            for label, concept in self._model.items():
                if feature in concept.rules['keyword'].words.keys():
                    weight = concept.rules['keyword'].words[feature]
                    concept.rules['keyword'].words[feature] = weight / all_features[feature][1]

        '''Add rules to account for repeated (useless) features'''
        for feature in all_features.keys():
            label, weight, count = all_features[feature]
            if count > 1:
                for concept in self._model.values():
                    if feature in concept.rules['keyword'].words.keys():
                        if 'useless' not in concept.rules.keys():
                            concept.rules['useless'] = NLPUselessFeatureRule("useless")
                        concept.rules['useless'].add_feature(feature, 0.1*concept.rules['keyword'].words[feature])


class NLPConcept(Concept):
    def __init__(self, label):
        super().__init__(label)
        self.rules = {"constraint": NLPFeatureRule("constraint", 0.1),
                      "keyword": NLPFeatureRule("keyword", 1.0)}

    def update(self, rule):
        '''
        Apply the natural language heuristics to update this concept.

        :param rule: The rule used to update this concept
        '''
        model = self.rules[rule.name]
        for word in rule.words:
            if word in model.words:
                '''Specialize: Update the weight of this model'''
                model.words[word] += rule.words[word] * model.weight
            else:
                '''Generalize: Broaden the definition of acceptable perceptions'''
                model.words[word] = rule.words[word] * model.weight


class NLPFeatureRule(Rule):
    def __init__(self, name, weight_factor=1.0):
        super().__init__(name, weight_factor)
        self.words = dict()  # dict{word: weight}

    def apply(self, sentence):
        sentence = NaturalLanguageParser.format(sentence)

        score = 0.0
        for word in sentence:
            if word in self.words.keys():
                score += self.words[word]
        return score


class NLPUselessFeatureRule(Rule):
    def __init__(self, name):
        super().__init__(name)
        self.useless_words = dict()  # dict{word: weight}

    def add_feature(self, word, weight):
        self.useless_words[word] = weight

    def apply(self, sentence):
        sentence = NaturalLanguageParser.format(sentence)

        score = 0.0
        for word in sentence:
            if word in self.useless_words.keys():
                score -= self.useless_words[word]
        return score


class NaturalLanguageParser:
    def __init__(self):
        pass

    @staticmethod
    def format(sentence):
        sentence = GrammarTools.str2words(sentence)
        sentence = GrammarTools.strip_auxiliary_features(sentence)
        out = []
        for word in sentence:
            word = GrammarTools.reduce_to_base(word)
            out = out + [word]
        return out

    @staticmethod
    def parse(sentence):
        '''Format the input'''
        grammar = GrammarRules()
        sentence = NaturalLanguageParser.format(sentence)

        '''Parse the desired data'''
        qwords = []
        constraints = []
        keywords = []
        for word in sentence:
            if word in grammar.prepositions:
                constraints.append(word)
            elif word in grammar.qwords:
                qwords.append(word)
            else:
                keywords.append(word)
        keywords = qwords + keywords

        '''Put into rules'''
        crule = NLPFeatureRule("constraint")
        for word in constraints:
            if word not in crule.words.keys():
                crule.words[word] = 1
            else:
                crule.words[word] += 1

        kwrule = NLPFeatureRule("keyword")
        for word in keywords:
            if word not in kwrule.words.keys():
                kwrule.words[word] = 1
            else:
                kwrule.words[word] += 1

        return (crule, kwrule)

