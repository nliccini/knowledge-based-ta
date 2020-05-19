"""
NAME: Nick Liccini

@brief: The set of rules that define the English grammar

@detail:
GrammarRules provides some of the Basic English rules for grammar

GrammarFrame is an interface for Basic English grammatical structures
    VerbFrame provides the frame for common verb phrases
    PrepositionalPhraseFrame provides the frame for common prepositions
    QuestionFrame provides the frame for simple questions

GrammarTools provides a few static methods for convenience
"""


from understanding import ThematicFrame


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
                             'until', 'till']
        self.conjunctions = ['and', 'or', 'but', 'if', 'so', 'next']
        self.adjectives = ['many', 'much', 'this', 'that', 'there']

        self.verbs = list()
        self.verbs.extend(self.qverbs)
        self.verbs.extend(['submit', 'check', 'start', 'fill', 'process', 'grade',
                           'give', 'get', 'take', 'doing', 'giving', 'gave', 'done',
                           'hand', 'took', 'return', 'go', 'going', 'gone', 'took',
                           'indicate', 'indicated', 'indicates', 'need', 'needs',
                           'say', 'says', 'affect', 'affects', 'influence', 'influences',
                           'expect', 'expected', 'expects', 'working', 'distribute', 'use',
                           'uses', 'find', 'found', 'finds', 'begin', 'complete', 'completed',
                           'close', 'open', 'closed', 'opened', 'write', 'contribute',
                           'contributing', 'contributes', 'getting', 'code', 'coding', 'finish',
                           'start', 'submitted', 'submit', 'submits', 'download', 'upload',
                           'downloaded', 'uploaded', 'submitting', 'expect', 'access', 'accessed',
                           'expected', ''])

    '''
    @brief: A new phrase generally starts with a verb or preposition
    '''
    def word_starts_new_phrase(self, word):
        phrase_words = list()
        phrase_words.extend(self.verbs)
        phrase_words.extend(self.prepositions)
        return word in phrase_words


class GrammarFrame(ThematicFrame):
    def __init__(self):
        super().__init__()
        self.rules = GrammarRules()
        self.agent = ''

    def parse(self, words):
        pass


class PrepositionalPhraseFrame(GrammarFrame):
    def __init__(self, prep, rest):
        super().__init__()
        self.preposition = prep
        self.object = []
        self.object_type = ''
        self.parse(rest)

        self.slots['thematic_object'] = GrammarTools.words2str(self.object)
        if self.preposition in self.constraints:
            types = self.constraints[self.preposition]
            self.object_type = types[0]

    '''
    @brief: Fill in the slots of the Prepositional Phrase frame using 
    the structure of a prepositional phrase

    @detail: Structure of prepositional phrases is generally:
        <preposition> <noun phrase>
    '''

    def parse(self, words):
        for word in words:
            if self.rules.word_starts_new_phrase(word):
                break
            self.object.append(word)


class VerbFrame(GrammarFrame):
    def __init__(self, verb, rest):
        super().__init__()
        self.verb = verb
        self.object = []
        self.parse(rest)

        self.slots['verb'] = self.verb
        self.slots['thematic_object'] = GrammarTools.words2str(self.object)

    '''
    @brief: Fill in the slots of the Verb frame using the structure of a verb

    @detail: Structure of verb phrases is generally:
        <verb> <noun phrase>
    '''

    def parse(self, words):
        for word in words:
            if self.rules.word_starts_new_phrase(word):
                break
            self.object.append(word)


class QuestionFrame(GrammarFrame):
    def __init__(self, words, context):
        super().__init__()

        self.qword = ''
        self.qvf = VerbFrame('', [])
        self.pfs = []
        self.vfs = []
        self.object = ''
        self.keywords = []
        self.noun_phrases = []

        self.contextual_keywords = context.keywords[context.topic]

        self.parse(words)

        self.slots['thematic_object'] = self.object
        self.slots['verb'] = self.qvf.verb

    def add_noun_phrase(self, phrase_words):
        if len(phrase_words) > 0:
            self.noun_phrases.append(phrase_words.copy())

    '''
    @brief: Choose the question object based on priority rules

    @detail: Priority rules are as follows:
        1. Question Verb Phrase
        2. Verb Phrases
        3. Noun Phrases
        4. Prepositional Phrases (that aren't constrained)
    '''

    def choose_object(self):
        try_qvf = True
        i_nouns = 0
        i_pfs = 0
        i_vfs = 0

        words = list()
        while len(words) == 0:
            if try_qvf and len(self.qvf.object) > 0:
                words = self.qvf.object
                try_qvf = False
            elif i_vfs < len(self.vfs) and len(self.vfs) > 0:
                words = self.vfs[i_vfs].object
                i_vfs += 1
            elif i_nouns < len(self.noun_phrases) and len(self.noun_phrases) > 0:
                words = self.noun_phrases[i_nouns]
                i_nouns += 1
            elif i_pfs < len(self.pfs) and len(self.pfs) > 0:
                pf = self.pfs[i_pfs]
                if pf.preposition not in self.constraints:
                    words = pf.object
                else:
                    words = []
                i_pfs += 1
            else:
                words = ['UNKNOWN']
                break

            words = GrammarTools.remove_words_in_list(words, self.rules.articles)
            words = GrammarTools.remove_words_in_list(words, self.rules.prepositions)
            words = GrammarTools.remove_words_in_list(words, self.rules.pronouns)
            words = GrammarTools.remove_words_in_list(words, self.contextual_keywords)
            words = GrammarTools.remove_words_in_list(words, self.rules.conjunctions)
            words = GrammarTools.remove_words_in_list(words, self.rules.adjectives)

        self.object = GrammarTools.words2str(words)

    '''
    @brief: Fill in the slots of the Question frame using simple
    question structure and Basic English

    @detail: Structure is generally as follows:
        <qword> <qverb> <qverb-noun phrase> <prepositional phrases> <noun phrases>
    '''

    def parse(self, words):
        noun_phrase_words = []
        noun_modifiers = list()
        noun_modifiers.extend(self.rules.articles)
        noun_modifiers.extend(self.rules.possessive_pronouns)

        for i in range(0, len(words)):
            word = words[i]
            if word in self.rules.qwords:
                self.qword = word
            elif word in self.rules.qverbs:
                self.add_noun_phrase(noun_phrase_words)
                noun_phrase_words.clear()
                self.qvf = VerbFrame(word, words[i + 1:])
            elif word in self.rules.prepositions:
                self.add_noun_phrase(noun_phrase_words)
                noun_phrase_words.clear()
                self.pfs.append(PrepositionalPhraseFrame(word, words[i + 1:]))
            elif word in self.rules.verbs and words[i-1] not in noun_modifiers:
                self.add_noun_phrase(noun_phrase_words)
                noun_phrase_words.clear()
                self.vfs.append(VerbFrame(word, words[i + 1:]))
            else:
                noun_phrase_words.append(word)
        self.add_noun_phrase(noun_phrase_words)

        self.choose_object()


class GrammarTools:
    def __init__(self):
        self.rules = GrammarRules()

    @staticmethod
    def remove_words_in_list(words, l):
        out = []
        for word in words:
            if word not in l:
                out.append(word)
        return out

    @staticmethod
    def words2str(words):
        out = ''
        for word in words:
            out = out + word + ' '
        return out.strip()
