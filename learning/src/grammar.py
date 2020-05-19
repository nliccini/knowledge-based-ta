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
                if (x == 's') or (w == 's' and x == 's') or (w == 's' and x == 'h') or (w == 'c' and x == 'h') or (x == 'x') or (x == 'z'):
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
