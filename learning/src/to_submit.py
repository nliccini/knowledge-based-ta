"""
NAME: Nick Liccini
"""

import sys
import getopt
from TestAdapter import TestAdapter


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


class GrammarRules:
    def __init__(self):
        self.qwords = ['what', 'where', 'when', 'why', 'how', 'who', 'whom', 'which']
        self.qverbs = ['is', 'are', 'was', 'were', 'do', 'does', 'did',
                       'have', 'has', 'had', 'can', 'could', 'should',
                       'would', 'will', 'be']

        self.articles = ['a', 'an', 'the']
        self.pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'us',
                         'me', 'my', 'mine', 'your', 'yours', 'him', 'his',
                         'her', 'hers', 'their', 'theirs', 'our', 'ours',
                         'them']
        self.possessive_pronouns = ['my', 'mine', 'your', 'yours', 'his',
                                    'hers', 'theirs', 'our', 'ours']
        self.prepositions = ['for', 'on', 'by', 'with', 'of', 'to', 'from',
                             'about', 'in', 'into', 'onto', 'after', 'before',
                             'during', 'within', 'without', 'above', 'below',
                             'until', 'till', 'as', 'during']
        self.conjunctions = ['and', 'or', 'but', 'if', 'so', 'next']
        self.adjectives = ['many', 'much', 'this', 'that', 'there', 'any']
        self.forms_of_be = ['be', 'is', 'are', 'were', 'was', 'will', 'am']
        self.trivial_verbs = ['go', 'going', 'gone', 'do', 'doing', 'done', 'did', 'get',
                              'give']


class GrammarTools:
    def __init__(self):
        self.rules = GrammarRules()

    @staticmethod
    def strip(words, l):
        out = []
        for word in words:
            if word not in l:
                out.append(word)
        return out

    @staticmethod
    def remove_numerals(words):
        out = []
        for word in words:
            if not word.isnumeric():
                out.append(word)
        return out

    @staticmethod
    def reduce_to_base(word):
        rules = GrammarRules()
        if word in rules.prepositions or word in rules.qwords:
            return word

        # Possessive
        if word[-2] == '\'' and word[-1] == 's':
            word = word[:-2]

        # Plural
        if word[-1] == 's':
            if len(word) > 4:
                w = word[-4]
            else:
                w = ''

            x = word[-3]
            y = word[-2]
            z = word[-1]
            if y == 'e' and z == 's':
                if (x == 's') or (w == 's' and x == 's') or (w == 's' and x == 'h') or (w == 'c' and x == 'h') or (
                        x == 'x') or (x == 'z'):
                    word = word[:-2]
            elif x == 'v' and y == 'e' and z == 's':
                word = word[:-3] + 'f'
            elif x == 'i' and y == 'e' and z == 's':
                word = word[:-3] + 'y'
            elif x == 'o' and y == 'e' and z == 's':
                word = word[:-2]
            elif y == 'o':
                word = word[:-1]
            elif y is not 's':
                word = word[:-1]

        # Past tense
        if len(word) > 3 and word[-3] == 'e' and word[-2] == 'e' and word[-1] == 'd':
            pass
        elif len(word) > 3 and word[-2] == 'e' and word[-1] == 'd' and word[-3] not in 'aeiouwt':
            word = word[:-1]
        elif len(word) > 3 and word[-2] == 'i' and word[-1] == 'e' and word[-3] not in 'd':
            word = word[:-3]
            word = word + 'y'
        elif word[-2] == 'e' and word[-1] == 'd':
            word = word[:-2]

        # Gerunds
        if len(word) > 4 and word[-3] == 'i' and word[-2] == 'n' and word[-1] == 'g':
            word = word[:-3]

        # Double letters
        if word[-2] == 't' and word[-1] == 't':
            word = word[:-1]

        return word

    @staticmethod
    def strip_auxiliary_features(sentence):
        grammar = GrammarRules()
        sentence = GrammarTools.strip(sentence, grammar.articles)
        sentence = GrammarTools.strip(sentence, grammar.conjunctions)
        sentence = GrammarTools.strip(sentence, grammar.pronouns)
        sentence = GrammarTools.strip(sentence, grammar.possessive_pronouns)
        sentence = GrammarTools.strip(sentence, grammar.adjectives)
        sentence = GrammarTools.strip(sentence, grammar.qverbs)
        sentence = GrammarTools.strip(sentence, grammar.forms_of_be)
        sentence = GrammarTools.strip(sentence, grammar.trivial_verbs)
        sentence = GrammarTools.remove_numerals(sentence)
        return sentence

    @staticmethod
    def str2words(str):
        return str.lower().split(' ')


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
                        concept.rules['useless'].add_feature(feature, 0.1 * concept.rules['keyword'].words[feature])


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


def _train_agent(training_raw):
    """
    Build a model from the raw training data

    :param training_raw:
    :return:
    """
    agent = NLPAgent()
    for row in training_raw:
        '''Extract the training data'''
        label = row[0]
        question = row[1]

        '''Induce some rules from the input'''
        rules = agent.induce(question)

        '''Incrementally update the concept using these rules'''
        agent.learn(label, rules)

    agent.reflect()
    model = agent.get_model()
    return model


def main(argv):
    """
        This is your test main. This main WILL NOT be used by the autograder.
        When grading your agent, we will call _train_agent() and _train_agent() from our autograder.
        DO NOT MAKE ANY CHANGES IN THIS FUNCTION THAT ARE REQUIRED BY YOUR AGENT TO FUNCTION.
    """
    print(__doc__)

    train_test_filename = argv[0]
    training_questions = []
    test_questions = []
    header = True
    print("Opening test file: " + train_test_filename)
    try:
        with open(train_test_filename, "r", encoding='ascii', errors='backslashreplace') as data:
            for line in data:
                if header:
                    header = False
                    continue
                line = line.split(',')
                training_questions.append([line[0].lower().strip(), line[1].lower().strip()])
                test_questions.append([line[0].lower().strip(), line[2].lower().strip()])
    except IOError as err:
        print("Failure opening or reading test questions filename: " + str(err))
        sys.exit(-1)


    print("\nTraining...")
    training_data = _train_agent(training_questions)
    jw_adapter = TestAdapter(training_data)
    print("\nTesting...")
    total_questions = 0
    correct_answers = 0
    results = {}
    for row in test_questions:
        label = row[0]
        test_question = row[1]
        result_dict = jw_adapter.ask_question(test_question)
        del result_dict['question']
        result_label = list(result_dict.keys())[0]
        print(test_question+"\n\tGround Truth: "+label+"\n\tResult: "+result_label)
        results.update({'test_question':test_question, 'label':label, 'result_label':result_label})
        total_questions += 1
        if label == result_label:
            correct_answers += 1
        print("\t"+str(label==result_label).upper())
    print("\nResults:")
    print("\tTotal Questions: "+str(total_questions))
    print("\tCorrect Answers: "+str(correct_answers))
    sys.exit(0)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
